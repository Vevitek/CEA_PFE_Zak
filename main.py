import matplotlib.pyplot as plt
from files_extraction import *


filename = r'S:\Image_processing\Vagisha Analysis\Vagisha_SNP\One_percent_total time_index.csv'

pathfile = r'S:\Image_processing\Vagisha Analysis\Vagisha_SNP'
name_file = r'\One_percent_SNP'

Rep_traj_unchanged(filename)
plt.savefig(pathfile+name_file+'_traj_unchanged.png')
Rep_same_origin(filename)
plt.savefig(pathfile+name_file+'_same_origin.png')
Distrib_direction_hist(filename)
plt.savefig(pathfile+name_file+'_hist.png')

# Analyse_diff_rate(filename)
# MSD_diff_rate(filename)

plt.show()



