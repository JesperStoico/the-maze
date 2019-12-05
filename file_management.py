"""
You should only be calling the functions\n
load, save and get_files_in_dir, directly from this file.\n
All other functions are just help functions for these calls.
"""
import json
import csv
import os
import glob
import jsbeautifier

from model import convert_to_dict, Maze, Stats


def load(filename) -> Maze:
    """
    Open filename from disk\n
    Returns : Maze object
    """
    filetype = filename.split('.')[1]
    if filetype == "json":
        return _load_from_json(filename)
    if filetype == "csv":
        return _load_from_csv(filename)
    raise Exception('We do currently not support {filetype}, sorry'.format(filetype=filetype))


def save(maze, datatype) -> Maze:
    """save maze to disk in datatype format"""
    data = convert_to_dict(maze)
    if datatype == "json":
        return _save_as_json(data)
    if datatype == "csv":
        return _save_as_csv(data)
    raise Exception('We do currently not support {datatype}, sorry'.format(datatype=datatype))


def check_os_path():
    """Finds correct maze path"""
    if os.name == "nt":
        return "mazes\\"
    else:
        return "mazes/"


def _load_from_json(filename):
    """
    Load json file\n
    Returns: Maze object
    """
    filepath = check_os_path() + filename
    try:
        if os.path.isfile(filepath):
            with open(filepath, "r") as file:
                data = json.load(file)  # returns dict
        return convert_from_dict_to_maze(data)  # returns Maze
    except IOError:
        raise Exception('Fail in loading file {filepath}'.format(filepath=filepath))


def _load_from_csv(filename):
    """
    Load csv files (Maze and stats)\n
    Returns: Maze object
    """
    filepath = check_os_path() + filename
    data = {}
    try:
        with open(filepath) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data["maze"] = eval(row['maze'])
                data['width'] = int(row['width'])
                data["height"] = int(row['height'])
                data["start_coords"] = eval(row['start_coords'])
                data["end_coords"] = eval(row['end_coords'])
    except IOError:
        raise Exception('Fail in loading file {filepath}'.format(filepath=filepath))
    filetype = filename.split('.')[1]
    filename = filepath.split('.')[0]
    filepath = '{filename}-stats.{filetype}'.format(filename=filename, filetype=filetype)
    data['stats'] = []
    try:
        with open(filepath, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                stat_data = {}
                stat_data['algo'] = str(row['algo'])
                stat_data['route'] = eval(row['route'])
                stat_data['steps'] = eval(row['steps'])
                stat_data['time'] = float(row['time'])
                data['stats'].append(stat_data)
    except IOError:
        raise Exception('Fail in loading file {filepath}'.format(filepath=filepath))
    return convert_from_dict_to_maze(data)


def convert_from_dict_to_maze(data) -> Maze:
    """
    Convert dict data to maze object\n
    Returns: Maze object
    """
    maze = Maze(
        data["maze"],
        data["width"],
        data["height"],
        data["start_coords"],
        data["end_coords"],
    )
    if "stats" in data:  # if maze has stats, add Stats() object
        maze.Stats = Stats()
        for stat in data["stats"]:
            maze.Stats.solutions.append(stat)
    return maze


def _new_file_num(path: str) -> int:
    path = path
    # returns a list of files in mazes folder
    files = [f for f in glob.glob(path + "*.*", recursive=False)]
    # lambda function splits the files string down to just the number
    if os.name == "nt":
        numbers = list(map(lambda x: x.split("_")[0].split("\\maze")[1], files))
    else:
        numbers = list(map(lambda x: x.split("_")[0].split("/maze")[1], files))
    if numbers:
        # find the highest number in the list
        highest_num = max(int(num) for num in numbers)
    else:
        highest_num = 0
    new_file_num = highest_num + 1
    return new_file_num


def _save_as_json(data):
    path = check_os_path()
    filepath = "{path}maze{number}_{width}x{height}.{fileformat}".format(
        path=path,
        number=_new_file_num(path),
        width=(data['width'] - 1) // 2,
        height=(data['height'] - 1) // 2,
        fileformat='json',
    )
    data = json.dumps(data)
    data = jsbeautifier.beautify(data)
    try:
        with open(filepath, "w") as file:
            file.writelines(data)
    except IOError:
        raise Exception('Cannot save file, {filepath}'.format(filepath=filepath))


def _save_as_csv(data):
    #  Saves filenumber to be able to use same on both files
    path = check_os_path()
    filenumber = _new_file_num(path)
    filepath = "{path}maze{number}_{width}x{height}.{fileformat}".format(
        path=path,
        number=filenumber,
        width=(data['width'] - 1) // 2,
        height=(data['height'] - 1) // 2,
        fileformat='csv',
    )
    try:
        with open(filepath, mode="w") as maze_file:
            writer = csv.DictWriter(maze_file, fieldnames=[
                "width",
                "height",
                "start_coords",
                "end_coords",
                "maze"
            ])
            writer.writeheader()
            writer.writerow(
                {
                    "width": data["width"],
                    "height": data["height"],
                    "start_coords": data["start_coords"],
                    "end_coords": data["end_coords"],
                    "maze": data["maze"],
                }
            )
        maze_file.close()
    except IOError:
        raise Exception('Cannot save file, {filepath}'.format(filepath=filepath))
    #  Save stats file
    filepath = "{path}maze{number}_{width}x{height}-stats.{fileformat}".format(
        path=path,
        number=filenumber,
        width=(data['width'] - 1) // 2,
        height=(data['height'] - 1) // 2,
        fileformat='csv',
    )
    try:
        with open(filepath, mode="w") as stats_file:
            writer = csv.DictWriter(stats_file, fieldnames=[
                "algo",
                "route",
                "steps",
                "time"
            ])
            writer.writeheader()
            for row in data['stats']:
                writer.writerow(
                    {
                        "algo": row["algo"],
                        "route": row["route"],
                        "steps": row["steps"],
                        "time": row["time"],
                    }
                )
        stats_file.close()
    except IOError:
        raise Exception('Cannot save file, {filepath}'.format(filepath=filepath))


def get_files_in_dir(fileformat: str) -> list:
    """Returns a list of the files in the mazes dir"""
    files = [f for f in glob.glob("mazes/" + "*." + fileformat)]
    files = list(filter(lambda file: "-stats" not in file, files))
    if os.name == "nt":
        files = list(map(lambda x: x.split("mazes\\")[1], files))
    else:
        files = list(map(lambda x: x.split("mazes/")[1], files))
    return files
