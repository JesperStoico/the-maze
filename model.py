from random import shuffle
import os
import re
import sys
import copy
import json
import glob
import jsbeautifier

# needed for dfg...
sys.setrecursionlimit(10000)


class Maze:
    def __init__(self, maze, width, height, start_coords, end_coords):
        self.maze = maze  # this used to be pretty_maze
        # holds a clean copy of maze
        # needed for DFS recursive method when
        # generating multiple solutions

        self.width = width
        self.height = height
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.Stats = Stats()

    # Overloaded __str__ method so we can use print(maze)
    # outputs json version of maze
    def __str__(self):
        ms = MazeSerializer(self, datatype="dict")
        data = ms.get_output()
        data = json.dumps(data)
        data = jsbeautifier.beautify(data)
        return data


# MazeGenerator outputs new mazes based on width/height input
class MazeGenerator:
    def __init__(self):
        pass

    def generate(self, width: int, height: int) -> Maze:

        self.empty_maze = [[[] for b in range(width)] for a in range(height)]
        self.raw_maze = self._dfg(self.empty_maze)
        self.pretty_maze = self._convert(self.raw_maze)
        self.start_coords = (1, 1)
        # self.end_coords = ((width * 2) - 1, (height * 2) - 1)
        self.end_coords = (len(self.pretty_maze) - 2, len(self.pretty_maze[0]) - 2)

        self._set_entrance()
        self._set_exit()

        return Maze(
            self.pretty_maze,
            len(self.pretty_maze[0]),
            len(self.pretty_maze),
            self.start_coords,
            self.end_coords,
        )

    # Recursive backtracker.
    # Looks at its neighbors randomly, if unvisitied, visit and recurse
    def _dfg(self, maze, coords=(0, 0)):
        #  0,1 = right, 1,0 = down, 0,-1 = left, -1,0 = up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        shuffle(directions)
        for direction in directions:
            new_coords = (coords[0] + direction[0], coords[1] + direction[1])
            if (
                (0 <= new_coords[0] < len(maze))
                and (0 <= new_coords[1] < len(maze[0]))
                and not maze[new_coords[0]][new_coords[1]]
            ):
                maze[coords[0]][coords[1]].append(direction)
                maze[new_coords[0]][new_coords[1]].append(
                    (-direction[0], -direction[1])
                )
                self._dfg(maze, new_coords)
        return maze

    def _convert(self, maze):
        self.pretty_maze = [
            ["1"] * (2 * len(maze[0]) + 1) for a in range(2 * len(maze) + 1)
        ]
        for y, row in enumerate(maze):
            for x, col in enumerate(row):
                self.pretty_maze[2 * y + 1][2 * x + 1] = "0"
                for direction in col:
                    self.pretty_maze[2 * y + 1 + direction[0]][
                        2 * x + 1 + direction[1]
                    ] = "0"
        return self.pretty_maze

    def _set_entrance(self):
        self.pretty_maze[self.start_coords[0]][self.start_coords[1]] = "3"

    def _set_exit(self):
        self.pretty_maze[self.end_coords[0]][self.end_coords[1]] = "2"

    def _convert_data_to_json(self):
        data = {
            "maze": self.pretty_maze,
            "width": len(self.pretty_maze[0]),
            "height": len(self.pretty_maze),
            "start_coords": self.start_coords,
            "end_coords": self.end_coords,
        }
        return data


# MazeDeserializer converts data to Maze objects
# Call .load() method to retrieve data from disk
class MazeDeserializer:
    def __init__(self):
        # we don't need anything to be initialized
        # as we use class methods
        pass

    # open filename from disk - must provide datatype
    def load(self, filename, datatype) -> Maze:
        self.loader = self._get_loader(datatype)
        return self.loader(filename)  # returns maze

    # returns loader method based on datatype
    def _get_loader(self, datatype):
        if datatype == "json":
            return self._load_from_json
        elif datatype == "csv":
            return self._load_from_csv
        else:
            raise Exception

    def _load_from_json(self, filename):
        if os.name == "nt":
            maze_dir = "mazes\\"
        else:
            maze_dir = "mazes/"

        if os.path.isfile(maze_dir + filename):
            with open(maze_dir + filename, "r") as file:
                data = json.load(file)  # returns dict

            return self.deserialize(data, datatype="dict")  # returns Maze
        else:
            raise Exception

    def _load_from_csv(self, filename):
        # TODO implement this method
        pass

    def deserialize(self, data, datatype) -> Maze:
        # determines which deserilizer to use
        self.deserializer = self._get_deserializer(datatype)
        return self.deserializer(data)  # returns a Maze object

    # returns deserializer method based on datatype
    def _get_deserializer(self, datatype):
        if datatype.lower() == "json":
            return self._deserialize_from_json
        elif datatype.lower() == "csv":
            return self._deserialize_from_csv
        elif datatype.lower() == "dict":
            return self._deserialize_from_dict

    # returns maze from json data
    def _deserialize_from_json(self, data):
        payload = json.loads(data)
        maze = Maze(
            payload["maze"],
            payload["width"],
            payload["height"],
            payload["start_coords"],
            payload["end_coords"],
        )
        if payload["stats"]:  # if maze has stats, add Stats() object
            maze.Stats = Stats()
            for stat in payload["stats"]:
                maze.Stats.solutions.append(stat)
        return maze

    def _deserialize_from_dict(self, data):
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

    def _deserialize_from_csv(self, data):
        pass


