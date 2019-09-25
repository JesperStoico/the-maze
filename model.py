from random import randint, shuffle, choice
import sys
#needed for DFS...
sys.setrecursionlimit(10000)

class Maze():
    def __init__(self, width, height):
        """
            DFS(make_empty_maze(size,size)) 
        """
        self.empty_maze = self._make_empty_maze(width, height)
        self.raw_maze = self._DFS(self.empty_maze)
        self.pretty_maze = self._convert(self.raw_maze)

    #Returns an empty maze of given size
    def _make_empty_maze(self, width, height):
        maze = [[[] for b in range(width)] for a in range(height)]
        return maze


    #Recursive backtracker.
    #Looks at its neighbors randomly, if unvisitied, visit and recurse
    def _DFS(self, maze, coords=(0,0)):
        #  0,1 = right, 1,0 = down, 0,-1 = left, -1,0 = upte
        directions = [(0,1),(1,0),(0,-1),(-1,0)]
        shuffle(directions)
        for direction in directions:
            new_coords = (coords[0] + direction[0], coords[1] + direction[1])
            if (0 <= new_coords[0] < len(maze)) and \
                (0 <= new_coords[1] < len(maze[0])) and \
                not maze[new_coords[0]][new_coords[1]]:
                    maze[coords[0]][coords[1]].append(direction)
                    maze[new_coords[0]][new_coords[1]].append((-direction[0], -direction[1]))
                    self._DFS(maze, new_coords)
        return maze

    def _convert(self, maze):
        pretty_maze = [["1"]*(2*len(maze[0])+1) for a in range(2*len(maze)+1)]
        for y,row in enumerate(maze):
            for x,col in enumerate(row):
                pretty_maze[2*y+1][2*x+1] = "0"
                for direction in col:
                    pretty_maze[2*y+1+direction[0]][2*x+1+direction[1]] = "0"
        return pretty_maze
    