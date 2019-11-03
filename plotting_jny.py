from get_files_in_dir import get_files_in_dir as get_files
import model
import os
# from decimal import Decimal


def is_win() -> bool:
    """ Return True if OS is Windows """
    return True if os.name == "nt" else False


def create_plot_data():
    """Takes all files in our mazes data folder\n
    Return : [[(width, height), 'solver', steps lengt, time]]"""
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
            data_temp = []
            data_temp.append(((file_data.width - 1) // 2, (file_data.height - 1) // 2))  # size
            data_temp.append(stats["algo"])
            data_temp.append(len(stats["steps"]))
            data_temp.append(stats["time"])
            data.append(data_temp)
    return data


def refine_plot_data(data):
    """Takes list of [(width, height), 'solver', steps lengt, time]
    Return : [[(width, height), 'solver', steps lengt, Avg. time, Min. time, Max. time]]"""
    data_list = []
    for row in data:
        if row[0:2] not in list(map(lambda x: x[0:2], data_list)):
            data_list.append(row)
            data_list[-1].append(row[3])
            data_list[-1].append(row[3])
        else:
            idx = list(map(lambda x: x[0:2], data_list)).index(row[0:2])

            # Update steps
            data_list[idx][2] = (data_list[idx][2] + row[2]) / 2

            # update avg time value
            data_list[idx][3] = (data_list[idx][3] + row[3]) / 2

            # update min time value
            if row[3] < data_list[idx][4]:
                data_list[idx][4] = row[3]

            # update max time value
            if row[3] > data_list[idx][5]:
                data_list[idx][5] = row[3]
    print(sorted(data_list))
    return sorted(data_list)


def get_plotting_data():
    """Return : [[(width, height), 'solver', steps lengt, Avg. time, Min. time, Max. time]]"""
    return refine_plot_data(create_plot_data())
