import sys
import json
import jsbeautifier

from random import shuffle

from utility import check_os_path

# needed for dfg...
sys.setrecursionlimit(10000)


class Maze:
    def __init__(self, maze, width, height, start_coords, end_coords):
        """
        maze holds a clean copy of the maze\n
        needed for DFS recursive method when\n
        generating multiple solutions
        """
        self.maze = maze  # this used to be pretty_maze
        self.width = width
        self.height = height
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.Stats = Stats()

    # Overloaded __str__ method so we can use print(maze)
    # outputs json version of maze
    def __str__(self):
        data = convert_to_dict(self)
        data["info"] = "This is a maze Object"
        del data["stats"]
        data = json.dumps(data)
        data = jsbeautifier.beautify(data)
        return data


class MazeFactory:
    """
    We have used classmethod so we can call the methods without\n
    instantiate an object. (Reason for using cls instead of self)
    """
    @classmethod
    def generate(cls, width: int, height: int) -> Maze:
        empty_maze = [[[] for b in range(width)] for a in range(height)]
        raw_maze = cls._dfg(empty_maze)
        pretty_maze = cls._convert(raw_maze)
        start_coords = (1, 1)
        end_coords = (len(pretty_maze) - 2, len(pretty_maze[0]) - 2)

        # set entrace on maze
        pretty_maze[start_coords[0]][start_coords[1]] = "3"

        # awr exit on maze
        pretty_maze[end_coords[0]][end_coords[1]] = "2"

        return Maze(pretty_maze, len(pretty_maze[0]), len(pretty_maze),
                    start_coords, end_coords)

    # This function creates the routes for the maze
    # Recursive backtracker.
    # Looks at its neighbors randomly, if unvisitied, visit and recurse
    @classmethod
    def _dfg(cls, maze, coords=(0, 0)):
        #  0,1 = right, 1,0 = down, 0,-1 = left, -1,0 = up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        shuffle(directions)
        for direction in directions:
            new_coords = (coords[0] + direction[0], coords[1] + direction[1])
            if ((0 <= new_coords[0] < len(maze))
                    and (0 <= new_coords[1] < len(maze[0]))
                    and not maze[new_coords[0]][new_coords[1]]):
                maze[coords[0]][coords[1]].append(direction)
                maze[new_coords[0]][new_coords[1]].append(
                    (-direction[0], -direction[1]))
                cls._dfg(maze, new_coords)
        return maze

    # This function converts the maze to a more visual maze
    @classmethod
    def _convert(cls, maze):
        cls.pretty_maze = [["1"] * (2 * len(maze[0]) + 1)
                           for a in range(2 * len(maze) + 1)]
        for y, row in enumerate(maze):
            for x, col in enumerate(row):
                cls.pretty_maze[2 * y + 1][2 * x + 1] = "0"
                for direction in col:
                    cls.pretty_maze[2 * y + 1 +
                                    direction[0]][2 * x + 1 +
                                                  direction[1]] = "0"
        return cls.pretty_maze


class Stats:
    def __init__(self):
        self.solutions = []  # list of dictionaries with solution stats

    def add_solution(self, algo, route, steps, time):
        self.solutions.append({
            "algo": algo,  # strig - algorithm used to solve maze
            "route": route,  # list - route (solution) through maze
            "steps": steps,  # list - steps taken to achieve solution
            "time": time,  # decimal - solution time
        })

    def get_solutions(self, algo="all"):
        if algo == "all":
            if self.solutions:
                return self.solutions
        else:
            # lambda function filters the list based on the algo input
            # algo = 'dfs' will return all solutions for dfs solver
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
                ))
            return result

    def time_avg(self, algo="all"):
        return sum(self.get_times(algo)) / len(self.get_times(algo))

    def time_max(self, algo="all"):
        return max(self.get_times(algo))

    def time_min(self, algo="all"):
        return min(self.get_times(algo))


class Cell:
    """
    Represent X,Y cordinate in the maze (only used in astar)
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


class Singelton_maze(object):
    instance = None

    def __new__(self):
        if not self.instance:
            self.instance = super(Singelton_maze, self).__new__(self)
            self.maze = None
        return self.instance


def convert_to_dict(maze):
    """returns dict version of maze"""
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
