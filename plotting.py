from get_files_in_dir import get_files_in_dir as get_files
import model
import os
from decimal import Decimal


def is_win() -> bool:
    """ Return True if OS is Windows """
    return True if os.name == "nt" else False


def create_plot_data():
    """Takes all files in our mazes data folder\n
    Return : [[(width, height), 'solver', steps, avg. time, min time, max time]]"""
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
            if algoritm not in data[-1][1]:
                data.append(extract_data(algoritm, stats, file_data))

    data_list = []
    for row in data:
        if row[0:2] not in list(map(lambda x: x[0:2], data_list)):
            data_list.append(row)
        else:
            idx = list(map(lambda x: x[0:2], data_list)).index(row[0:2])
            # update min time value
            if row[4] < data_list[idx][4]:
                data_list[idx][4] = row[4]

            # update max time value
            if row[5] > data_list[idx][5]:
                data_list[idx][5] = row[5]

            # update avg time value
            data_list[idx][3] = (data_list[idx][3] + row[3]) / 2

            # Update steps
            data_list[idx][2] = (data_list[idx][2] + row[2]) / 2

    print(sorted(data_list))
    return sorted(data_list)


def extract_data(algo, stats, file_data):
    """Returns data for the specific algoritm"""
    data = []

    data.append(((file_data.width - 1) // 2, (file_data.height - 1) // 2))
    data.append(algo)
    data.append(len(stats["steps"]))
    data.append(file_data.Stats.time_avg(algo=algo))
    data.append(file_data.Stats.time_min(algo=algo))
    data.append(file_data.Stats.time_max(algo=algo))
    return data
