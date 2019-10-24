from get_files_in_dir import get_files_in_dir as get_files
import model

def plot_data():
    files = []
    files = get_files('*', recursive=False)
    data_main = []
    
    for file in files:
        data = []        
        file = file.split("\\")[1]
        file_data = model.MazeDeserializer().load(filename=file, datatype='json')        
        stats_data = file_data.Stats.get_solutions()
        for stats in stats_data:
            data_row = []
            data_row.append(((file_data.width -1)//2, (file_data.height -1)//2))
            data_row.append(stats['algo'])
            data_row.append(len(stats['route']))
            data_row.append(stats['time'])
            data.append(data_row)
        data_main.append(data)    
    return data_main

print(plot_data())