from files_extraction import *
from MSDtraj import *
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
def process_data_im(filename,pathfile,name_file,min_frames,x_left, x_right, y_bottom, y_top):
    fig, axes = plt.subplots(1, 3, figsize=(8, 5))
    Rep_traj_unchanged(filename, pathfile,name_file,axes[0], min_frames)
    Rep_same_origin(pathfile,name_file,filename,axes[1], min_frames, x_left, x_right, y_bottom, y_top)
    Distrib_direction_hist(pathfile,name_file,filename,fig)

    plt.tight_layout() # Ajuster la mise en page


def process_data_msd(pathfile,name_file,ax,label,min_num_MSD,reg_value,deltaT=50):
    msd = MSDtraj(pathfile, ['t', 'x', 'y'], deltaT,min_num_MSD, 0)  # MSDtraj(pathfile, [time, x_position, y_position],
    # timestep in ms, number of last points to remove from graphs if outliers)

    msddata, MSDlist, taul = msd.main()
    plt.savefig(pathfile + name_file + '_MeanMSD.png')
    msd.multiple_plots(msddata, ax, label=label)

    nb_values_for_grad = reg_value
    x = np.arange(len(msddata[1:nb_values_for_grad]))
    grad = np.polyfit(x, msddata[1:nb_values_for_grad], 1)[0]  # using the first nb values for computing gradient

    D_grad = grad/(4*6.2**2)

    # x = np.arange(len(msddata))

    # Calcul de la régression linéaire
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, msddata[1:nb_values_for_grad])

    previous_r_value = None

    while r_value<0.998 and r_value!=previous_r_value:
        print("unstable r_value :",r_value)
        reg_value +=1
        nb_values_for_grad = reg_value
        x = np.arange(len(msddata[1:nb_values_for_grad]))
        grad = np.polyfit(x, msddata[1:nb_values_for_grad], 1)[0]  # using the first nb values for computing gradient

        D_grad = grad / (4 * 6.2 ** 2)

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, msddata[1:nb_values_for_grad])
        previous_r_value = r_value


    print('the effective diffusion coefficient is : ' + str(
        D_grad) + ' µm^2/ms')  # effective diffusion coefficient `
    # Affichage des résultats
    print("Slope of regression line :", slope)
    # print("Constant term of the regression line :", intercept)
    print("Correlation coefficient :", r_value)
    # print("p-value :", p_value)

    kb = 1.3806488e-23 # J.K-1.
    T = 293 # K
    µ = 1.00e-3 # Pa.s

    R = kb*T / (6*np.pi*µ*D_grad*10**(-12))

    print("Estimated radius", name_file," :", R*10**(9) ,"nm","\n")

def alternative_calculus_linreg(pathfile,deltaT, min_num_MSD):
    # Données
    msd = MSDtraj(pathfile, ['t', 'x', 'y'], deltaT, min_num_MSD, 0)
    msddata, MSDlist, taul = msd.main()
    x = np.arange(len(msddata))
    y = msddata

    # Nombre maximal de points pour la régression linéaire
    max_points = len(msddata)

    # Diviser les données en plusieurs sous-ensembles pour la validation croisée
    tscv = TimeSeriesSplit(n_splits=5)

    best_mse = float('inf')
    best_num_points = 0

    for num_points in range(2, max_points + 1):
        mse_values = []

        for train_index, test_index in tscv.split(x):
            x_train, x_test = x[train_index], x[test_index]
            y_train, y_test = y[train_index], y[test_index]

            # Ajuster une régression linéaire
            model = LinearRegression()
            model.fit(x_train[:num_points].reshape(-1, 1), y_train[:num_points])

            # Prédire sur les données de test
            y_pred = model.predict(x_test.reshape(-1, 1))

            # Calculer l'erreur quadratique moyenne
            mse = mean_squared_error(y_test, y_pred)
            mse_values.append(mse)

        # Utiliser la moyenne des erreurs quadratiques moyennes
        average_mse = np.mean(mse_values)

        # Mettre à jour si le modèle actuel est meilleur
        if average_mse < best_mse:
            best_mse = average_mse
            best_num_points = num_points

    # Utiliser le meilleur nombre de points pour la régression linéaire
    print("Meilleur nombre de points pour la régression linéaire :", best_num_points)
