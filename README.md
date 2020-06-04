# cldLib
The cldLib module is a library of functions for processing and plotting data stored in csv files.
It uses the os module to move in between folders, the matplotlib.pyplot module to analyze and display data, and the pickle module to save the data in a more easily readable format.

cldLib.py is the file containing the module.  file_crawler_multigraph and average_grapher are sample scripts.

Methods:

generate_avgs(data_list)
	Generates average values and standard deviations for a set of trials and returns it as three lists: avg_x, avg_y, and std_dev

generate_data_dict(folder, cur_dir)
	Turns the data in a folder into a dictionary with the test parameters, axis limits, average values, and standard deviations

generate_data_list(folder, cur_dir)
	Generates a list of dictionaries, each of which refers to the x and y axis of the data of one of the files in the given folder
	Inputs: folder(a folder from os.scandir) and cur_dir(the filepath of the folder as a string)
	Returns the list, the maximum x value, the maximum y value, the minimum y value

generate_plot_lists(filename)
	Generate lists of data for the x and y axes from a file for which the filename is given
	Returns x axis list, y axis list

make_title_from_params(data_dict)
	Returns the title graph based on the parameters in its data dictionary

make_title_text(foldername)
	Make a title for a graph based on a folder name with letters in it

pick_folder()
	Allow user to pick a folder from an inputted directory
	Returns the folder, the filepath of the folder as a string

pickle_data(filename, data_dict)
	Saves data_dict as a .pkl file with name filename (filename should end with .pkl)

unpickle_data(filename)
	Returns a dictionary with the data from a .pkl file (filename should end with .pkl)

plot_avg(avg_x, avg_y, std_dev, max_x, max_y, min_y, ax)
	Plot a shaded standard deviation shaded graph based on x averages, y averages, and standard deviations on the specified axis

plot_trials(data, max_x, max_y, min_y, ax)
	Plots of all the trials in data onto the specified axis

pull_test_params(foldername)
	Returns a dictionary based on a folder name without letters following the naming convention:
	0: Date (key "date")
	1: Pull test rod diameter (with a vestigial 1 at the beginning) (key "diam")
	2: Pressure (psi) (key "pressure")
	3: Number of Dip Coatings (key "dip_num")
	4: Fabrication Angle (if "gravity programmed", 1 if "fiber programmed") (angle key: "angle", fabrication method key: "fab")
	5: Sample Number (key "sample_num")
