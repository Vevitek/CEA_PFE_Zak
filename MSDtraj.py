import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import os

forty_x_magn = 6.67

""" at the end we should get the mean square displacement of the particle trajectories;
if multiple particles are present then assume the mean of all MSDs
"""
class MSDtraj:

    def __init__(self,dirname,coords,deltaT,min_num_MSD,remove_lasts_pts):
        self.dirname = dirname +'\particule'
        files = [file for file in os.listdir(dirname +'\particule') if os.path.isfile(os.path.join(dirname +'\particule', file))]
        self.filenum = len(files)-1
        self.coords = coords
        self.timestep = 1
        self.remove_lasts_pts = remove_lasts_pts
        self.deltat = deltaT
        self.min_num_MSD = min_num_MSD


    def importtraj(self,num,delimiter =' '):
            d = [] # stores data from the text file
            filename = self.dirname + r'\particule' + str(num)+".txt"
            with open(filename, 'r', encoding='utf-8') as source:
                for line in source:
                    if delimiter in line:
                        f = line.split(' ')
                        d.append(list(map(lambda i: float(f[i]), [0, 1, 2])))

            return pd.DataFrame(d, columns=self.coords)

    # function to compute MSD for one trajectory
    def compute_msd(self,trajectory):

        tau = trajectory['t'].copy()
        study_time = int(max(tau))

        tau = tau - tau.iloc[0]
        tau = tau[0:study_time]
        tau = pd.to_numeric(tau)
        shifts = np.floor(tau / self.timestep).astype(int)
        msds = []
        msds_std = []
        consecutive_zeros = 0  # Counter for consecutive zeros

        for i, shiftpos in enumerate(shifts):
            shifted_trajectory = trajectory[self.coords].shift(-shiftpos)
            shifted_trajectory = shifted_trajectory.interpolate()  # Fill in missing values by interpolation

            if shifted_trajectory.shape[0] >= self.min_num_MSD:  # Filter trajectories with fewer than x points
                diffs = (shifted_trajectory - trajectory[self.coords])/ forty_x_magn
                sqdist = np.square(diffs).sum(axis=1)
                msd = sqdist.mean()/ len(diffs)
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
            plt.plot(msd.index[:-1-self.remove_lasts_pts]*self.deltat/1000, msd.values[:-1-self.remove_lasts_pts]
                     , alpha=0.2)

        x = np.arange(len(msdcomposelist[:-1 - self.remove_lasts_pts])) * (self.deltat/1000)

        plt.plot(x, msdcomposelist[:-1-self.remove_lasts_pts], 'r', label='Mean value')
        plt.xlabel('Time (s)')
        plt.ylabel('Mean Square Displacement (MSD) in µm²')
        plt.legend()

    def multiple_plots(self,msddata,ax,label):
        x = np.arange(len(msddata))
        ax.plot(x[1:-1-self.remove_lasts_pts]*self.deltat/1000, msddata[1:-1-self.remove_lasts_pts],label=label)

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

# def remove_outliers(data_list, threshold=2):
#     cleaned_list = []
#     for data in data_list:
#         diff = np.diff(data)  # Calculate the differences between consecutive MSD values
#         relative_diff = np.abs(diff / data[:-1])  # Calculate the relative differences
#         mask = relative_diff < threshold  # Mask to filter out the outlier values
#         cleaned_data = data[:-1][mask]  # Keep only the non-outlier values
#         cleaned_list.append(cleaned_data)
#     return cleaned_list

