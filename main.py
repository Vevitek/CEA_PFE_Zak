deltat = 90 #time in ms between 2 frames
forty_x_magn = 6.67 # px/µm if using 40x, divide by 2 for 20x


# For MSD limits modification go in files_extraction.py and change first global parameters defined as None

from Shortversion import *
from Velocity_data import *

filename1 = r"C:\Users\za274317\Downloads\For Zak\snp\0s_snp.csv" #exact location of your 1st file, for example r'E:\...\my_file1.csv'
filename2 = r"C:\Users\za274317\Downloads\For Zak\snp\5s_snp.csv"#exact location of your  2nd file, for example r'E:\...\my_file2.csv' and so on
filename3 = r"C:\Users\za274317\Downloads\For Zak\snp\10s_snp.csv"
# filename4 = r"C:\Users\za274317\Downloads\For Zak\jp\final-10s_jp.csv"

vel_data1 = r"N:\..." #exact location of your velocity data file, for example r'E:\...\my_velocityfile1.csv'
vel_data2 = r"N:\..."
vel_data3 = r"N:\..."

pathfile1 = r"C:\Users\za274317\Downloads\For Zak\Nouveau départ\0pc" #path where you want to register your first dataset
pathfile2 = r"C:\Users\za274317\Downloads\For Zak\Nouveau départ\5pc" #path where you want to register your second dataset
pathfile3 = r"C:\Users\za274317\Downloads\For Zak\Nouveau départ\10pc"
# pathfile4 = r"C:\Users\za274317\Downloads\For Zak\Nouveau départ\10pc_bis"

name_file1 = r'\0pc' #make sure you keep the "\" before the name you want to give to your files
name_file2 = r'\5pc'
name_file3 = r'\10pc'
# name_file4 = r'\10pc_bis'

##---------------------Image processing---------------------##

x_left = None   #Let None by default and choose the best values for visualization of axises
x_right = None
y_bottom = None
y_top = None
min_frames = 3 #shortest length you want to remove (based on timeframes)

#Values of x_left, x_right, y_bottom, y_top have to be changed according to your other files, by default (None) it will
# optimize the representation for a single file
process_data_im(filename1,pathfile1,name_file1,min_frames,x_left, x_right, y_bottom, y_top)
process_data_im(filename2,pathfile2,name_file2,min_frames,x_left,x_right,y_bottom,y_top)
process_data_im(filename3,pathfile3,name_file3,min_frames,x_left,x_right,y_bottom,y_top)
# process_data_im(filename4,pathfile4,name_file4,min_frames,x_left,x_right,y_bottom,y_top)
# plt.close('all')


##---------------------VELOCITY analysis---------------------##

#Leave None for default values then adjust by yourself

bins_avg_speed = None   #Has to be an integer e.g: 10 | 40 | 46
range_avg_speed = None  #Has to be a tuple e.g: (0,6) | (1 , 2.3)

bins_total_dist = None
range_total_dist = None

bins_conf_ratio = None
range_conf_ratio = None

bins_direc_CR = None
range_direc_CR = None

bins = [bins_avg_speed,bins_total_dist,bins_conf_ratio,bins_direc_CR]
range = [range_avg_speed,range_total_dist,range_conf_ratio,range_direc_CR]


# fig2, ax2 = plt.subplots()
# combined_func(vel_data1,pathfile1,name_file1,forty_x_magn, deltat, bins, range)
# combined_func(vel_data2,pathfile2,name_file2,forty_x_magn, deltat, bins, range)
# combined_func(vel_data3,pathfile3,name_file3,forty_x_magn, deltat, bins, range)


# ##---------------------MSD calculation---------------------##

min_num_MSD = 40 #only trajectories with more than min_num_MSD will be taken into account for MSD calculation
reg_value = 7 #number of values used for linear regression and diffusion coefficient
max_el_msd = None


label1 = "0pc"
label2 = "5pc"
label3 = "10pc"
label4 = "10pc_bis"

fig, ax1 = plt.subplots()
msdcomposelist1,  intercept1, slope1, x1 = process_data_msd(pathfile1,name_file1,ax1,label1,min_num_MSD,reg_value,deltat,max_el_msd)
msdcomposelist2,  intercept2, slope2, x2 = process_data_msd(pathfile2,name_file2,ax1,label2,min_num_MSD,reg_value,deltat,max_el_msd)
msdcomposelist3,  intercept3, slope3, x3 = process_data_msd(pathfile3,name_file3,ax1,label3,min_num_MSD,reg_value,deltat,max_el_msd)
# msdcomposelist4,  intercept4, slope4, x4 = process_data_msd(pathfile4,name_file4,ax1,label4,min_num_MSD,reg_value,deltat,max_el_msd)


msdcomposelist = [msdcomposelist1,msdcomposelist2,msdcomposelist3] #,msdcomposelist4
intercepts = [intercept1,intercept2,intercept3] #,intercept4
slopes = [slope1,slope2,slope3] #,slope4
labels = [label1,label2,label3] #,label4

MSD_superimposition(msdcomposelist,pathfile1,intercepts,slopes,labels,deltat)
