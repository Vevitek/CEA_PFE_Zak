import matplotlib.pyplot as plt
from files_extraction import *
from MSDtraj import *
from scipy import stats


filename = r'D:\...' #exact location of your file, for example r'D:\...\my_file.csv

pathfile = r'C:\...' #path where you want to register your data (images + text files)
name_file = r'\prefix of your file' #make sure you keep the \ before the name you want to give to your files


##---------------------Image processing---------------------##
Rep_traj_unchanged(filename,pathfile)
plt.savefig(pathfile+name_file+'_traj_unchanged.png')
Rep_same_origin(filename)
plt.savefig(pathfile+name_file+'_same_origin.png')
Distrib_direction_hist(filename)
plt.savefig(pathfile+name_file+'_hist.png')

##---------------------MSD calculation---------------------##
msd = MSDtraj(pathfile+ r'\particule',130,['t','x','y'],1,60)
msddata= msd.main()

plt.figure()
plt.plot(msddata)

nb_values_for_grad = 10
x = np.arange(len(msddata[1:nb_values_for_grad]))
grad = np.polyfit(x,msddata[1:nb_values_for_grad], 1)[0] # using the first 100 values for computing gradient

print('the effective diffusion coefficient is : ' + str(grad/(6*1e-6)) + ' um^2/sec') # effective diffusion coefficient `

x = np.arange(len(msddata))

# Calcul de la régression linéaire
slope, intercept, r_value, p_value, std_err = stats.linregress(x, msddata)

# Affichage des résultats
print("Pente de la droite de régression :", slope)
print("Terme constant de la droite de régression :", intercept)
print("Coefficient de corrélation :", r_value)
print("Valeur p :", p_value)


plt.figure()

# Tracé du graphique avec la droite de régression
plt.plot(x, msddata, 'o', label='Données')
plt.plot(x, intercept + slope*x, 'r', label='Droite de régression')
plt.xlabel('Tau')
plt.ylabel('MSD')
plt.legend()

plt.show()




