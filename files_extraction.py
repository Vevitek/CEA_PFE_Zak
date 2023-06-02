import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def Read_data(filename):
    csv_f = pd.read_csv(filename, low_memory=False) #, delimiter=';'
    csv_f = csv_f.drop(labels="LABEL", axis=1)
    csv_f = csv_f.drop(index=range(3), axis=0)
    csv_f = csv_f.astype(float)

    return csv_f


def Rep_same_origin(filename, ax=None):
    csv_f = Read_data(filename)

    each_traj = csv_f.groupby(["TRACK_ID"]).apply(lambda x: x.sort_values(["POSITION_T"], ascending=True))

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.invert_yaxis()
        ax.set_transform(ax.transData + plt.matplotlib.transforms.Affine2D().rotate_deg(180))



    for i in each_traj["TRACK_ID"].unique():
        # Calculer les déplacements relatifs à la première position
        X_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_X"] - \
              each_traj[each_traj["TRACK_ID"] == i]["POSITION_X"].iloc[0]
        Y_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_Y"] - \
              each_traj[each_traj["TRACK_ID"] == i]["POSITION_Y"].iloc[0]

        # Tracer la trajectoire


        ax.plot(X_l, Y_l)
        ax.set_aspect('equal', adjustable='box')

        plt.axhline(y=0, color='black', linewidth=0.5)
        plt.axvline(x=0, color='black', linewidth=0.5)

def Rep_traj_unchanged(filename, ax=None):
    csv_f = Read_data(filename)

    each_traj = csv_f.groupby(["TRACK_ID"]).apply(lambda x: x.sort_values(["POSITION_T"], ascending=True))

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.invert_yaxis()
        ax.set_transform(ax.transData + plt.matplotlib.transforms.Affine2D().rotate_deg(180))

    for i in each_traj["TRACK_ID"].unique():
        # Calculer les déplacements relatifs à la première position
        X_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_X"]
        Y_l = each_traj[each_traj["TRACK_ID"] == i]["POSITION_Y"]

        # Tracer la trajectoire
        ax.plot(X_l, Y_l)

def Distrib_direction_hist(filename, ax=None):
    # Import CSV file containing X and Y positions for each particle
    df = Read_data(filename)

    each_traj = df.groupby(["TRACK_ID"]).apply(lambda x: x.sort_values(["POSITION_T"], ascending=True))
    directions = []

    for i in each_traj["TRACK_ID"].unique():
        masque_id = each_traj["TRACK_ID"] == i
        df_particule_i = each_traj[masque_id]

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

    # Set number of bins and bin edges
    # bin_edges = np.linspace(0, 360, 120 + 1)  # Bin edges in degrees

    occurrences, bin_edges = np.histogram(directions, bins=np.linspace(0, 360, 120 + 1))

    weights = np.ones_like(directions) * len(directions)

    # Plot the circular histogram
    bars = ax.hist(np.deg2rad(directions), bins=np.deg2rad(bin_edges), weights=weights, color='steelblue', alpha=0.8)

    for bar, occurrence, bin_edge in zip(bars[0], occurrences, bin_edges[:-1]):
        height = bar
        angle = np.deg2rad(bin_edge)
        ax.text(angle, height, occurrence, ha='center', va='bottom', fontsize=14, color='red')

    ax.set_yticklabels([])




def Mean_Square_Displacement(filename, deltaT=1, ax=None):
    df = Read_data(filename)

    each_traj = df.groupby(["TRACK_ID"]).apply(lambda x: x.sort_values(["POSITION_T"], ascending=True))

    MSD_all = []
    for i in each_traj["TRACK_ID"].unique():
        mask = each_traj["TRACK_ID"] == i
        df_i = each_traj[mask].reset_index(drop=True)

        # Calculer la distance euclidienne entre les positions x et y
        r = np.sqrt(df_i["POSITION_X"] ** 2 + df_i["POSITION_Y"] ** 2)

        # Calculer la différence de distance entre deux temps consécutifs
        diff = np.diff(r)

        # Calculer le carré de la différence de distance
        diff_sq = diff ** 2

        # Calculer le MSD pour chaque temps de retard
        MSD = []
        for j in range(1, len(df_i)):
            msd_j = np.mean(diff_sq[:len(diff_sq) - j])
            MSD.append(msd_j)
        MSD_all.append(MSD)

    # Tracer le MSD pour chaque trajectoire
    fig, ax = plt.subplots()
    for i in range(len(MSD_all)):
        ax.plot(range(len(MSD_all[i])), abs(MSD_all[i] - MSD_all[i][0]))

    ax.set_xlabel('Time')
    ax.set_ylabel('Mean Square Displacement')

