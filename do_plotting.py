import glob
import matplotlib.pyplot as plt
import jsbeautifier
import json


def get_files_in_dir(fileformat: str, recursive: bool) -> list:
    path = "mazes/"
    files = [f for f in glob.glob(path + "*." + fileformat, recursive=recursive)]
    return files


# files = get_files_in_dir("*", False)

data = []
data.append([(5, 5), "dfs", 10, 0.22, 0.33, 0.24])
data.append([(10, 10), "dfs", 15, 0.32, 0.33, 0.24])
data.append([(15, 15), "dfs", 26, 0.12, 0.33, 0.24])
data.append([(20, 20), "dfs", 34, 0.16, 0.33, 0.24])
data.append([(25, 25), "dfs", 56, 0.33, 0.33, 0.24])
data.append([(5, 5), "astar", 10, 0.22, 0.33, 0.24])
data.append([(10, 10), "astar", 13, 0.32, 0.33, 0.24])
data.append([(15, 15), "astar", 21, 0.12, 0.33, 0.24])
data.append([(20, 20), "astar", 29, 0.16, 0.33, 0.24])
data.append([(25, 25), "astar", 40, 0.11, 0.33, 0.24])


def _label(size: tuple) -> str:
    return "{}x{}".format(size[0], size[1])


def prepare_data_for_plotting(data: list) -> dict:
    # data_point = [size, solver, steps, avg time, min time, max time]

    # labels = ['5x5', '10x10', '15x15', '20x20', '25x25', '30x30']
    # print('data\n',data)

    # labels = []
    # for data_point in data:
    #     if _label(data_point[0]) not in labels:
    #         labels.append(_label(data_point[0]))

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

    print(jsbeautifier.beautify(json.dumps(plotting_data)))
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


plotting_data = prepare_data_for_plotting(data)
# plot_steps = prepare_steps_plot(plotting_data)
plot_times = prepare_times_plot(plotting_data)

# plot_steps.show()
plot_times.show()
