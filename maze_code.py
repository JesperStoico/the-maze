from random import shuffle
import sys
# needed for DFS...
sys.setrecursionlimit(10000)


# Each maze cell contains a tuple of directions of cells to which it is connected
# Takes a maze and converts it to an array of 1's and blanks to represent walls, etc
def convert(maze):
    pretty_maze = [["1"]*(2*len(maze[0])+1) for a in range(2*len(maze)+1)]
    for y, row in enumerate(maze):
        for x, col in enumerate(row):
            pretty_maze[2*y+1][2*x+1] = "0"
            for direction in col:
                pretty_maze[2*y+1+direction[0]][2*x+1+direction[1]] = "0"
    return pretty_maze


# Takes a converted maze and pretty prints it
def pretty_print(maze):
    for a in convert(maze):
        string = ""
        for b in a:
            string += b
        print(string)
    print("")


# Returns an empty maze of given size
def make_empty_maze(width, height):
    maze = [[[] for b in range(width)] for a in range(height)]
    return maze


# Recursive backtracker.
# Looks at its neighbors randomly, if unvisitied, visit and recurse
def DFS(maze, coords=(0, 0)):
    #  0,1 = right, 1,0 = down, 0,-1 = left, -1,0 = upte
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    shuffle(directions)
    for direction in directions:
        new_coords = (coords[0] + direction[0], coords[1] + direction[1])
        if (0 <= new_coords[0] < len(maze)) and \
            (0 <= new_coords[1] < len(maze[0])) and \
                not maze[new_coords[0]][new_coords[1]]:
                    maze[coords[0]][coords[1]].append(direction)
                    maze[new_coords[0]][new_coords[1]].append((-direction[0], -direction[1]))
                    DFS(maze, new_coords)
    return maze


size = 8

# pretty_print(DFS(make_empty_maze(size,size)))


#################################################
# Understanding the code
#################################################
def display_maze(maze):
    for row in maze:
        print(row)


maze_empty = make_empty_maze(size, size)
maze_coords = DFS(maze_empty)
maze_converted = convert(maze_coords)

display_maze(maze_coords)
display_maze(maze_converted)
display_maze(maze_converted)
