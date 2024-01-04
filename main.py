from Shortversion import *
from Velocity_data import *


#------------------If you don't need MSD part feel free to comment it-----------------------#
deltat = 40 #time in ms between 2 frames
forty_x_magn = 6.15 # px/µm if using 40x, divide by 2 for 20x

filename1 = r"S:\..." #exact location of your 1st file, for example r'E:\...\my_file1.csv'
filename2 = r"S:\..." #exact location of your  2nd file, for example r'E:\...\my_file2.csv' and so on
filename3 = r"S:\..."

vel_data1 = r"S:\..." #exact location of your velocity data file, for example r'E:\...\my_velocityfile1.csv'
vel_data2 = r"S:\..."
vel_data3 = r"S:\..."

pathfile1 = r"S:\..." #path where you want to register your first dataset
pathfile2 = r"S:\..." #path where you want to register your second dataset
pathfile3 = r"S:\..."


name_file1 = r'\...' #make sure you keep the "\" before the name you want to give to your files
name_file2 = r'\...'
name_file3 = r'\...'

x_left = None   #Let None by default and choose the best values for visualization of axises
x_right = None
y_bottom = None
y_top = None

##---------------------Image processing---------------------##

min_frames = 3 #shortest length you want to remove (based on timeframes)

#Values of x_left, x_right, y_bottom, y_top have to be changed according to your other files, by default (None) it will
#optimize the representation for a single file
process_data_im(filename1,pathfile1,name_file1,min_frames,x_left, x_right, y_bottom, y_top)
process_data_im(filename2,pathfile2,name_file2,min_frames,x_left,x_right,y_bottom,y_top)
process_data_im(filename3,pathfile3,name_file3,min_frames,x_left,x_right,y_bottom,y_top)

##---------------------MSD calculation---------------------##

min_num_MSD = 20 #only trajectories with more than min_num_MSD will be taken into account for MSD calculation
reg_value = 70 #number of values used for linear regression and diffusion coefficient



label1 = "SNP"
label2 = "Not SNP"
label3 = "Whatever"

fig, ax1 = plt.subplots()
process_data_msd(pathfile1,name_file1,ax1,label1,min_num_MSD,reg_value,deltat)
process_data_msd(pathfile2,name_file2,ax1,label2,min_num_MSD,reg_value,deltat)
process_data_msd(pathfile3,name_file3,ax1,label3,min_num_MSD,reg_value,deltat)

ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Mean Square Displacement (MSD) in pixels')
ax1.legend()

##---------------------VELOCITY analysis---------------------##

combined_func(vel_data1,pathfile1,namefile,forty_x_magn, deltat)
combined_func(vel_data2,pathfile2,namefile,forty_x_magn, deltat)
combined_func(vel_data3,pathfile3,namefile,forty_x_magn, deltat)



plt.show() #comment this line if you want to not display figures everytime you run