# MazeSerializer converts Maze Object to flat versions in dict, json, csv
# Call .save() method to store on disk
class MazeSerializer:
    def __init__(self, maze, datatype="dict"):
        self.maze = maze
        self.datatype = datatype
        # determines which deserilizer to use
        self.serializer = self._get_serializer(datatype)
        self.output = self.serializer(maze)  # holds dict version of maze

    def get_output(self):
        return self.output

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

    # save self.output to disk in datatype format
    def save(self):
        self.saver = self._get_saver()
        self.saver()

    # returns saver method based on datatype
    def _get_saver(self):
        if self.datatype == "json":
            return self._save_as_json
        elif self.datatype == "csv":
            return self._save_as_csv
        else:
            raise Exception

    def _save_as_json(self):
        data = self.output
        if os.name == "nt":
            path = "mazes\\"
        else:
            path = "mazes/"
        filename = "{}maze{}_{}x{}.{}".format(
            path,
            self._new_file_num(path),
            (self.maze.width - 1) // 2,
            (self.maze.height - 1) // 2,
            self.datatype,
        )

        with open(filename, "w") as file:
            file.writelines(data)

    def _save_as_csv(self):
        data = self.output
        if os.name == "nt":
            path = "mazes\\"
        else:
            path = "mazes/"
        filenumber = self._new_file_num(path)
        filename = "{}maze{}_{}x{}.{}".format(
            path,
            filenumber,
            (self.maze.width - 1) // 2,
            (self.maze.height - 1) // 2,
            self.datatype,
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

    # returns serializer method based on datatype
    def _get_serializer(self, datatype):
        if datatype.lower() == "json":
            return self._serialize_to_json
        elif datatype.lower() == "csv":
            return self._serialize_to_csv
        elif datatype.lower() == "dict":
            return self._serialize_to_dict

    # returns json version of maze
    def _serialize_to_json(self, maze):
        data = json.dumps(self._serialize_to_dict(maze))
        data = jsbeautifier.beautify(data)
        return data

    # returns csv version of maze
    def _serialize_to_csv(self, maze):
        # TODO implement this method
        pass

    # returns dict version of maze (default)
    def _serialize_to_dict(self, maze):
        data = {
            "maze": maze.maze,
            "width": maze.width,
            "height": maze.height,
            "start_coords": maze.start_coords,
            "end_coords": maze.end_coords,
        }
        if maze.Stats:  # if maze has stats - add them
            data["stats"] = []
            for solution in maze.Stats.solutions:
                data["stats"].append(solution)
        return data


class Stats:
    def __init__(self):
        self.solutions = []  # list of dictionaries with solution stats

    def add_solution(self, algo, route, steps, time):
        self.solutions.append(
            {
                "algo": algo,  # strig - algorithm used to solve maze
                "route": route,  # list - route (solution) through maze
                "steps": steps,  # list - steps taken to achieve solution
                "time": time,  # decimal - solution time
            }
        )

    def get_solutions(self, algo="all"):
        if algo == "all":
            if self.solutions:
                return self.solutions
        else:
            # lambda function filters the list based on the algo input
            # algo = 'dfg' will return all solutions for dfg solver
            result = list(filter(lambda x: algo in x["algo"], self.solutions))
            return result

    def get_times(self, algo="all"):
        if algo == "all":
            if self.solutions:
                times = []
                for item in self.solutions:
                    # print(item['time'])
                    times.append(item["time"])
                return times
        else:
            # second lambda func filters the list of dicts based on algo input
            # filtered list is passed to the first map lambda function
            # which returns all the values of the time key
            result = list(
                map(
                    lambda x: x["time"],
                    filter(lambda x: algo in x["algo"], self.solutions),
                )
            )
            return result

    def time_avg(self, algo="all"):
        return sum(self.get_times(algo)) / len(self.get_times(algo))

    def time_max(self, algo="all"):
        return max(self.get_times(algo))

    def time_min(self, algo="all"):
        return min(self.get_times(algo))


class Cell:
    """
    Represent X,Y cordinate in the maze (used in astar)
    Contains:\n
    x, y = Own cords\n
    prex_x, prex_y = previus cell cords\n
    end_y, end_x = goal\n
    g = distance from previus to current cell\n
    h = Length from cell to goal if there was no walls\n
    f = Weight value on this cell for selcetion(g+h)
    """

    def __init__(self, x, y, prev_x, prev_y, end_x, end_y, g):
        self.x = x
        self.y = y
        self.prev_x = prev_x
        self.prev_y = prev_y
        self.g = g
        self.h = ((x + y) - (end_x + end_y)) * -1
        self.f = self.g + self.h
