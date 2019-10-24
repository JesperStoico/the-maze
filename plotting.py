from get_files_in_dir import get_files_in_dir as get_files
import model


def create_plot_data():
    """Takes all files in our mazes data folder\n
    Return : [[(width, height), 'solver', steps, avg. time, min time, max time]]"""
    files = get_files('*', recursive=False)
    data = []
    for file in files:
        file = file.split("\\")[1]
        file_data = model.MazeDeserializer().load(filename=file, datatype='json')
        stats_data = file_data.Stats.get_solutions()
        for stats in stats_data:
            algoritm = stats['algo']
            if data == []:
                data.append(extract_data(algoritm, stats, file_data))
            if algoritm not in data[-1][1]:
                data.append(extract_data(algoritm, stats, file_data))
    return data


def extract_data(algo, stats, file_data):
    """Returns data for the specific algoritm"""
    data = []
    if algo == 'dfs':
        data.append(((file_data.width - 1) // 2, (file_data.height -1) // 2))
        data.append(algo)
        data.append(len(stats['route']))
        data.append(file_data.Stats.time_avg(algo=algo))
        data.append(file_data.Stats.time_min(algo=algo))
        data.append(file_data.Stats.time_max(algo=algo))
        return data
    if algo == 'astar':
        data.append(((file_data.width - 1) // 2, (file_data.height -1) // 2))
        data.append(algo)
        data.append(len(stats['route']))
        data.append(file_data.Stats.time_avg(algo=algo))
        data.append(file_data.Stats.time_min(algo=algo))
        data.append(file_data.Stats.time_max(algo=algo))
        return data
    return 'Solver unknown'
