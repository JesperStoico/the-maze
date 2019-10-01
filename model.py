from random import shuffle
import sys
# needed for DFS...
sys.setrecursionlimit(10000)


class Maze():
    def __init__(self, width, height):
        """
            DFS(make_empty_maze(size,size))
        """
        self.empty_maze = self._make_empty_maze(width, height)
        self.raw_maze = self._DFS(self.empty_maze)
        self.pretty_maze = self._convert(self.raw_maze)

        self.Stats = Stats()

    # Returns an empty maze of given size
    def _make_empty_maze(self, width, height):
        maze = [[[] for b in range(width)] for a in range(height)]
        return maze

    # Recursive backtracker.
    # Looks at its neighbors randomly, if unvisitied, visit and recurse
    def _DFS(self, maze, coords=(0, 0)):
        #  0,1 = right, 1,0 = down, 0,-1 = left, -1,0 = up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        shuffle(directions)
        for direction in directions:
            new_coords = (coords[0] + direction[0], coords[1] + direction[1])
            if (0 <= new_coords[0] < len(maze)) and \
                (0 <= new_coords[1] < len(maze[0])) and \
                    not maze[new_coords[0]][new_coords[1]]:
                maze[coords[0]][coords[1]].append(direction)
                maze[new_coords[0]][new_coords[1]].\
                    append((-direction[0], -direction[1]))
                self._DFS(maze, new_coords)
        return maze

    def _convert(self, maze):
        pretty_maze = [["1"]*(2*len(maze[0])+1) for a in range(2*len(maze)+1)]
        for y, row in enumerate(maze):
            for x, col in enumerate(row):
                pretty_maze[2*y+1][2*x+1] = "0"
                for direction in col:
                    pretty_maze[2*y+1+direction[0]][2*x+1+direction[1]] = "0"
        return pretty_maze


class Stats():

    def __init__(self):
        self.solutions = list()  # list of dictionaries with solution stats

    def add_solution(self, algo, route, steps, time):
        self.solutions.append({'algo': algo,    # strig - algorithm used to solve maze
                               'route': route,  # list - route (solution) through maze
                               'steps': steps,  # list - steps taken to achieve solution
                               'time': time     # decimal - solution time
                               })

    def get_solutions(self, algo='all'):
        if algo == 'all':
            if self.solutions:
                return self.solutions
        else:
            # lambda function filters the list based on the algo input
            # algo = 'dfs' will return all solutions for DFS solver
            result = list(filter(lambda x: algo in x['algo'], self.solutions))
            return result

    def get_times(self, algo='all'):
        if algo == 'all':
            if self.solutions:
                times = []
                for item in self.solutions:
                    # print(item['time'])
                    times.append(item['time'])
                return times
        else:
            # second lambda func filters the list of dicts based on algo input
            # filtered list is passed to the first map lambda function
            # which returns all the values of the time key
            result = list(map(lambda x: x['time'], filter(lambda x: algo in x['algo'], self.solutions)))
            return result

    def solution_time_avg(self, algo='all'):
        return sum(self.get_times(algo)) / len(self.get_times(algo))

    def solution_time_max(self, algo='all'):
        return max(self.get_times(algo))

    def solution_time_min(self, algo='all'):
        return min(self.get_times(algo))
