This code is meant for analyzing particles after tracking using Trackmate on Fiji (ImageJ)

Once tracking is done on Trackmate, you have to export data to a .csv file. By copying the exact path into the main.py
you can process by running code. Read comments on the main.py file for more precise explanation.

'Rep_traj_unchanged()' will represent your trajectories as they appeared during tracking

'Rep_same_origin()' will represent your trajectories with a common starting point

'Distrib_direction_hist()' will represent the distribution of the angles of trajectories using a circular histogram. Be 
careful, depending on your data it may not be suitable. Only the first and last positions of tracking are taken into account