"""
You should only be calling the functions\n
get_step_plot and get_time_plot, directly from this file.\n
All other functions are just help functions for these calls.
"""
from matplotlib import pyplot as plt

from file_management import get_files_in_dir, load


def get_stats_data():
    """Takes all files in our mazes data folder\n
    Return : [[(width, height), 'solver', steps, time]]"""
    files = get_files_in_dir("*")
    data = []
    for file in files:
        file_data = load(filename=file)
        stats_data = file_data.Stats.get_solutions()
        for stats in stats_data:
            temp_data = []
            temp_data.append(((file_data.width - 1) // 2, (file_data.height - 1) // 2))
            temp_data.append(stats["algo"])
            temp_data.append(len(stats["steps"]))
            temp_data.append(stats["time"])
            data.append(temp_data)
    return data


def merge_data_for_plotting(data):
    """Take in a list of lists : [[(width, height), 'solver', steps, time]]\n
    Returns : [[(width, height), 'solver', steps lengt, Avg. time, Min. time, Max. time]]\n
    1 list pr solver"""
    data_list = []
    for row in data:
        if row[0:2] not in list(map(lambda x: x[0:2], data_list)):
            data_list.append(row)
            data_list[-1].append(row[3])
            data_list[-1].append(row[3])
        else:
            idx = list(map(lambda x: x[0:2], data_list)).index(row[0:2])
            # update min time value
            if row[3] < data_list[idx][4]:
                data_list[idx][4] = row[3]

            # update max time value
            if row[3] > data_list[idx][5]:
                data_list[idx][5] = row[3]

            # update avg time value
            data_list[idx][3] = (data_list[idx][3] + row[3]) / 2

            # Update steps
            data_list[idx][2] = (data_list[idx][2] + row[2]) / 2
    return sorted(data_list)


def prepare_data_for_plotting(data: list) -> dict:
    """Takes in : [[(width, height), 'solver', steps lengt, Avg. time, Min. time, Max. time]]\n
    returns {labels, "dfs_steps", "astar_steps",\n
    "dfs_avg_time", "astar_avg_time",\n
    "dfs_min_time", "astar_min_time",\n
    "dfs_max_time", "astar_max_time"}"""
    # data_point = [size, solver, steps, avg time, min time, max time]
    # labels = ['5x5', '10x10', '15x15', '20x20', '25x25', '30x30']

    def _label(size: tuple) -> str:
        return "{}x{}".format(size[0], size[1])

    labels = set([_label(data_point[0]) for data_point in data])
    labels = sorted(set(labels), key=lambda x: int(x.split("x")[0]) * int(x.split("x")[1]))

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


def prepare_steps_plot(plotting_data: dict) -> plt:
    plt.plot(plotting_data["labels"], plotting_data["dfs_steps"], label="dfs steps")
    plt.plot(plotting_data["labels"], plotting_data["astar_steps"], label="astar steps")
    plt.xlabel("maze sizes")
    plt.ylabel("steps")
    plt.title("Maze solutions by algorithm")
    plt.legend()
    return plt


def prepare_times_plot(plotting_data: dict) -> plt:
    plt.plot(plotting_data["labels"], plotting_data["dfs_avg_time"], label="dfs avg. time")
    plt.plot(plotting_data["labels"], plotting_data["astar_avg_time"], label="astar avg. time",)
    plt.title("Maze solutions by algorithm")
    plt.legend()
    return plt


def get_step_plot():
    data = get_stats_data()
    merge_data = merge_data_for_plotting(data)
    preped_data = prepare_data_for_plotting(merge_data)
    plot = prepare_steps_plot(preped_data)
    return plot


def get_time_plot():
    data = get_stats_data()
    merge_data = merge_data_for_plotting(data)
    preped_data = prepare_data_for_plotting(merge_data)
    plot = prepare_times_plot(preped_data)
    return plot
