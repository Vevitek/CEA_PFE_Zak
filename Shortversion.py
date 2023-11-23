from files_extraction import *
from MSDtraj import *

def process_data_im(filename,pathfile,name_file,min_frames,x_left, x_right, y_bottom, y_top):
    Rep_traj_unchanged(filename, pathfile, min_frames)
    plt.savefig(pathfile + name_file + '_traj_unchanged.png')
    Rep_same_origin(filename, min_frames, x_left, x_right, y_bottom, y_top)
    plt.savefig(pathfile + name_file + '_same_origin.png')
    Distrib_direction_hist(filename)
    plt.savefig(pathfile + name_file + '_hist.png')


def process_data_msd(pathfile,name_file,ax,label,deltaT=50):
    msd = MSDtraj(pathfile, ['t', 'x', 'y'], deltaT, 0)  # MSDtraj(pathfile, [time, x_position, y_position],
    # timestep in ms, number of last points to remove from graphs if outliers)

    msddata, MSDlist, taul = msd.main()
    plt.savefig(pathfile + name_file + '_MeanMSD.png')
    msd.multiple_plots(msddata, ax, label=label)
