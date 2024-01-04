import matplotlib.pyplot as plt

from files_extraction import *

def Avg_speed(filename,pathfile,namefile,forty_x_magn, deltat):
    vel_data = Read_data(filename)
    vel_data["TRACK_MEAN_SPEED"] = vel_data["TRACK_MEAN_SPEED"]*forty_x_magn/deltat
    vel_data = vel_data.sort_values(["TRACK_MEAN_SPEED"], ascending=True).reset_index(drop=True)

    plt.hist(vel_data["TRACK_MEAN_SPEED"],
             edgecolor='black', alpha=0.7)

    plt.xlabel('Mean speed (µm/ms)')
    plt.ylabel('Frequency')

    # Affichage de l'histogramme
    plt.savefig(pathfile + namefile + "_AVG_speed")
    plt.close()

def Total_dist_traveled(filename,pathfile,namefile,forty_x_magn, deltat):
    vel_data = Read_data(filename)
    vel_data["TOTAL_DISTANCE_TRAVELED"] = vel_data["TOTAL_DISTANCE_TRAVELED"] * forty_x_magn / deltat
    vel_data = vel_data.sort_values(["TOTAL_DISTANCE_TRAVELED"], ascending=True).reset_index(drop=True)

    plt.hist(vel_data["TOTAL_DISTANCE_TRAVELED"],
             bins=range(int(min(vel_data["TOTAL_DISTANCE_TRAVELED"])), int(max(vel_data["TOTAL_DISTANCE_TRAVELED"])),10),
             edgecolor='black', alpha=0.7)

    plt.xlabel('Total distance traveled (µm)')
    plt.ylabel('Frequency')

    # Affichage de l'histogramme
    plt.savefig(pathfile + namefile + "_Total_dist")
    plt.close()

def conf_ratio(filename,pathfile,namefile,forty_x_magn, deltat):
    vel_data = Read_data(filename)
    vel_data = vel_data.sort_values(["CONFINEMENT_RATIO"], ascending=True).reset_index(drop=True)

    plt.hist(vel_data["CONFINEMENT_RATIO"],
             edgecolor='black', alpha=0.7)

    plt.xlabel('Confinement ratio')
    plt.ylabel('Frequency')

    # Affichage de l'histogramme
    plt.savefig(pathfile + namefile + "_Conf_ratio")
    plt.close()

def MEAN_DIRECTIONAL_CHANGE_RATE(filename,pathfile,namefile,forty_x_magn, deltat):
    vel_data = Read_data(filename)

    vel_data["MEAN_DIRECTIONAL_CHANGE_RATE"] = vel_data["MEAN_DIRECTIONAL_CHANGE_RATE"] * forty_x_magn / deltat
    vel_data = vel_data.sort_values(["MEAN_DIRECTIONAL_CHANGE_RATE"], ascending=True).reset_index(drop=True)

    plt.hist(vel_data["MEAN_DIRECTIONAL_CHANGE_RATE"],
             edgecolor='black', alpha=0.7)

    plt.xlabel('Mean directional change rate (µm/ms)')
    plt.ylabel('Frequency')

    # Affichage de l'histogramme
    plt.savefig(pathfile + namefile + "_Mean_direct_change")
    plt.close()

def combined_func(filename,pathfile,namefile,forty_x_magn, deltat):
    Avg_speed(filename,pathfile,namefile,forty_x_magn, deltat)
    Total_dist_traveled(filename,pathfile,namefile,forty_x_magn, deltat)
    conf_ratio(filename,pathfile,namefile,forty_x_magn, deltat)
    MEAN_DIRECTIONAL_CHANGE_RATE(filename,pathfile,namefile,forty_x_magn, deltat)



filename = r"S:\Mails\Vagisha\Velocity_data\5-iso-track-s.csv"
pathfile = r"S:\Mails\Vagisha\Letruc"
namefile = r"\lemachin"
forty_x_magn = 6.15
deltat = 40
combined_func(filename,pathfile,namefile,forty_x_magn, deltat)