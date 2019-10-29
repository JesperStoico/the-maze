"""
You should only be calling the functions\n
load and save, directly from this file.\n
All other functions are just help functions for these calls.
"""
from model import convert_to_dict


def load(filename, datatype) -> Maze:
    """open filename from disk - must provide datatype"""
    loader = _get_loader(datatype)
    return loader(filename)  # returns maze


def _get_loader(datatype):
    """returns loader method based on datatype"""
    if datatype == "json":
        return _load_from_json
    elif datatype == "csv":
        return _load_from_csv
    else:
        raise Exception('We do currently not support {datatype}, sorry'.format(datatype=datatype))


def _load_from_json(filename):
    """
    Load json file\n
    returns: Maze object
    """
    if os.name == "nt":
        maze_dir = "mazes\\"
    else:
        maze_dir = "mazes/"

    if os.path.isfile(maze_dir + filename):
        with open(maze_dir + filename, "r") as file:
            data = json.load(file)  # returns dict

        return convert_data(data, datatype="dict")  # returns Maze
    else:
        raise Exception('Fail in loading file {filepath}'.format(filepath=filepath))


def _load_from_csv(filename):
    """
    Load csv file\n
    returns: Maze object
    """
    if os.name == "nt":
        maze_dir = "mazes\\"
    else:
        maze_dir = "mazes/"
    filepath = maze_dir + filename
    data = {}
    with open(filepath, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data = row
        return convert_data(data, datatype="dict")  # returns Maze
    else:
        raise Exception('Fail in loading file {filepath}'.format(filepath=filepath))


def convert_data(data, datatype) -> Maze:
    """
    Choose converter via datatype\n
    Converts data from datatype to Maze object
    Returns: Maze object
    """
    deserializer = _get_converter(datatype)
    return deserializer(data)


def _get_converter(datatype):
    """returns deserializer method based on datatype"""
    if datatype.lower() == "dict":
        return _convert_from_dict


def _convert_from_dict(data):
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


def _new_file_num(self, path: str) -> int:
    path = path
    # returns a list of files in mazes folder
    files = [f for f in glob.glob(path + "*.*", recursive=False)]
    # lambda function splits the files string by dot and slash returning just the filename
    if os.name == "nt":
        filenames = list(map(lambda x: x.split(".")[0].split("\\")[1], files))
    else:
        filenames = list(map(lambda x: x.split(".")[0].split("/")[1], files))
    # lambda function returns just the digits after 'maze' in the filename
    numbers = list(
        filter(
            lambda x: x.isdigit(),
            map(lambda x: x.split("maze")[1].split("_")[0], filenames),
        )
    )
    if numbers:
        # find the highest number in the list
        highest_num = max(int(num) for num in numbers)
    else:
        highest_num = 0
    new_file_num = highest_num + 1
    return new_file_num


def save(maze, datatype) -> Maze:
    """save maze to disk in datatype format"""
    data = convert_to_dict(maze)
    if datatype == "json":        
        return _save_as_json(data)
    elif datatype == "csv":        
        return _save_as_csv(data)
    else:
        raise Exception

    
def _save_as_json(data):
    if os.name == "nt":
        path = "mazes\\"
    else:
        path = "mazes/"
    filename = "{path}maze{number}_{width}x{height}.{fileformat}".format(
        path=path,
        number=_new_file_num(path),
        width=(maze.width - 1) // 2,
        height=(maze.height - 1) // 2,
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
    filename = "{path}maze{number}_{width}x{height}.{fileformat}".format(
        path=path,
        number=_new_file_num(path),
        width=(maze.width - 1) // 2,
        height=(maze.height - 1) // 2,
        fileformat='csv',
    )
    with open(filename, mode="w") as maze_file:
        fieldnames = ["width", "height", "start_coord", "end_coord", "maze"]
        writer = csv.DictWriter(maze_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow(
            {
                "width": data["width"],
                "height": data["height"],
                "start_coord": data["start_coord"],
                "end_coord": data["end_coord"],
                "maze": data["maze"],
            }
        )
    maze_file.close()

    filename = "{}maze_stats{}_{}x{}.{}".format(
        path,
        filenumber,
        (self.maze.width - 1) // 2,
        (self.maze.height - 1) // 2,
        self.datatype,
    )
    with open(filename, mode="w") as stats_file:
        fieldnames = ["algo", "route", "steps", "time"]
        writer = csv.DictWriter(stats_file, fieldnames=fieldnames)
        stat_data = data["stats"]

        writer.writeheader()
        for row, data in enumerate(stat_data):
            writer.writerow(
                {
                    "algo": stat_data[row]["algo"],
                    "route": stat_data[row]["route"],
                    "steps": stat_data[row]["steps"],
                    "time": stat_data[row]["time"],
                }
            )
    stats_file.close()
