import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

""" at the end we should get the mean square displacement of the particle trajectories;
if multiple particles are present then assume the mean of all MSDs
"""
class MSDtraj:

    def __init__(self,dirname,filenum,coords,timestep,timeCMSD=1000):
        self.dirname = dirname
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
        tau = pd.to_numeric(tau)  # Conversion de la colonne tau en type numérique
        # print(tau)
        shifts = np.floor(tau / self.timestep).astype(int)
        msds = np.zeros(shifts.size)
        msds_std = np.zeros(shifts.size)

        for i, shiftpos in enumerate(shifts):
            shifted_trajectory = trajectory[self.coords].shift(-shiftpos)
            shifted_trajectory = shifted_trajectory.interpolate()  # Remplissage des valeurs manquantes par interpolation

            if shifted_trajectory.shape[0] >= 10:  # Filtrer les trajectoires avec moins de 10 points
                diffs = shifted_trajectory - trajectory[self.coords]
                sqdist = np.square(diffs).sum(axis=1)
                msds[i] = sqdist.mean()
                msds_std[i] = sqdist.std()

        msds = pd.DataFrame({'msds': msds, 'tau': tau, 'msds_std': msds_std})
        return msds, tau

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
        # stdcomposelist = np.mean(list(map(list,zip(*STDlist))),axis=1)
        # msdcomposelist = np.nanmean(np.array(MSDlist), axis=0)
        # stdcomposelist = np.nanmean(np.array(STDlist), axis=0)
        return msdcomposelist #, stdcomposelist #, tau_list