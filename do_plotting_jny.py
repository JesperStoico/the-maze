from get_files_in_dir import get_files_in_dir as get_files
import model
import glob
import matplotlib.pyplot as plt
import jsbeautifier
import json
import os
import plotting


def is_win() -> bool:
    """ Return True if OS is Windows """
    return True if os.name == "nt" else False


def _label(size: tuple) -> str:
    return "{}x{}".format(size[0], size[1])


def prepare_data_for_plotting(data: list) -> dict:
    # data_point = [size, solver, steps, avg time, min time, max time]
    # labels = ['5x5', '10x10', '15x15', '20x20', '25x25', '30x30']

    labels = [_label(data_point[0]) for data_point in data if data_point[1] == "dfs"]

    dfs_steps = [data_point[2] for data_point in data if data_point[1] == "dfs"]
    astar_steps = [data_point[2] for data_point in data if data_point[1] == "astar"]

    dfs_avg_time = [data_point[3] for data_point in data if data_point[1] == "dfs"]
    astar_avg_time = [data_point[3] for data_point in data if data_point[1] == "astar"]

    dfs_min_time = [data_point[4] for data_point in data if data_point[1] == "dfs"]
    astar_min_time = [data_point[4] for data_point in data if data_point[1] == "astar"]

    dfs_max_time = [data_point[5] for data_point in data if data_point[1] == "dfs"]
    astar_max_time = [data_point[5] for data_point in data if data_point[1] == "astar"]

    plotting_data = {}
    plotting_data["labels"] = labels
    plotting_data["dfs_steps"] = dfs_steps
    plotting_data["astar_steps"] = astar_steps
    plotting_data["dfs_avg_time"] = dfs_avg_time
    plotting_data["astar_avg_time"] = astar_avg_time
    plotting_data["dfs_min_time"] = dfs_min_time
    plotting_data["astar_min_time"] = astar_min_time
    plotting_data["dfs_max_time"] = dfs_max_time
    plotting_data["astar_max_time"] = astar_max_time

    return plotting_data


# tutorial: https://towardsdatascience.com/matplotlib-tutorial-learn-basics-of-pythons-powerful-plotting-library-b5d1b8f67596


def prepare_steps_plot(plotting_data: dict) -> plt:

    plt.plot(plotting_data["labels"], plotting_data["dfs_steps"], label="dfs steps")
    plt.plot(plotting_data["labels"], plotting_data["astar_steps"], label="astar steps")

    plt.xlabel("maze sizes")
    plt.ylabel("steps")

    plt.title("Maze solutions by algorithm")

    plt.legend()

    # plt.show()
    return plt


def prepare_times_plot(plotting_data: dict) -> plt:
    plt.plot(
        plotting_data["labels"], plotting_data["dfs_avg_time"], label="dfs avg. time"
    )
    plt.plot(
        plotting_data["labels"],
        plotting_data["astar_avg_time"],
        label="astar avg. time",
    )

    plt.xlabel("maze sizes")
    plt.ylabel("time")

    plt.title("Maze solutions by algorithm")

    plt.legend()

    return plt


def print_data(data):
    for row in data:
        print(row)


data = plotting.get_plotting_data()
plotting_data = prepare_data_for_plotting(data)

plot_steps = prepare_steps_plot(plotting_data)
plot_steps.show()


#plot_times = prepare_times_plot(plotting_data)
#plot_times.show()
