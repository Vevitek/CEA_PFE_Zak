
from Shortversion import *

filename1 = r'S:\...' #exact location of your 1st file, for example r'E:\...\my_file1.csv
filename2 = r'S:\...' #exact location of your  2nd file, for example r'E:\...\my_file2.csv and so ib

pathfile1 = r'S:\...' #path where you want to register your data (images + text files for MSD calculation)
pathfile2 = r'S:\...' #path where you want to register your data (for MSD calculation)

name_file1 = r'\...' #make sure you keep the "\" before the name you want to give to your files
name_file2 = r'\...'


x_left = None   #Let None by default and choose the best values for visualization of axises
x_right = None
y_bottom = None
y_top = None

##---------------------Image processing---------------------##

min_frames = 70 #shortest length you want to remove (based on timeframes)

#Values of x_left, x_right, y_bottom, y_top have to be changed according to your other files, by default (None) it will
#optimize the representation for a single file
process_data_im(filename1,pathfile1,name_file1,min_frames,x_left, x_right, y_bottom, y_top)
process_data_im(filename2,pathfile2,name_file2,min_frames,x_left,x_right,y_bottom,y_top)

##---------------------MSD calculation---------------------##
deltat = 100 #time in ms between 2 frames

fig, ax1 = plt.subplots()
label1 = "H2O2 0 percent"
label2 = "H2O2 5 percent"

process_data_msd(pathfile1,name_file1,ax1,label1,deltat)
process_data_msd(pathfile2,name_file2,ax1,label2,deltat)

ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Mean Square Displacement (MSD) in pixels')
ax1.legend()

plt.show() #comment this line if you want to not display figures everytime you run




