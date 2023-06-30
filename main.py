import matplotlib.pyplot as plt
from files_extraction import *
from MSDtraj import *


filename = r'D:\...' #exact location of your file, for example r'E:\...\my_file.csv

pathfile = r'S:\...' #path where you want to register your data (images + text files for MSD calculation)
name_file = r'\prefix of your file' #make sure you keep the "\" before the name you want to give to your files


##---------------------Image processing---------------------##

#Values of x_left, x_right, y_bottom, y_top have to be changed according to your other files, by default it will optimize the representation
Rep_traj_unchanged(filename,pathfile,x_left=None, x_right=None, y_bottom=None, y_top=None)
plt.savefig(pathfile+name_file+'_traj_unchanged.png')
Rep_same_origin(filename,x_left=None, x_right=None, y_bottom=None, y_top=None)
plt.savefig(pathfile+name_file+'_same_origin.png')
Distrib_direction_hist(filename)
plt.savefig(pathfile+name_file+'_hist.png')

##---------------------MSD calculation---------------------##
msd = MSDtraj(pathfile,['t','x','y'],50,0)   # MSDtraj(pathfile, [time, x_position, y_position],
                                            # timestep in ms, number of last points to remove from graphs if outliers)

msddata, MSDlist, taul = msd.main()  #First argument is used for slope_origin calculation

msd.slope_origin(msddata,10)    #Second argument is meant to adapt the number of points you want to take for linear regression

plt.show()




