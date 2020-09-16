# Displays the average value of the trials in the selected folder, with a shaded region for the standard deviation

from matplotlib import pyplot
import cldLib

folder, current_dir = cldLib.pick_folder()
data_dict = cldLib.generate_data_dict(folder, current_dir)
fig = pyplot.figure()
cldLib.plot_avg(data_dict["avg_x"], data_dict["avg_y"], data_dict["std_dev"], data_dict["max_x"], data_dict["max_y"], data_dict["min_y"], pyplot.axes())
fig.suptitle(data_dict["title"], ha="center", va="top")
#pyplot.savefig(current_dir + "std_dev_graph.png")
pyplot.show()
