import csv
import os
import math
import pickle
from matplotlib import pyplot

# Generates average values and standard deviations for a set of trials and returns it as three lists: avg_x, avg_y, and std_dev
def generate_avgs(data_list):
	# Average Data from each file in the chosen folder
	master_x = []
	master_y = []
	std_dev = []
	size = 0
	trials = len(data_list)
	# Set length of our x and y data lists for the standard deviation graph
	for data in data_list:
		if (len(data["x"]) > size):
			size = len(data["x"])
	for i in range(size):
		x_tot = 0.0
		y_tot = 0.0
		diff_tot = 0.0
		skip = 0
		# average the datapoints
		for data in data_list:
			try:
				x_tot += data["x"][i]
				y_tot += data["y"][i]
			except IndexError:
				skip += 1
		x_tot /= trials - skip
		y_tot /= trials - skip
		# find the std deviation from the average and add the points to our master lists
		for data in data_list:
			try:
				diff_tot += (data["y"][i] - y_tot) ** 2
			except IndexError:
				pass
		master_x.append(x_tot)
		master_y.append(y_tot)
		std_dev.append(math.sqrt(diff_tot/(trials - skip)))
	return master_x, master_y, std_dev

# Turns the data in a folder into a dictionary with the test parameters, axis limits, average values, and standard deviations
def generate_data_dict(folder, cur_dir):
	pickle_dict = pull_test_params(cur_dir.split("/")[-2])
	data, max_x, max_y, min_y = generate_data_list(folder, cur_dir)
	pickle_dict["data"] = data
	pickle_dict["max_x"] = max_x
	pickle_dict["max_y"] = max_y
	pickle_dict["min_y"] = min_y
	avg_x, avg_y, std_dev = generate_avgs(pickle_dict["data"])
	pickle_dict["avg_x"] = avg_x
	pickle_dict["avg_y"] = avg_y
	pickle_dict["std_dev"] = std_dev
	return pickle_dict

# Generates a list of dictionaries, each of which refers to the x and y axis of the data of one of the files in the given folder
# Inputs: folder(a folder from os.scandir) and cur_dir(the filepath of the folder as a string)
# Returns the list, the maximum x value, the maximum y value, the minimum y value
def generate_data_list(folder, cur_dir):
	max_x = 0.0
	max_y = 0.0
	min_y = 0.0
	data_lists = []
	for data in folder:
		if (data.name[-4:] == ".csv"):
			x, y = generate_plot_lists(cur_dir + data.name)
			data_lists.append({"x": x, "y": y})
			if (max(x) > max_x):
				max_x = max(x)
			if (max(y) > max_y):
				max_y = max(y)
			if (min(y) > min_y):
				min_y = min(y)
	return data_lists, max_x, max_y, min_y

# Generate lists of data for the x and y axes from a file for which the filename is given
# Returns x axis list, y axis list
def generate_plot_lists(filename):
	f = open(filename)
	reader = csv.reader(f)
	header_row = next(reader)
	header_2 = next(reader)
	x_inputs = []
	y_inputs = []
	for row in reader:
		x_inputs.append(float(row[1]))
		y_inputs.append(float(row[2]))
	f.close()
	return x_inputs, y_inputs

# Returns the title graph based on the parameters in its data dictionary
def make_title_from_params(data_dict):
	if data_dict["angle"] == 1:
		fab = data_dict["fab"].title() + " Programmed"
	else:
		fab = data_dict["fab"].title() + " Programmed at " + str(data_dict["angle"]) + " Degrees"
	title = fab + " with " + str(data_dict["dip_num"]) + " Dips\nActuated at " + str(data_dict["pressure"]) + " psi around a " + str(data_dict["diam"]) + " in Tube"
	data_dict["title"] = title
	return title

# Make a title for a graph based on a folder name with letters in it
def make_title_text(foldername):
	subtitle = foldername.split("_")[-4]
	notes = foldername.split("_")[-2]
	if (notes != "noNotes"):
		subtitle = subtitle + "\n" + notes
	title_index = 1
	while (title_index < len(subtitle)):
		if (subtitle[title_index].isupper() and subtitle[title_index - 1] != " "):
			subtitle = subtitle[:title_index] + " " + subtitle[title_index:]
			title_index += 1
		elif (subtitle[title_index:title_index + 2] == "mm" or (subtitle[title_index:title_index + 2] == "in" and subtitle[title_index - 1] in "1234567890")):
			subtitle = subtitle[:title_index + 2] + " " + subtitle[title_index + 2:]
			title_index += 2
		elif (subtitle[title_index] in "1234567890" and not(subtitle[title_index - 1] in "1234567890 \n")):
			subtitle = subtitle[:title_index] + " " + subtitle[title_index:]
			title_index += 1
		title_index += 1
	if (len(subtitle) > 40 or (not ("\n" in subtitle) and len(subtitle) > 20)):
		title_index = -1
		while (subtitle[title_index] != " "):
			title_index -= 1
		subtitle = subtitle[:title_index] + "\n" + subtitle[title_index + 1:]
	return subtitle

