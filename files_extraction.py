import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def Read_data(filename):
    csv_f = pd.read_csv(filename, low_memory=False)
    csv_f = csv_f.drop(labels="LABEL", axis=1)
    csv_f = csv_f.drop(index=range(3), axis=0)
    csv_f = csv_f.astype(float)

    return csv_f

def Rep_same_origin(pathfile,name_file,filename,ax, min_frames=10, x_left=None, x_right=None, y_bottom=None, y_top=None):
    csv_f = Read_data(filename)
    each_traj = csv_f.groupby(["TRACK_ID"]).apply(lambda x: x.sort_values(["POSITION_T"], ascending=True).reset_index(drop=True) + 1)

    ax.set_transform(ax.transData + plt.matplotlib.transforms.Affine2D().rotate_deg(180))

    x_max_global, y_max_global = float(-30000), float(-30000)
    x_min_global, y_min_global = float(30000), float(30000)

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

            # Update global min and max values
            x_min_global = min(x_min_global, min(X_l))
            x_max_global = max(x_max_global, max(X_l))
            y_min_global = min(y_min_global, min(Y_l))
            y_max_global = max(y_max_global, max(Y_l))

            ax.set_aspect('equal', adjustable='box')

            ax.axhline(y=0, color='black', linewidth=0.5)
            ax.axvline(x=0, color='black', linewidth=0.5)

    # Check for NaN or Inf before setting axis limits
    if not np.isnan(y_min_global) and not np.isnan(y_max_global) and not np.isinf(y_min_global) and not np.isinf(
            y_max_global):
        # Réglage des limites y pour que les trajectoires touchent l'axe y
        ax.set_ylim(top=-y_max_global, bottom=abs(y_min_global))

    # Réglage des limites y pour que les trajectoires touchent l'axe y
    ax.set_ylim(top=-y_max_global, bottom=abs(y_min_global))

    # Réglage des limites x pour que les trajectoires touchent l'axe x
    ax.set_xlim(left=x_min_global, right=x_max_global)

    ax.invert_yaxis()

    if x_left is not None and x_right is not None:
        ax.set_xlim(left=float(x_left), right=float(x_right))
    if y_bottom is not None and y_top is not None:
        ax.set_ylim(bottom=float(y_bottom), top=float(y_top))

    fig2, ax2 = plt.subplots(figsize=(6, 6))
    ax2.set_transform(ax2.transData + plt.matplotlib.transforms.Affine2D().rotate_deg(180))

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
            ax2.plot(X_l, -Y_l)

            # Update global min and max values
            x_min_global = min(x_min_global, min(X_l))
            x_max_global = max(x_max_global, max(X_l))
            y_min_global = min(y_min_global, min(Y_l))
            y_max_global = max(y_max_global, max(Y_l))

            ax2.set_aspect('equal', adjustable='box')
            plt.axhline(y=0, color='black', linewidth=0.5)
            plt.axvline(x=0, color='black', linewidth=0.5)


    # Réglage des limites y pour que les trajectoires touchent l'axe y
    ax2.set_ylim(top=-y_max_global, bottom=abs(y_min_global))

    # Réglage des limites x pour que les trajectoires touchent l'axe x
    ax2.set_xlim(left=x_min_global, right=x_max_global)

    plt.axhline(y=0, color='black', linewidth=0.5)
    plt.axvline(x=0, color='black', linewidth=0.5)

    ax2.invert_yaxis()

    if x_left is not None and x_right is not None:
        ax2.set_xlim(left=float(x_left), right=float(x_right))
    if y_bottom is not None and y_top is not None:
        ax2.set_ylim(bottom=float(y_bottom), top=float(y_top))

    plt.savefig(pathfile + name_file + '_same_origin.png')
    plt.close(fig2)

