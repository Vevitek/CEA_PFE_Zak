import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

""" at the end we should get the mean square displacement of the particle trajectories;
if multiple particles are present then assume the mean of all MSDs
"""
class MSDtraj:

    def __init__(self,dirname,filenum,coords,timestep,timeCMSD=1000):
        self.dirname = dirname +'\particule'
        self.filenum = filenum
        self.timeCMSD = timeCMSD
        self.coords = coords
        self.timestep = timestep

    # importing trajectory
    def importtraj(self,num,delimiter =' '):
            lencoords = len(self.coords)
            d = [] # stores data from the text file
            filename = self.dirname + r'\particule' + str(num)+".txt"
            with open(filename, 'r', encoding='utf-8') as source:
                for line in source:
                    if delimiter in line:
                        f = line.split(' ')
                        if lencoords == 4:  # for 3D case
                            d.append(list(map(lambda i: float(f[i]),[0,1,2,3])))
                        elif lencoords == 3:  # for 2D case
                            d.append(list(map(lambda i: float(f[i]), [0, 1, 2])))
                        else:  # for 1-D
                            d.append(map(lambda i: float(f[i]),[0,1]))

            return pd.DataFrame(d, columns=self.coords)

            # return data

    # function to compute MSD for one trajectory
    def compute_msd(self,trajectory):
        tau = trajectory['t'].copy()
        tau = tau[0:self.timeCMSD]
        tau = pd.to_numeric(tau)  # Counter for consecutive zeros
        # print(tau)
        shifts = np.floor(tau / self.timestep).astype(int)
        msds = []
        msds_std = []
        consecutive_zeros = 0  # Counter for consecutive zeros

        for i, shiftpos in enumerate(shifts):
            shifted_trajectory = trajectory[self.coords].shift(-shiftpos)
            shifted_trajectory = shifted_trajectory.interpolate()  # Fill in missing values by interpolation

            if shifted_trajectory.shape[0] >= 10:  # Filter trajectories with fewer than 10 points
                diffs = shifted_trajectory - trajectory[self.coords]
                sqdist = np.square(diffs).sum(axis=1)
                msd = sqdist.mean()
                msd_std = sqdist.std()

                if msd == 0:  # Vérifier si la valeur MSD est nulle
                    consecutive_zeros += 1
                else:
                    if consecutive_zeros <= 3:  # Check for less than three consecutive zeros
                        msds.append(msd)
                        msds_std.append(msd_std)
                    consecutive_zeros = 0

        msds = pd.DataFrame({'msds': msds, 'tau': tau[:len(msds)], 'msds_std': msds_std})
        return msds, tau[:len(msds)]

    def plot_msd(self, MSDlist, msdcomposelist, tau_list):
        plt.figure()
        for msd, tau in zip(MSDlist, tau_list):
            plt.plot(msd.index, msd.values, alpha=0.2)
        plt.plot(msdcomposelist, 'r', label='Mean value')
        plt.xlabel('Time')
        plt.ylabel('Mean Square Displacement (MSD)')
        plt.legend()

    def slope_origin(self,msddata,nb_values_for_reg):
        x = np.arange(len(msddata[1:nb_values_for_reg]))
        grad = np.polyfit(x, msddata[1:nb_values_for_reg], 1)[0]  # using the first 100 values for computing gradient

        print('the effective diffusion coefficient is : ' + str(
            grad / (6 * 1e-6)) + ' um^2/sec')  # effective diffusion coefficient `

        x = np.arange(len(msddata))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x[:nb_values_for_reg],
                                                                       msddata[:nb_values_for_reg])

        # Affichage des résultats
        print("Slope of regression line :", slope)
        print("Constant term of the regression line :", intercept)
        print("Correlation coefficient :", r_value)
        print("p-value :", p_value)

        # Tracé du graphique avec la droite de régression
        plt.figure()
        plt.plot(x, msddata, 'o', label='MSD data')
        plt.plot(x, intercept + slope * x, 'r', label='Regression line')
        plt.xlabel('Tau')
        plt.ylabel('MSD')
        plt.legend()

    ## main import trajectories, calculate composed MSD and STD
    def main(self):
        MSDlist,STDlist = [],[]
        tau_list = []
        for num in range(1, self.filenum + 1):
            traj = self.importtraj(num)
            msd, tau = self.compute_msd(traj)
            MSDlist.append(msd['msds'])
            STDlist.append(msd['msds_std'])
            tau_list.append(tau)
        max_len = max(len(msd) for msd in MSDlist)
        padded_MSDlist = [np.pad(msd, (0, max_len - len(msd)), mode='constant', constant_values=np.nan) for msd in
                          MSDlist]
        msdcomposelist = np.nanmean(np.array(padded_MSDlist), axis=0)

        self.plot_msd(MSDlist, msdcomposelist, tau_list)

        return msdcomposelist, MSDlist, tau_list