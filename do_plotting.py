from get_files_in_dir import get_files_in_dir as get_files
import model
import glob
import matplotlib.pyplot as plt
import jsbeautifier
import json
import os


# def get_files_in_dir(fileformat: str, recursive: bool) -> list:
#     path = "mazes/"
#     files = [f for f in glob.glob(path + "*." + fileformat, recursive=recursive)]
#     return files


def is_win() -> bool:
    """ Return True if OS is Windows """
    return True if os.name == "nt" else False


def create_plot_data():
    """Takes all files in our mazes data folder\n
    Return : [[width, height, 'solver', steps, avg. time, min time, max time]]"""
    files = get_files("*", recursive=False)
    data = []
    for file in files:
        if is_win():
            file = file.split("\\")[1]
        else:
            file = file.split("/")[1]
        file_data = model.MazeDeserializer().load(filename=file, datatype="json")
        stats_data = file_data.Stats.get_solutions()
        for stats in stats_data:
            algoritm = stats["algo"]
            if data == []:
                data.append(extract_data(algoritm, stats, file_data))
            if algoritm not in data[-1][2]:
                data.append(extract_data(algoritm, stats, file_data))

    return data


def extract_data(algo, stats, file_data):
    """Returns data for the specific algoritm"""
    data = []
    if algo == "dfs":
        data.append((file_data.width - 1) // 2)
        data.append((file_data.height - 1) // 2)
        data.append(algo)
        data.append(len(stats["route"]))
        data.append(file_data.Stats.time_avg(algo=algo))
        data.append(file_data.Stats.time_min(algo=algo))
        data.append(file_data.Stats.time_max(algo=algo))
        return data
    if algo == "astar":
        data.append((file_data.width - 1) // 2)
        data.append((file_data.height - 1) // 2)
        data.append(algo)
        data.append(len(stats["route"]))
        data.append(file_data.Stats.time_avg(algo=algo))
        data.append(file_data.Stats.time_min(algo=algo))
        data.append(file_data.Stats.time_max(algo=algo))
        return data
    return "Solver unknown"


def _label(size: tuple) -> str:
    return "{}x{}".format(size[0], size[1])


def prepare_data_for_plotting(data: list) -> dict:
    # data_point = [size, solver, steps, avg time, min time, max time]
    # labels = ['5x5', '10x10', '15x15', '20x20', '25x25', '30x30']

    data = sorted(data, key=lambda x: x[0][0])

    labels = [_label(data_point[0]) for data_point in data if data_point[1] == "dfs"]

    dfs_steps = [
        [data_point[0], data_point[2]] for data_point in data if data_point[1] == "dfs"
    ]
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

    # print(jsbeautifier.beautify(json.dumps(plotting_data, indent=4)))
    return plotting_data


# tutorial: https://towardsdatascience.com/matplotlib-tutorial-learn-basics-of-pythons-powerful-plotting-library-b5d1b8f67596


def prepare_steps_plot(plotting_data: dict) -> plt:

    plt.plot(plotting_data["labels"], plotting_data["dfs_steps"], label="dfs steps")
    plt.plot(plotting_data["labels"], plotting_data["astar_steps"], label="astar steps")

    plt.xlabel("maze sizes")
    plt.ylabel("time")

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
    plt.plot(
        plotting_data["labels"], plotting_data["dfs_min_time"], label="dfs min. time"
    )
    plt.plot(
        plotting_data["labels"],
        plotting_data["astar_min_time"],
        label="astar min. time",
    )
    plt.plot(
        plotting_data["labels"], plotting_data["dfs_max_time"], label="dfs max. time"
    )
    plt.plot(
        plotting_data["labels"],
        plotting_data["astar_max_time"],
        label="astar max. time",
    )

    plt.xlabel("maze sizes")
    plt.ylabel("steps")

    plt.title("Maze solutions by algorithm")

    plt.legend()

    # plt.show()
    return plt


def print_data(data):
    for row in data:
        print(row)


# data = []
# data.append([5, 5, "dfs", 10, 0.22, 0.33, 0.24])
# data.append([10, 10, "dfs", 15, 0.32, 0.33, 0.24])
# data.append([15, 15, "dfs", 26, 0.12, 0.33, 0.24])
# data.append([20, 20, "dfs", 34, 0.16, 0.33, 0.24])
# data.append([25, 25, "dfs", 56, 0.33, 0.33, 0.24])
# data.append([5, 5, "astar", 10, 0.22, 0.33, 0.24])
# data.append([10, 10, "astar", 13, 0.32, 0.33, 0.24])
# data.append([15, 15, "astar", 21, 0.12, 0.33, 0.24])
# data.append([20, 20, "astar", 29, 0.16, 0.33, 0.24])
# data.append([25, 25, "astar", 40, 0.11, 0.33, 0.24])


data = create_plot_data()
# print_data(data)

# plotting_data = prepare_data_for_plotting(data)

algos = list(set([d[2] for d in data]))

# find all maze sizes
sizes = list([[d[0], d[1]] for d in data])
# find unique mazes sizes
sizes = [list(y) for y in set([tuple(x) for x in sizes])]
# sort maze sizes by key = multiply width x height


def sort_data(data):
    """ Expects a list of maze stats data where\n
    index 0 is width and index 1 is height"""
    data.sort(key=lambda x: x[0] * x[1])
    return data


sizes = sort_data(sizes)


# build dict for sorting data
data_dict = {}
for a in algos:
    data_dict[a] = {}
    for s in sizes:
        data_dict[a].update(
            {"{}x{}".format(s[0], s[1]): {"steps": {}, "min": {}, "max": {}, "avg": {}}}
        )

# print(algos, sizes)
# print(data_dict)
# print(jsbeautifier.beautify(json.dumps(data_dict)))

dfs_data = sort_data([row for row in data if row[2] == "dfs"])
astar_data = sort_data([row for row in data if row[2] == "astar"])

# print_data(dfs_data)
# print_data(astar_data)
# print(sizes)

dfs_steps = {}
astar_steps = {}

dfs_avg = {}
dfs_min = {}
dfs_max = {}

astar_avg = {}
astar_min = {}
astar_max = {}

# data_point = [width, height, solver, steps, avg time, min time, max time]

for size in sizes:
    # dfs steps data
    step_dfs = [row[3] for row in dfs_data if [row[0], row[1]] == size]
    step_dfs_avg = sum(step_dfs) / len(step_dfs)
    dfs_steps.update({_label(size): step_dfs_avg})

    # astar steps data
    step_astar = [row[3] for row in astar_data if [row[0], row[1]] == size]
    step_astar_avg = sum(step_astar) / len(step_astar)
    astar_steps.update({_label(size): step_astar_avg})

    # dfs avg time data
    avg_dfs = [row[4] for row in dfs_data if [row[0], row[1]] == size]
    avg_dfs_avg = sum(avg_dfs) / len(avg_dfs)
    dfs_avg.update({_label(size): avg_dfs_avg})

    # astar avg time data
    avg_astar = [row[4] for row in astar_data if [row[0], row[1]] == size]
    avg_astar_avg = sum(avg_astar) / len(avg_astar)
    astar_avg.update({_label(size): avg_astar_avg})

print("steps data")
print(dfs_steps)
print(astar_steps)
print("avg time data")
print(dfs_avg)
print(astar_avg)


# print(plotting_data["dfs_steps"])

# plot_steps = prepare_steps_plot(plotting_data)
# plot_times = prepare_times_plot(plotting_data)

# plot_steps.show()
# plot_times.show()
