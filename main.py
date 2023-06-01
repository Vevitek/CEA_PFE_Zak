import matplotlib.pyplot as plt
from files_extraction import *


# filename = "S:\Image_processing\Data\SiO2_track"
# filename = 'S:\Image_processing\Data\example_tracking'

filename = r'S:\Image_processing\mon_fichier.csv'

Rep_traj_unchanged(filename)
Rep_same_origin(filename)
Distrib_direction_hist(filename)


plt.show()



