import matplotlib.pyplot as plt
from files_extraction import *
from MSDtraj import *
from Shortversion import *

filename1 = r'S:\Test_Vagisha\Vagisha Analysis\0H2O2-JP_1-3.5mBar_10FPS_35spots.csv' #exact location of your 1st file, for example r'E:\...\my_file1.csv
filename2 = r'S:\Test_Vagisha\Vagisha Analysis\5H2O2-JP_2-3mBar_10FPS_37spots.csv' #exact location of your  2nd file, for example r'E:\...\my_file2.csv and so ib

pathfile1 = r'S:\Test_Vagisha\Vagisha Analysis\0PC_H2O2' #path where you want to register your data (images + text files for MSD calculation)
pathfile2 = r'S:\Test_Vagisha\Vagisha Analysis\5PC_H2O2' #path where you want to register your data (for MSD calculation)

name_file1 = r'\0pc_H2O2' #make sure you keep the "\" before the name you want to give to your files
name_file2 = r'\5pc_H2O2'


x_left = None   #Let None by default and choose the best values for visualization of axises
x_right = None
y_bottom = None
y_top = None

##---------------------Image processing---------------------##

min_frames = 10 # number of shortest path you want to remove (based of timeframes)

#Values of x_left, x_right, y_bottom, y_top have to be changed according to your other files, by default (None) it will
#optimize the representation for a single file
process_data_im(filename1,pathfile1,name_file1,min_frames,x_left, x_right, y_bottom, y_top)
process_data_im(filename2,pathfile2,name_file2,min_frames,x_left,x_right,y_bottom,y_top)

##---------------------MSD calculation---------------------##

fig, ax1 = plt.subplots()
label1 = "H2O2 0 percent"
label2 = "H2O2 5 percent"

process_data_msd(pathfile1,ax1,label1)
process_data_msd(pathfile2,ax1,label2)

ax1.set_xlabel('Tau')
ax1.set_ylabel('MSD')
ax1.legend()

plt.show()




