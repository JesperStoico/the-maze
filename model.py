from random import shuffle
from time import process_time
import sys
import copy
# needed for dfg...
sys.setrecursionlimit(10000)


class Maze():
    def __init__(self, width, height):
        """
            dfg(make_empty_maze(size,size))
        """
        self.start_coord = (1, 1)
        self.end_coord = ((width*2)-1, (height*2)-1)

        self.empty_maze = self.make_empty_maze(width, height)
        self.raw_maze = self.dfg(self.empty_maze)
        self.pretty_maze = self.convert(self.raw_maze)

        self.Stats = Stats()

    # Returns an empty maze of given size
    def make_empty_maze(self, width, height):
        maze = [[[] for b in range(width)] for a in range(height)]
        return maze

    # Recursive backtracker.
    # Looks at its neighbors randomly, if unvisitied, visit and recurse
    def dfg(self, maze, coords=(0, 0)):
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
                self.dfg(maze, new_coords)
        return maze

    def convert(self, maze):
        self.pretty_maze = [["1"]*(2*len(maze[0])+1) for a in range(2*len(maze)+1)]
        for y, row in enumerate(maze):
            for x, col in enumerate(row):
                self.pretty_maze[2*y+1][2*x+1] = "0"
                for direction in col:
                    self.pretty_maze[2*y+1+direction[0]][2*x+1+direction[1]] = "0"
        self.set_entrance()
        self.set_exit()
        return self.pretty_maze

    def set_entrance(self):
        self.pretty_maze[self.start_coord[0]][self.start_coord[1]] = "3"

    def set_exit(self):
        self.pretty_maze[self.end_coord[0]][self.end_coord[1]] = "2"


class Stats():

    def __init__(self):
        self.solutions = []  # list of dictionaries with solution stats

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
            # algo = 'dfg' will return all solutions for dfg solver
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

    def time_avg(self, algo='all'):
        return sum(self.get_times(algo)) / len(self.get_times(algo))

    def time_max(self, algo='all'):
        return max(self.get_times(algo))

    def time_min(self, algo='all'):
        return min(self.get_times(algo))


class Resolver():
    def __init__(self, maze):
        self.route = []
        self.total_steps = []
        self.pretty_maze = maze.pretty_maze
        self.pretty_maze_copy = copy.deepcopy(self.pretty_maze)
        self.maze = maze

    def solve(self, amount):
        for i in range(amount):
            start_time = process_time()
            self.dfs()
            time = process_time() - start_time
            self.maze.Stats.add_solution('dfs', self.route, self.total_steps, time)
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
        elif y < len(self.pretty_maze)-1 and \
                self.pretty_maze[x][y+1] == "0" or \
                y < len(self.pretty_maze)-1 and \
                self.pretty_maze[x][y+1] == "2":
            self.pretty_maze[x][y] = "3"
            self.route.append([x, y])
            # print('rykket højre')
            self.dfs(x, y+1)
        #  Tjek om jeg kan gå ned
        elif x < len(self.pretty_maze[0])-1 and \
                self.pretty_maze[x+1][y] == "0" or \
                x < len(self.pretty_maze)-1 and \
                self.pretty_maze[x+1][y] == "2":
            self.pretty_maze[x][y] = "3"
            self.route.append([x, y])
            # print('rykket ned')
            self.dfs(x+1, y)
        #  Tjek om jeg kan gå til venstre
        elif y > 0 and self.pretty_maze[x][y-1] == "0" or \
                y > 0 and self.pretty_maze[x][y-1] == "2":
            self.pretty_maze[x][y] = "3"
            self.route.append([x, y])
            # print('rykket venstre')
            self.dfs(x, y-1)
        #  Tjek om jeg kan gå op
        elif x > 0 and self.pretty_maze[x-1][y] == "0" or \
                x > 0 and self.pretty_maze[x-1][y] == "2":
            self.pretty_maze[x][y] = "3"
            self.route.append([x, y])
            # print('rykket op')
            self.dfs(x-1, y)
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
