import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

def Read_data(filename):
    csv_f = pd.read_csv(filename, low_memory=False)
    csv_f = csv_f.drop(labels="LABEL", axis=1)
    csv_f = csv_f.drop(index=range(3), axis=0)
    csv_f = csv_f.astype(float)

    return csv_f

def Rep_same_origin(filename, min_frames=10,x_left=None,x_right=None,y_bottom=None,y_top=None):
    csv_f = Read_data(filename)
    each_traj = csv_f.groupby(["TRACK_ID"]).apply(lambda x: x.sort_values(["POSITION_T"], ascending=True).reset_index(drop=True) + 1)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_transform(ax.transData + plt.matplotlib.transforms.Affine2D().rotate_deg(180))

    for i in each_traj["TRACK_ID"].unique():
        # Calculate displacements relative to the first position
        X_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_X"] - \
              each_traj[each_traj["TRACK_ID"] == i]["POSITION_X"].iloc[0]
        Y_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_Y"] - \
              each_traj[each_traj["TRACK_ID"] == i]["POSITION_Y"].iloc[0]

        # Tracing the trajectory
        # Filter trajectories based on the number of frames
        if len(X_l) >= min_frames:
            # Tracing the trajectory
            ax.plot(X_l, -Y_l)

            # Inversion de l'axe y
            ax.invert_yaxis()

            # Réglage des limites y pour centrer le graphe
            y_range = max(Y_l) - min(Y_l)
            ax.set_ylim(top=max(Y_l) + y_range / 2, bottom=min(Y_l) - y_range / 2)

            # Réglage de l'aspect du graphe et ajout des lignes de référence
            ax.set_aspect('equal', adjustable='box')
            plt.axhline(y=0, color='black', linewidth=0.5)
            plt.axvline(x=0, color='black', linewidth=0.5)
    print("Max frame = ", each_traj["POSITION_T"].max())

    if x_left is not None and x_right is not None:
        ax.set_xlim(left=float(x_left), right=float(x_right))
    if y_bottom is not None and y_top is not None:
        ax.set_ylim(bottom=float(y_bottom), top=float(y_top))

def Rep_traj_unchanged(filename, pathfile,min_frames=10,x_left=None,x_right=None,y_bottom=None,y_top=None):
    csv_f = Read_data(filename)
    each_traj = csv_f.groupby(["TRACK_ID"]).apply(lambda x: x.sort_values(["POSITION_T"], ascending=True).reset_index(drop=True))

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.invert_yaxis()
    ax.set_transform(ax.transData + plt.matplotlib.transforms.Affine2D().rotate_deg(180))

    folder_traj = pathfile + r'\particule'
    os.makedirs(folder_traj, exist_ok=True)
    os.chdir(folder_traj)
    max_time = each_traj["POSITION_T"].max()

    for i in each_traj["TRACK_ID"].unique():
        # Calculate displacements relative to the first position
        X_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_X"]
        Y_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_Y"]
        T_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_T"]
        name_file = 'particule'+str(int(i))+'.txt'
        with open(name_file,'w', encoding='utf-8') as fichier:
            # Write data to file with separate columns
            for t, x, y in zip(T_l, X_l, Y_l):
                fichier.write(f"{t} {x} {y}\n")

        # Plot trajectory
        if len(X_l) >= min_frames:
            ax.plot(X_l, Y_l)

    if x_left is not None and x_right is not None:
        ax.set_xlim(left=float(x_left), right=float(x_right))
    if y_bottom is not None and y_top is not None:
        ax.set_ylim(bottom=float(y_bottom), top=float(y_top))

    return max_time