# Allow user to pick a folder from an inputted directory
# Returns the folder, the filepath of the folder as a string
def pick_folder():
	main_dir = input("Name of Directory: ") + "/" # get the desired folders in a list
	entries = os.scandir(main_dir)
	print(main_dir)
	data_folders = []
	for entry in entries:
		if (entry.name[-1] in "10"):
			data_folders.append(entry)
	
	for i in range(len(data_folders)):
		print("(",i,")",data_folders[i].name)
	data_num = int(input("Which number folder do you want? "))
	#print(data_num)
	
	current_dir = main_dir + data_folders[data_num].name + "/"
	print(current_dir)
	return os.scandir(current_dir), current_dir

# Saves data_dict as a .pkl file with name filename (filename should end with .pkl)
def pickle_data(filename, data_dict):
	with open(filename, "w+b") as f:
		pickle.dump(f, data_dict)

# Returns a dictionary with the data from a .pkl file (filename should end with .pkl)
def unpickle_data(filename):
	f = open(filename, "r+b")
	data = pickle.load(f)
	f.close()
	return data

# Plot a shaded standard deviation shaded graph based on x averages, y averages, and standard deviations
# Returns the axes with the plotted averages
def plot_avg(avg_x, avg_y, std_dev, max_x, max_y, min_y, ax):
	
	# set upper and lower bounds of the shaded region with the std deviation at each x
	lower = []
	upper = []
	for i in range(len(avg_x)):
		lower.append(avg_y[i] - std_dev[i])
		upper.append(avg_y[i] + std_dev[i])
	# plot the data and return the figure
	ax.plot(avg_x, lower, linewidth=0.5)
	ax.plot(avg_x, upper, linewidth=0.5)
	ax.fill_between(avg_x, upper, lower)
	ax.plot(avg_x, avg_y, linewidth=0.5)
	ax.axis([0, max_x * 1.1, min_y * 1.1, max_y * 1.1])
	ax.set_xlabel("Extension (mm)", fontsize=10)
	ax.set_ylabel("Pull Force (N)", fontsize=10)
	ax.tick_params(axis='both', which='minor', labelsize=10)
	ax.minorticks_on()

# returns a figure containing the plot of a plot of all the trials in data
def plot_trials(data, max_x, max_y, min_y, ax):
	for datum in data:
		ax.plot(datum["x"], datum["y"], linewidth=0.7)
	ax.axis([0, max_x * 1.1, min_y * 1.1, max_y * 1.1])
	ax.set_xlabel("Extension (mm)", fontsize=10)
	ax.set_ylabel("Pull Force (N)", fontsize=10)
	ax.tick_params(axis='both', which='minor', labelsize=10)
	ax.minorticks_on()

# Returns a dictionary based on a folder name without letters following the naming convention:
# 0: Date (key "date")
# 1: Pull test rod diameter (with a vestigial 1 at the beginning) (key "diam")
# 2: Pressure (psi) (key "pressure")
# 3: Number of Dip Coatings (key "dip_num")
# 4: Fabrication Angle (if "gravity programmed", 1 if "fiber programmed") (angle key: "angle", fabrication method key: "fab")
# 5: Sample Number (key "sample_num")
def pull_test_params(foldername):
	if (foldername.upper() != foldername.lower()):
		param_dict = {"title": make_title_text(foldername)}
	else:
		param_list = foldername.split("_")
		if param_list[4] == "1":
			fab = "fiber"
		else:
			fab = "gravity"
		param_dict = {
			"date": param_list[0],
			"diam": float(param_list[1][1:])/100.0,
			"pressure": int(param_list[2]),
			"dip_num": int(param_list[3]),
			"fab": fab,
			"angle": int(param_list[4]),
			"sample_num": int(param_list[5])
		}
		make_title_from_params(param_dict)
	return param_dict			
