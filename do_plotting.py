import glob
import matplotlib.pyplot as plt
import pandas as pd

def get_files_in_dir(fileformat: str, recursive: bool) -> list:
    path = "mazes/"
    files = [f for f in glob.glob(path + "*." + fileformat, recursive=recursive)]
    return files


files = get_files_in_dir("*", False)

data = []
data.append(["5x5", "dfs", 10, 0.22])
data.append(["5x5", "dfs", 10, 0.24])
data.append(["10x10", "dfs", 15, 0.32])
data.append(["10x10", "dfs", 15, 0.27])
data.append(["15x15", "dfs", 26, 0.12])
data.append(["15x15", "dfs", 26, 0.21])
data.append(["20x20", "dfs", 34, 0.16])
data.append(["20x20", "dfs", 34, 0.45])
data.append(["25x25", "dfs", 56, 0.33])
data.append(["25x25", "dfs", 56, 0.11])
data.append(["5x5", "astar", 10, 0.22])
data.append(["5x5", "astar", 10, 0.24])
data.append(["10x10", "astar", 10, 0.32])
data.append(["10x10", "astar", 10, 0.27])
data.append(["15x15", "astar", 10, 0.12])
data.append(["15x15", "astar", 10, 0.21])
data.append(["20x20", "astar", 10, 0.16])
data.append(["20x20", "astar", 10, 0.45])
data.append(["25x25", "astar", 10, 0.33])
data.append(["25x25", "astar", 10, 0.11])


def prepare_data_for_plotting(data: list):
    # data_point = ['maze size', 'algo', 'steps', 'time']

    # labels = ['5x5', '10x10', '15x15', '20x20', '25x25', '30x30']
    # print(data)

    data_astar = [data_point for data_point in data if data_point[1] == 'astar']

    # labels = list(set([data_point[0] for data_point in data]))
    # print("labels:", labels)


    # steps_dfs = [[data_point[0], data_point[2]] for data_point in data if data_point[1] == "dfs"]
    # steps_astar = [[data_point[0], data_point[2]] for data_point in data if data_point[1] == "astar"]

    # steps_dfs = []

    # times_dfs = [
    #     [data_point[0], data_point[3]] for data_point in data if data_point[1] == "dfs"
    # ]
    # times_astar = [
    #     [data_point[0], data_point[3]]
    #     for data_point in data
    #     if data_point[1] == "astar"
    # ]

    # print("steps dfs:", steps_dfs)
    # print("steps astar:", steps_astar)

    # print(times_dfs, times_astar)
    # steps_dfs = [3, 10, 23, 35, 56, 97]
    # steps_astar = [2, 9, 16, 27, 40, 60]

    # plt.plot(labels, steps_dfs, label='dfs')
    # plt.plot(labels, steps_astar, label='astar')

    # plt.xlabel('maze sizes')
    # plt.ylabel('steps')

    # plt.title("Maze solutions by algorithm")

    # plt.legend()

    # plt.show()
    # return plt


plot = prepare_data_for_plotting(data)
# plot.show()