def Rep_traj_unchanged(filename, pathfile,name_file,ax, min_frames=10):
    csv_f = Read_data(filename)
    each_traj = csv_f.groupby(["TRACK_ID"]).apply(
        lambda x: x.sort_values(["POSITION_T"], ascending=True).reset_index(drop=True))

    folder_traj = pathfile + r'\particule'
    os.makedirs(folder_traj, exist_ok=True)
    os.chdir(folder_traj)
    name_file2 = name_file
    all_times = []

    fig2, ax2 = plt.subplots(figsize=(6, 6))

    each_traj["TRACK_ID"] = each_traj["TRACK_ID"].rank(method='dense').astype(int)

    each_traj["TRACK_ID"].max()

    for i in each_traj["TRACK_ID"].unique():
        # Calculate displacements relative to the first position
        X_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_X"]
        Y_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_Y"]
        T_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_T"] - each_traj[each_traj["TRACK_ID"] == i][
            "POSITION_T"].min() + 1
        all_times.extend(T_l.tolist())
        name_file = 'particule' + str(i) + '.txt'
        with open(name_file, 'w', encoding='utf-8') as fichier:
            # Write data to file with separate columns
            for t, x, y in zip(T_l, X_l, Y_l):
                fichier.write(f"{t} {x} {y}\n")
        # Plot trajectory
        if len(X_l) >= min_frames:
            ax2.plot(X_l, -Y_l + abs(each_traj["POSITION_Y"]).max())  # Inversion de Y lors du traçage

    ax2.set_aspect('equal', adjustable='box')
    # Réglage des limites y pour que les trajectoires touchent l'axe y
    ax2.set_ylim(top=each_traj["POSITION_Y"].max(), bottom=each_traj["POSITION_Y"].min())
    # Réglage des limites x pour que les trajectoires touchent l'axe x
    x_range = each_traj["POSITION_X"].max() - each_traj["POSITION_X"].min()
    ax2.set_xlim(left=each_traj["POSITION_X"].min(), right=each_traj["POSITION_X"].min() + x_range)
    plt.savefig(pathfile + name_file2 + '_traj_unchanged.png')
    plt.close(fig2)

    count_part_file = 0
    for i in each_traj["TRACK_ID"].unique():

        # Calculate displacements relative to the first position
        X_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_X"]
        Y_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_Y"]
        T_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_T"] - each_traj[each_traj["TRACK_ID"] == i]["POSITION_T"].min() + 1
        all_times.extend(T_l.tolist())
        # count_part_file += 1
        # name_file = 'particule' + str(int(i)) + '.txt'
        # with open(name_file, 'w', encoding='utf-8') as fichier:
        #     # Write data to file with separate columns
        #     for t, x, y in zip(T_l, X_l, Y_l):
        #         fichier.write(f"{t} {x} {y}\n")

        # Plot trajectory
        if len(X_l) >= min_frames:
            ax.plot(X_l, -Y_l+abs(each_traj["POSITION_Y"]).max())  # Inversion de Y lors du traçage

    ax.set_aspect('equal', adjustable='box')

    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.axvline(x=0, color='black', linewidth=0.5)

    # Réglage des limites y pour que les trajectoires touchent l'axe y
    ax.set_ylim(top=each_traj["POSITION_Y"].max(), bottom=each_traj["POSITION_Y"].min())

    # Réglage des limites x pour que les trajectoires touchent l'axe x
    x_range = each_traj["POSITION_X"].max() - each_traj["POSITION_X"].min()
    ax.set_xlim(left=each_traj["POSITION_X"].min(), right=each_traj["POSITION_X"].min() + x_range)  # Utilisation de x_range pour définir la largeur du tracé



def Distrib_direction_hist(pathfile,name_file,filename,fig):
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

    ax = fig.add_subplot(133, projection='polar')
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

    fig2 = plt.figure(figsize=(8, 8))
    ax2 = fig2.add_subplot(111, polar=True)
    ax2.set_theta_direction(-1)

    bars = ax2.hist(np.deg2rad(directions), bins=np.deg2rad(bin_edges), weights=weights, color='steelblue', alpha=0.8)

    max_occ = np.max(occurrences)
    for bar, occurrence, bin_edge in zip(bars[0], occurrences, bin_edges[:-1]):
        height = bar
        angle = np.deg2rad(bin_edge)

        if np.any(occurrence > 0.3 * max_occ):  # Threshold for text display height
            ax2.text(angle, height, occurrence, ha='center', va='bottom', fontsize=14, color='red')

    ax2.set_yticklabels([])

    plt.savefig(pathfile + name_file + '_hist.png')
    plt.close(fig2)

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




