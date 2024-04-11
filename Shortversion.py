

from files_extraction import *
from MSDtraj import *
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy import stats



deltat = 10
def process_data_im(filename,pathfile,name_file,min_frames,x_left, x_right, y_bottom, y_top):
    fig, axes = plt.subplots(1, 3, figsize=(8, 5))
    Rep_traj_unchanged(filename, pathfile,name_file,axes[0], min_frames)
    Rep_same_origin(pathfile,name_file,filename,axes[1], min_frames, x_left, x_right, y_bottom, y_top)
    Distrib_direction_hist(pathfile,name_file,filename,fig)

    plt.tight_layout() # Ajuster la mise en page


def process_data_msd(pathfile,name_file,ax,label,min_num_MSD,reg_value,deltat,*remove_lasts_pts):
    msd = MSDtraj(pathfile, ['t', 'x', 'y'], deltat,min_num_MSD, remove_lasts_pts[0])  # MSDtraj(pathfile, [time, x_position, y_position],
    # timestep in ms, number of last points to remove from graphs if outliers)

    msddata, MSDlist, taul = msd.main()
    plt.savefig(pathfile + name_file + '_MeanMSD.png')
    msd.multiple_plots(msddata, ax, label=label)

    nb_values_for_grad = reg_value
    x = np.arange(len(msddata[1:nb_values_for_grad]))*deltat/1000
    grad = np.polyfit(x, msddata[1:nb_values_for_grad], 1)[0]  # using the first nb values for computing gradient

    D_grad = grad/4

    # x = np.arange(len(msddata))

    # Calcul de la régression linéaire
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, msddata[1:nb_values_for_grad])

    previous_r_value = None

    while r_value<0.998 and r_value!=previous_r_value:
        print("unstable r_value :",r_value)
        reg_value +=1
        nb_values_for_grad = reg_value
        x = np.arange(len(msddata[1:nb_values_for_grad]))*deltat/1000
        grad = np.polyfit(x, msddata[1:nb_values_for_grad], 1)[0]  # using the first nb values for computing gradient

        D_grad = grad/4

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
    D = kb*T / (0.5*10**(-6)*np.pi*µ*6)

    print("Estimated radius", name_file[1:]," :", R*10**(9) ,"nm")
    print("Expected diffusive coefficient : ", D*10**(12), "µm²/s","\n")

    return msddata, intercept, slope, x


def MSD_superimposition(msdcomposelists,pathfile,intercepts,slopes, deltat=1):
    fig2, ax2 = plt.subplots()
    for i, (msdcomposelist, intercept, slope) in enumerate(zip(msdcomposelists, intercepts, slopes)):
        x = np.arange(len(msdcomposelist))*deltat/1000
        ax2.plot(x, msdcomposelist ,label=f'Curve {i+1}')
        ax2.plot(x, intercept + slope * x, 'r', label=f'Reg{i+1}')




    ax2.set_title("MSD Comparison")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("MSD  (µm²)")
    ax2.legend()

    plt.savefig(os.path.dirname(pathfile) + r"\C_superimposition")