def Mean2(filename, ax=None):
    df = pd.read_csv(filename, low_memory=False)
    df = df.drop(labels="LABEL", axis=1)
    df = df.drop(index=range(3), axis=0)
    df = df.astype(float)

    df["POSITION_Y"] = -1 * df["POSITION_Y"]

    each_traj = df.groupby(["TRACK_ID"]).apply(lambda x: x.sort_values(["POSITION_T"], ascending=True))

    MSD_list = []
    for i in each_traj["TRACK_ID"].unique():
        mask = each_traj["TRACK_ID"] == i
        df_i = each_traj[mask].reset_index(drop=True)

        diff = df_i[["POSITION_X", "POSITION_Y"]] - df_i.iloc[0][["POSITION_X", "POSITION_Y"]]
        diff_sq = diff ** 2
        MSD_list.append(diff_sq.values)

    MSD_array = np.vstack(MSD_list)
    print(type(MSD_array))

    MSD_means = np.nanmean(MSD_array, axis=0)
    print(type(MSD_means))

    if ax is None:
        fig, ax = plt.subplots()

    ax.plot(df["POSITION_T"][:len(MSD_means)], MSD_means)
    ax.set_xlabel("Time (frames)")
    ax.set_ylabel("MSD")
    ax.set_title("Mean Squared Displacement")

def Mean3(filename, ax=None):
    # Step 1: Read CSV file
    df = pd.read_csv(filename, low_memory=False)

    # Step 2: Drop useless lines and columns

    df = df.drop(labels="LABEL", axis=1)
    df = df.drop(index=range(3), axis=0)
    df = df.astype(float)   #By default, str is the type

    # Step 3: Sort data
    df = df.sort_values(by=['TRACK_ID', 'POSITION_T'])

    # Step 4: Calculate the differences of position by time
    df['DX'] = df.groupby('TRACK_ID')['POSITION_X'].diff()
    df['DY'] = df.groupby('TRACK_ID')['POSITION_Y'].diff()

    # Step 5: Calculate MSD for each particle
    df['MSD'] = df['DX'] ** 2 + df['DY'] ** 2

    # Step 6: Calculate MSD mean for each time using all trajectories
    msd_mean = df.groupby('POSITION_T')['MSD'].mean()

    msd_mean_all = df.groupby('POSITION_T')['MSD'].mean()

    # Step 7: Check if the curve is increasing according to brownian motion
    if not np.all(np.diff(msd_mean.values) >= 0):
        print('La courbe MSD n\'est pas croissante conformément à un mouvement brownien !')

    if ax is None:
        fig, ax = plt.subplots()
    # Step 8: Plot MSD global
    ax.plot(msd_mean_all.index, msd_mean_all.values, label="All trajectories",linewidth=2.5)

    # Step 9: Calculate MSD for each trajectory
    msd_mean_traj = df.groupby(['TRACK_ID', 'POSITION_T'])['MSD'].mean().reset_index()

    # Step 10: Plot MSD for each trajectory
    for traj_id in msd_mean_traj['TRACK_ID'].unique():
        traj_data = msd_mean_traj[msd_mean_traj['TRACK_ID'] == traj_id]
        plt.plot(traj_data['POSITION_T'][0:3], traj_data['MSD'][0:3],alpha=0.6)

    ax.set_xlabel('Time T')
    ax.set_ylabel('Mean Square Displacement (MSD)')
    ax.legend()

def MSD_GPT():
    # Set seed for reproducibility
    np.random.seed(42)

    # Set parameters
    n_steps = 1000
    step_size = 1
    dimension = 2

    # Generate random steps for Brownian motion
    steps = np.random.normal(scale=step_size, size=(n_steps, dimension))

    # Set initial position
    start_pos = np.zeros((1, dimension))

    # Calculate positions over time
    positions = np.concatenate([start_pos, np.cumsum(steps, axis=0)])

    # Calculate the displacement
    displacement = positions[1:] - start_pos

    # Calculate the squared displacement
    squared_displacement = np.sum(displacement ** 2, axis=1)

    # Calculate the mean square displacement
    msd = np.mean(squared_displacement)

    # Plot the positions over time
    # plt.plot(positions[:, 0], positions[:, 1], alpha=0.5)
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.title('2D Brownian Motion')
    # plt.show()

    # Plot the MSD over time
    time = np.arange(n_steps - 1)
    squared_displacement = squared_displacement[:-1]
    plt.figure()
    plt.plot(time, squared_displacement)
    plt.xlabel('Time')
    plt.ylabel('Squared Displacement')
    plt.title('Mean Square Displacement = {}'.format(msd))