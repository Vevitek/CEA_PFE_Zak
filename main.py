import matplotlib.pyplot as plt
from files_extraction import *
from MSDtraj import *


filename1 = r'S:\Test_Vagisha\Vagisha Analysis\Vagisha_SNP\Zero_percent_total time_index.csv' #exact location of your 1st file, for example r'E:\...\my_file1.csv
filename2 = r'S:\Test_Vagisha\Vagisha Analysis\Vagisha_SNP\Five_percent_entire track_index.csv' #exact location of your  2nd file, for example r'E:\...\my_file2.csv and so ib

pathfile1 = r'C:\Users\za274317\Downloads\Test_Vagisha\First dataset' #path where you want to register your data (images + text files for MSD calculation)
pathfile2 = r'C:\Users\za274317\Downloads\Test_Vagisha\Second dataset' #path where you want to register your data (for MSD calculation)

name_file = r'\love' #make sure you keep the "\" before the name you want to give to your files

x_left = -80
x_right = 80
y_bottom = -80
y_top = 60

##---------------------Image processing---------------------##

min_frames = 150 # number of shortest path you want to remove (based of timeframes)

#Values of x_left, x_right, y_bottom, y_top have to be changed according to your other files, by default it will optimize the representation
Rep_traj_unchanged(filename1,pathfile1,min_frames)
plt.savefig(pathfile1+name_file+'_traj_unchanged.png')
Rep_same_origin(filename1,min_frames,x_left, x_right, y_bottom, y_top)
plt.savefig(pathfile1+name_file+'_same_origin.png')
Distrib_direction_hist(filename1)
plt.savefig(pathfile1+name_file+'_hist.png')

Rep_traj_unchanged(filename2,pathfile2,min_frames)
plt.savefig(pathfile1+name_file+'_traj_unchanged.png')
Rep_same_origin(filename2,min_frames,x_left, x_right, y_bottom, y_top)
plt.savefig(pathfile2+name_file+'_same_origin.png')
Distrib_direction_hist(filename2)
plt.savefig(pathfile2+name_file+'_hist.png')

##---------------------MSD calculation---------------------##

fig, ax1 = plt.subplots()

msd1 = MSDtraj(pathfile1,['t','x','y'],50,0)   # MSDtraj(pathfile, [time, x_position, y_position],
                                            # timestep in ms, number of last points to remove from graphs if outliers)

msddata1, MSDlist, taul = msd1.main()
msd1.multiple_plots(msddata1,ax1,label="0 percent")

msd2 = MSDtraj(pathfile2,['t','x','y'],50,0)
msddata2, MSDlist, taul = msd2.main()
msd2.multiple_plots(msddata2,ax1,label="5 percent")

ax1.set_xlabel('Tau')
ax1.set_ylabel('MSD')
ax1.legend()

plt.show()




