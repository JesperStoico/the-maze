from random import shuffle
from time import process_time
import os
import sys
import copy
import json
import jsbeautifier

# needed for dfg...
sys.setrecursionlimit(10000)


class Maze:
    def __init__(self, maze, width, height, start_coords, end_coords):
        self.maze = maze
        self.maze_copy = copy.deepcopy(maze)
        self.width = width
        self.height = height
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.Stats = Stats()

    def __str__(self):
        ms = MazeSerializer(self, datatype="dict")
        data = ms.get_output()
        data = json.dumps(data)
        data = jsbeautifier.beautify(data)
        return data


class MazeGenerator:
    def __init__(self):
        pass

    def generate(self, width: int, height: int) -> Maze:
        self.start_coords = (1, 1)
        self.end_coords = ((width * 2) - 1, (height * 2) - 1)

        self.empty_maze = [[[] for b in range(width)] for a in range(height)]
        self.raw_maze = self._dfg(self.empty_maze)
        self.pretty_maze = self._convert(self.raw_maze)
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


class MazeDeserializer:
    def __init__(self):
        pass

    def deserialize(self, data, datatype) -> Maze:
        self.deserializer = self._get_deserializer(
            datatype
        )  # determines which deserilizer to use
        return self.deserializer(data)  # returns a deserialized Maze object

    def _get_deserializer(self, datatype):
        if datatype.lower() == "json":
            return self._deserialize_from_json
        elif datatype.lower() == "csv":
            return self._deserialize_from_csv
        elif datatype.lower() == "dict":
            return self._deserialize_from_dict

    def _deserialize_from_json(self, data):
        payload = json.loads(data)
        maze = Maze(
            payload["maze"],
            payload["width"],
            payload["height"],
            payload["start_coords"],
            payload["end_coords"],
        )
        if payload["stats"]:
            # maze.stats = payload["stats"]
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
        if "stats" in data:
            print("creating stats object")
            # maze.stats = data["stats"]
            maze.Stats = Stats()
            for stat in data["stats"]:
                maze.Stats.solutions.append(stat)
        return maze

    def _deserialize_from_csv(self, data):
        pass

    def load(self, filename, datatype) -> Maze:
        self.loader = self._get_loader(datatype)
        return self.loader(filename)

    def _get_loader(self, datatype):
        if datatype == 'json':
            return self._load_from_json
        elif datatype == 'csv':
            return self._load_from_json
        else:
            raise Exception

    def _load_from_json(self, filename):
        maze_dir = "mazes/"
        maze_base_name = "maze"
        stat_base_name = "stats"

        if os.path.isfile(maze_dir + filename):
            with open(maze_dir + filename, "r") as file:
                data = json.load(file) # returns dict

            return self.deserialize(data, datatype='dict') # returns Maze
        else:
            raise Exception

    def _load_from_csv(self, filename):
        # TODO implement this method
        pass


class MazeSerializer:
    def __init__(self, maze, datatype):
        self.maze = maze
        self.datatype = datatype
        self.serializer = self._get_serializer(
            datatype
        )  # determines which deserilizer to use
        self.output = self.serializer(maze)
        # return self.output

    def get_output(self):
        return self.output

    def save(self):
        self.saver = self._get_saver()
        self.saver()

    def _get_saver(self):
        if self.datatype == "json":
            return self._save_as_json
        elif self.datatype == "csv":
            return self._save_as_csv
        else:
            raise Exception

    def _save_as_json(self):
        data = self.output

        with open("mazes/maze.json", "w") as file:
            file.writelines(data)

    def _save_as_csv(self):
        pass

    def _get_serializer(self, datatype):
        if datatype.lower() == "json":
            return self._serialize_to_json
        elif datatype.lower() == "csv":
            return self._serialize_to_csv
        elif datatype.lower() == "dict":
            return self._serialize_to_dict

    def _serialize_to_json(self, maze):
        data = json.dumps(self._serialize_to_dict(maze))
        data = jsbeautifier.beautify(data)
        return data

    def _serialize_to_csv(self, maze):
        # TODO implement this method
        pass

    def _serialize_to_dict(self, maze):
        data = {
            "maze": maze.maze,
            "width": maze.width,
            "height": maze.height,
            "start_coords": maze.start_coords,
            "end_coords": maze.end_coords,
        }
        if maze.Stats:
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


class Resolver:
    def __init__(self, maze):
        self.route = []
        self.total_steps = []
        self.pretty_maze = maze.maze
        self.pretty_maze_copy = copy.deepcopy(self.pretty_maze)
        self.maze = maze

    def solve(self, amount):
        for i in range(amount):
            start_time = process_time()
            self.dfs()
            time = process_time() - start_time
            self.maze.Stats.add_solution("dfs", self.route, self.total_steps, time)
            self.pretty_maze = copy.deepcopy(self.pretty_maze_copy)
            self.route = []
            self.total_steps = []

    # def dfs(self, pretty_maze, x, y):
    def dfs(self, x=1, y=1):
        self.total_steps.append([x, y])
        #  Tjek om vi er i mål
        if self.pretty_maze[x][y] == "2":
            self.route.append([x, y])

        # Tjek om jeg kan gå til højre
        elif (
            y < len(self.pretty_maze) - 1
            and self.pretty_maze[x][y + 1] == "0"
            or y < len(self.pretty_maze) - 1
            and self.pretty_maze[x][y + 1] == "2"
        ):
            self.pretty_maze[x][y] = "3"
            self.route.append([x, y])
            # print('rykket højre')
            self.dfs(x, y + 1)
        #  Tjek om jeg kan gå ned
        elif (
            x < len(self.pretty_maze[0]) - 1
            and self.pretty_maze[x + 1][y] == "0"
            or x < len(self.pretty_maze) - 1
            and self.pretty_maze[x + 1][y] == "2"
        ):
            self.pretty_maze[x][y] = "3"
            self.route.append([x, y])
            # print('rykket ned')
            self.dfs(x + 1, y)
        #  Tjek om jeg kan gå til venstre
        elif (
            y > 0
            and self.pretty_maze[x][y - 1] == "0"
            or y > 0
            and self.pretty_maze[x][y - 1] == "2"
        ):
            self.pretty_maze[x][y] = "3"
            self.route.append([x, y])
            # print('rykket venstre')
            self.dfs(x, y - 1)
        #  Tjek om jeg kan gå op
        elif (
            x > 0
            and self.pretty_maze[x - 1][y] == "0"
            or x > 0
            and self.pretty_maze[x - 1][y] == "2"
        ):
            self.pretty_maze[x][y] = "3"
            self.route.append([x, y])
            # print('rykket op')
            self.dfs(x - 1, y)
        #  Tjek for no win scenario
        # elif self.route[0][0] == x and self.route[0][1] == y:
        #     print("No Solution")
        #     print("Routen er: " + str(self.route))
        #     print("Antal total steps incl start: " + str(len(self.total_steps)))
        #     return self.route, self.total_steps
        else:
            self.pretty_maze[x][y] = "3"
            # print('Backtrace')
            del self.route[-1]
            self.dfs(self.route[-1][0], self.route[-1][1])
