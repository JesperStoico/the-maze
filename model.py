from random import shuffle
import sys
import json
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
        data = convert_to_dict(self)
        data['info'] = 'This is a maze Object'
        del data['stats']
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