def Distrib_direction_hist(filename, ax=None):
    # Import CSV file containing X and Y positions for each particle
    df = Read_data(filename)
    each_traj = df.groupby(["TRACK_ID"]).apply(lambda x: x.sort_values(["POSITION_T"], ascending=True))
    directions = []

    for i in each_traj["TRACK_ID"].unique():
        mask_id = each_traj["TRACK_ID"] == i
        df_particule_i = each_traj[mask_id]

        dy = df_particule_i["POSITION_Y"].iloc[-1] - df_particule_i["POSITION_Y"].iloc[0]
        dx = df_particule_i["POSITION_X"].iloc[-1] - df_particule_i["POSITION_X"].iloc[0]

        direction = np.rad2deg(np.arctan2(dy, dx))

        if direction < 0:
            direction += float(360)

        # Group directions near cardinal directions together
        if 0 <= direction < 30 :
            directions.append(15)
        elif 30 <= direction < 60:
            directions.append(45)
        elif 60 <= direction < 90:
            directions.append(75)
        elif 90 <= direction < 120:
            directions.append(105)
        elif 120 <= direction < 150:
            directions.append(135)
        elif 150 <= direction < 180:
            directions.append(165)
        elif 180 <= direction < 210:
            directions.append(195)
        elif 210 <= direction < 240:
            directions.append(225)
        elif 240 <= direction < 270:
            directions.append(255)
        elif 270 <= direction < 300:
            directions.append(285)
        elif 300 <= direction < 330:
            directions.append(305)
        elif 330 <= direction < 360:
            directions.append(335)

    # Create a polar histogram
    if ax is None:
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111, polar=True)
        ax.set_theta_direction(-1)

    occurrences, bin_edges = np.histogram(directions, bins=np.linspace(0, 360, 120 + 1))

    weights = np.ones_like(directions) * len(directions)

    # Plot the circular histogram
    bars = ax.hist(np.deg2rad(directions), bins=np.deg2rad(bin_edges), weights=weights, color='steelblue', alpha=0.8)

    max_occ = np.max(occurrences)
    for bar, occurrence, bin_edge in zip(bars[0], occurrences, bin_edges[:-1]):
        height = bar
        angle = np.deg2rad(bin_edge)

        if np.any(occurrence > 0.3 * max_occ):  # Threshold for text display height
            ax.text(angle, height, occurrence, ha='center', va='bottom', fontsize=14, color='red')

    ax.set_yticklabels([])

def calcul_coefficient_diffusion(filename, nb_iterations):
    data_tracking = Read_data(filename)
    deplacements_x = np.diff(data_tracking['POSITION_X'])
    deplacements_y = np.diff(data_tracking['POSITION_Y'])
    deplacements_carres = deplacements_x**2 + deplacements_y**2

    msd_estime = []
    nb_deplacements = len(deplacements_carres)

    duree_totale = data_tracking['POSITION_T'].iloc[-1] - data_tracking['POSITION_T'].iloc[0]

    for _ in range(nb_iterations):
        intervalle_temps = np.random.randint(0, nb_deplacements)
        temps_cumulatif = data_tracking['POSITION_T'].iloc[intervalle_temps] - data_tracking['POSITION_T'].iloc[0]
        temps_normalise = temps_cumulatif / duree_totale
        if np.isclose(temps_normalise, 0):
            continue
        msd_estime.append(np.mean(deplacements_carres[:intervalle_temps]) / temps_normalise)

    msd_moyen = np.mean(msd_estime)
    coefficient_diffusion_estime = msd_moyen / 4

    return coefficient_diffusion_estime


