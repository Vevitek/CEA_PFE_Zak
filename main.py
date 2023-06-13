import matplotlib.pyplot as plt
from files_extraction import *
from MSDtraj import *


filename = r'D:\...' #exact location of your file, for example r'E:\...\my_file.csv

pathfile = r'C:\...' #path where you want to register your data (images + text files for MSD calculation)
name_file = r'\prefix of your file' #make sure you keep the "\" before the name you want to give to your files


##---------------------Image processing---------------------##

Rep_traj_unchanged(filename,pathfile)
plt.savefig(pathfile+name_file+'_traj_unchanged.png')
Rep_same_origin(filename)
plt.savefig(pathfile+name_file+'_same_origin.png')
Distrib_direction_hist(filename)
plt.savefig(pathfile+name_file+'_hist.png')

##---------------------MSD calculation---------------------##
msd = MSDtraj(pathfile,130,['t','x','y'],1,60) # MSDtraj(pathfile, number of files you want to analyze, [time, x_position
                                                # y_position], timestep, total time analysis
msddata, MSDlist, taul = msd.main()

msd.slope_origin(msddata,10)

plt.show()




