import copy
from time import process_time


def dfs(maze, route, steps, x=1, y=1, first_run=0):
    """Returns [route, total_steps]"""
    if first_run == 1:
        route = []
        steps = []
        solution = {}

    steps.append([x, y])
    #  Check if we have reached the end
    if maze[x][y] == "2":
        route.append([x, y])
    # Check right
    elif (
        y < len(maze) - 1
        and maze[x][y + 1] == "0"
        or y < len(maze) - 1
        and maze[x][y + 1] == "2"
    ):
        maze[x][y] = "3"
        route.append([x, y])
        dfs(maze, route=route, steps=steps, x=x, y=y + 1)
    #  Check down
    elif (
        x < len(maze[0]) - 1
        and maze[x + 1][y] == "0"
        or x < len(maze) - 1
        and maze[x + 1][y] == "2"
    ):
        maze[x][y] = "3"
        route.append([x, y])
        dfs(maze, route=route, steps=steps, x=x + 1, y=y)
    #  Check left
    elif y > 0 and maze[x][y - 1] == "0" or y > 0 and maze[x][y - 1] == "2":
        maze[x][y] = "3"
        route.append([x, y])
        dfs(maze, route=route, steps=steps, x=x, y=y - 1)
    #  Check up
    elif x > 0 and maze[x - 1][y] == "0" or x > 0 and maze[x - 1][y] == "2":
        maze[x][y] = "3"
        route.append([x, y])
        dfs(maze, route=route, steps=steps, x=x - 1, y=y)
    else:
        maze[x][y] = "3"
        del route[-1]
        dfs(maze, route=route, steps=steps, x=route[-1][0], y=route[-1][1])

    solution = {"route": route, "steps": steps}
    return solution


def resolve_maze(maze_obj, amount=1, solver=dfs):
    """
    Resolves a maze\n
    maze: maze object\n 
    amount: How many times should the maze be resolved, default=1\n
    solver: Which algoritm to use, default=dfs\n
    """
    maze = maze_obj
    maze_copy = copy.deepcopy(maze)

    while amount > 0:
        start_time = process_time()
        if solver == "dfs":
            solution = dfs(maze_copy.maze, route=[], steps=[], first_run=1)
        time = process_time() - start_time
        maze.Stats.add_solution(solver, solution["route"], solution["steps"], time)
        maze_copy = copy.deepcopy(maze)
        amount -= 1