def Analyse_diff_rate(filename):
    df = Read_data(filename)

    # Filtrer les données pour une seule trajectoire
    df_trajectoire = df[df['TRACK_ID'] == 2]

    # Tri des données par temps croissant pour chaque trajectoire
    df['POSITION_T'] = pd.to_datetime(df['POSITION_T'])
    df.sort_values(['TRACK_ID', 'POSITION_T'], inplace=True)

    # Calcul des déplacements
    df['dx'] = df.groupby('TRACK_ID')['POSITION_X'].diff()
    df['dy'] = df.groupby('TRACK_ID')['POSITION_Y'].diff()

    # Calcul de la distance moyenne au carré
    df['distance_carre'] = df['dx'] ** 2 + df['dy'] ** 2

    # Calcul du temps moyen au carré
    df['POSITION_T'] = pd.to_datetime(df['POSITION_T'])
    df['temps_carre'] = (df['POSITION_T'] - df['POSITION_T'].min()).dt.total_seconds() ** 2

    # Calcul de la distance moyenne au carré en fonction du temps moyen au carré
    plt.plot(df['temps_carre'], df['distance_carre'], 'b.')
    plt.xlabel('Temps moyen au carré')
    plt.ylabel('Distance moyenne au carré')
    plt.title('Analyse de mouvement brownien')
    plt.show()

    # Calcul de la pente (coefficient de diffusion)
    pente = np.polyfit(df['temps_carre'], df['distance_carre'], 1)[0]
    coefficient_diffusion = pente / 4

    print('Coefficient de diffusion estimé:', coefficient_diffusion)

def MSD_diff_rate(filename,window_size):
    df = Read_data(filename)

    # Tri des données par temps croissant pour chaque trajectoire
    # df['POSITION_T'] = pd.to_datetime(df['POSITION_T'])
    df.sort_values(['TRACK_ID', 'POSITION_T'], inplace=True)

    # Calcul des déplacements
    df['dx'] = df.groupby('TRACK_ID')['POSITION_X'].diff()
    df['dy'] = df.groupby('TRACK_ID')['POSITION_Y'].diff()

    # Calcul du Mean Squared Displacement (MSD)
    df['distance_carre'] = df['dx'] ** 2 + df['dy'] ** 2
    df['POSITION_T'] = pd.to_datetime(df['POSITION_T'])
    df['temps_cumulatif'] = (df['POSITION_T'] - df['POSITION_T'].min()).dt.total_seconds()

    # Normalisation temporelle
    df['temps_normalise'] = df['temps_cumulatif'] / df.groupby('TRACK_ID')['temps_cumulatif'].transform('max')

    # Calcul du MSD moyen pour chaque temps normalisé
    df['msd_norm_time'] = df.groupby('temps_normalise')['distance_carre'].transform('mean')

    # Calcul de la courbe moyenne de toutes les trajectoires
    msd_moyen = df.groupby('temps_normalise')['msd_norm_time'].mean()

    # Lissage de la courbe moyenne avec une moyenne mobile
    msd_moyen_lisse = moving_average(msd_moyen.values, window_size)

    # Obtenir une palette de couleurs pour les trajectoires
    palette = sns.color_palette('colorblind', len(df['TRACK_ID'].unique()))

    # Tracé des courbes MSD pour chaque trajectoire
    for i, (_, group) in enumerate(df.groupby('TRACK_ID')):
        color = palette[i % len(palette)]  # Sélectionne une couleur de la palette
        plt.plot(group['temps_normalise'], group['msd_norm_time'], '-', alpha=0.15, color=color)

    # Régression linéaire pour estimer la tendance moyenne
    pente, ordonnee_origine = np.polyfit(df['temps_normalise'], df['msd_norm_time'], 1)
    tendance_moyenne = pente * df['temps_normalise'] + ordonnee_origine
    plt.plot(df['temps_normalise'], tendance_moyenne, 'g--', label='Tendance moyenne')

    # Tracé de la courbe moyenne des MSD de toutes les trajectoires
    plt.plot(msd_moyen.index[window_size-1:], msd_moyen_lisse, 'r-', label='MSD mean (smoothed)')
    plt.xlabel('Normalized time')
    plt.ylabel('MSD')
    plt.title('Mean Squared Displacement (MSD) analysis with time normalization')
    plt.legend()

    # Calcul du coefficient de diffusion
    temps_normalise = df['temps_normalise'].values
    msd = df['msd_norm_time'].values
    coefficient_diffusion = np.polyfit(temps_normalise, msd, 1)[0] / 4

    print('Coefficient de diffusion estimé:', coefficient_diffusion)

def moving_average(x, window_size):
    return np.convolve(x, np.ones(window_size) / window_size, mode='valid')



