import matplotlib.pyplot as plt
from files_extraction import *


# filename = "S:\Image_processing\Data\SiO2_track"
# filename = 'S:\Image_processing\Data\example_tracking'

filename = r'S:\Image_processing\Vagisha Analysis\01062023\0%[H2O2]-entire track - track index.csv'

pathfile = r'S:\Image_processing\Vagisha Analysis\01062023'
name_file = r'\0%[H2O2]-entire track'

Rep_traj_unchanged(filename)
plt.savefig(pathfile+name_file+'_traj_unchanged.png')
Rep_same_origin(filename)
plt.savefig(pathfile+name_file+'_same_origin.png')
Distrib_direction_hist(filename)
plt.savefig(pathfile+name_file+'_hist.png')


plt.show()



