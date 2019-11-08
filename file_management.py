"""
You should only be calling the functions\n
load and save, directly from this file.\n
All other functions are just help functions for these calls.
"""
from collections import OrderedDict
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


def _load_from_json(filename):
    """
    Load json file\n
    Returns: Maze object
    """
    if os.name == "nt":
        maze_dir = "mazes\\"
    else:
        maze_dir = "mazes/"
    filepath = maze_dir + filename
    try:
        if os.path.isfile(maze_dir + filename):
            with open(maze_dir + filename, "r") as file:
                data = json.load(file)  # returns dict
        return convert_from_dict_to_maze(data)  # returns Maze
    except IOError:
        raise Exception('Fail in loading file {filepath}'.format(filepath=filepath))


def _load_from_csv(filename):
    """
    Load csv files (Maze and stats)\n
    Returns: Maze object
    """
    if os.name == "nt":
        maze_dir = "mazes\\"
    else:
        maze_dir = "mazes/"
    filepath = maze_dir + filename
    data = {}
    try:
        with open(filepath, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data = row
    except IOError:
        print('Fail in loading file {filepath}'.format(filepath=filepath))
    finally:
        csv_file.close()
    data = dict(OrderedDict(data))
    filetype = filename.split('.')[1]
    filename = filename.split('.')[0]
    filepath = '{dir}{filename}-stats.{filetype}'.format(dir=maze_dir, filename=filename, filetype=filetype)
    try:
        with open(filepath, mode='r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data['stats'].append(dict(row['algo'], row['route'], row['steps'], row['time']))
    except IOError:
        print('Fail in loading file {filepath}'.format(filepath=filepath))
    finally:
        csv_file.close()

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
    if os.name == "nt":
        path = "mazes\\"
    else:
        path = "mazes/"
    filename = "{path}maze{number}_{width}x{height}.{fileformat}".format(
        path=path,
        number=_new_file_num(path),
        width=(data['width'] - 1) // 2,
        height=(data['height'] - 1) // 2,
        fileformat='json',
    )
    data = json.dumps(data)
    data = jsbeautifier.beautify(data)
    with open(filename, "w") as file:
        file.writelines(data)


def _save_as_csv(data):
    if os.name == "nt":
        path = "mazes\\"
    else:
        path = "mazes/"
    #  Saves filenumber to be able to use same on both files
    filenumber = _new_file_num(path)
    filename = "{path}maze{number}_{width}x{height}.{fileformat}".format(
        path=path,
        number=filenumber,
        width=(data['width'] - 1) // 2,
        height=(data['height'] - 1) // 2,
        fileformat='csv',
    )
    with open(filename, mode="w") as maze_file:
        fieldnames = []
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
    #  Save stats file
    filename = "{path}maze{number}_{width}x{height}-stats.{fileformat}".format(
        path=path,
        number=filenumber,
        width=(data['width'] - 1) // 2,
        height=(data['height'] - 1) // 2,
        fileformat='csv',
    )
    with open(filename, mode="w") as stats_file:
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
                    "algo": stat_data[row]["algo"],
                    "route": stat_data[row]["route"],
                    "steps": stat_data[row]["steps"],
                    "time": stat_data[row]["time"],
                }
            )
    stats_file.close()
