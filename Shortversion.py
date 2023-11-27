from files_extraction import *
from MSDtraj import *

def process_data_im(filename,pathfile,name_file,min_frames,x_left, x_right, y_bottom, y_top):
    fig, axes = plt.subplots(1, 3, figsize=(8, 5))
    Rep_traj_unchanged(filename, pathfile,name_file,axes[0], min_frames)
    Rep_same_origin(pathfile,name_file,filename,axes[1], min_frames, x_left, x_right, y_bottom, y_top)
    Distrib_direction_hist(pathfile,name_file,filename,fig)

    plt.tight_layout() # Ajuster la mise en page


def process_data_msd(pathfile,name_file,ax,label,min_num_MSD,deltaT=50):
    msd = MSDtraj(pathfile, ['t', 'x', 'y'], deltaT,min_num_MSD, 0)  # MSDtraj(pathfile, [time, x_position, y_position],
    # timestep in ms, number of last points to remove from graphs if outliers)

    msddata, MSDlist, taul = msd.main()
    plt.savefig(pathfile + name_file + '_MeanMSD.png')
    msd.multiple_plots(msddata, ax, label=label)
