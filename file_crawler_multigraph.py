# Makes and saves a PDF with graphs for all the tests in the selected directory

import os
from matplotlib import pyplot
from matplotlib import gridspec
import math
import cldLib

main_dir = input("Name of Directory: ") + "/"
entries = os.scandir(main_dir)

data_folders = []
for entry in entries:
	if (entry.name[-1] in "10"):
		data_folders.append(entry)
rows = (len(data_folders) + 1)// 2
cols = 2
fig, axs = pyplot.subplots(rows, cols, figsize = [cols * 4, rows * 4], gridspec_kw = {"wspace": 0.2, "hspace": 0.6})
#print("rows:", rows)
#print("cols:", cols)
graph_num = 0
for fldr in data_folders:
#fldr = data_folders[0]
	# Plot Data from each file in the current folder
	current_dir = main_dir + fldr.name + "/"
	data_dict = cldLib.generate_data_dict(os.scandir(current_dir), current_dir)
	current_axis = axs[graph_num % rows, graph_num // rows]
	cldLib.plot_trials(data_dict["data"], data_dict["max_x"], data_dict["max_y"], data_dict["min_y"], current_axis)
	current_axis.set_title(data_dict["title"])
	graph_num += 1
fig.suptitle(input("Name your set of graphs: "), va = "top", ha = "center", fontsize = 20)
pyplot.savefig(main_dir + main_dir[:-1] + "_graphs.pdf")
#pyplot.show()

		
