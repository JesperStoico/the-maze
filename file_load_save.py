import os
import json
import jsbeautifier  # makes json file more readable

maze_dir = "mazes/"
maze_base_name = "maze"
stat_base_name = "stats"


def convert_data_to_json(maze):
    data = {}
    data = {
        "maze": maze.pretty_maze,
        "width": len(maze.pretty_maze[0]),
        "height": len(maze.pretty_maze),
        "start_coord": maze.start_coord,
        "end_coord": maze.end_coord,
        "stats": maze.Stats.get_solutions(),
    }

    return data


def save_to_json(data, filename):
    # data = jsbeautifier.beautify(data)
    data = json.dumps(data)  # dictionary to json
    data = jsbeautifier.beautify(data)  # make json more readable

    with open(maze_dir + filename + ".json", "w") as file:
        file.writelines(data)


def load_from_json(filename):

    if os.path.isfile(maze_dir + filename):
        with open(maze_dir + filename, "r") as file:
            data = json.load(file)

        return data
