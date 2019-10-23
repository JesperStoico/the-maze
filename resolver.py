import copy
from time import process_time
from model import Cell


# DFS resolver
def dfs(maze, route, steps, x=1, y=1, first_run=0):
    """Returns: {'route': [], 'steps': []}"""
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
        y < len(maze[0]) - 1
        and maze[x][y + 1] == "0"
        or y < len(maze[0]) - 1
        and maze[x][y + 1] == "2"
    ):
        maze[x][y] = "3"
        route.append([x, y])
        dfs(maze, route=route, steps=steps, x=x, y=y + 1)
    #  Check down
    elif (
        x < len(maze) - 1
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


# backtrace route on astar
def backtrace_route(visited_cells):
    """
    Backtrace from the cell you are in and back to start and\n
    returns a list with the cordinates of the route
    """
    route = [[visited_cells[-1].x, visited_cells[-1].y]]
    cur_obj = visited_cells[-1]
    while cur_obj.prev_x != "start":
        for cell in visited_cells:
            if cell.x == cur_obj.prev_x and cell.y == cur_obj.prev_y:
                route.append([cell.x, cell.y])
                cur_obj = cell
    route.reverse()
    return route


# Tjek if object is in visited_cells list on astar
def is_in_visited_cells(visited_cells, x, y):
    """Checks if cords are already in the visited_cells"""
    for cell in visited_cells:
        if cell.x == x and cell.y == y:
            return True
    return False


# change list of cell to cords
def cell_to_cords(route_of_cells):
    coords = [(cell.x, cell.y) for cell in route_of_cells]
    return coords


# A* search af en maze
def a_star_search(maze):
    """
    Parameter: Maze object\n
    Returns: {'route': [], 'steps': []}\n
    """

    pretty_maze = maze.maze
    end_x = maze.end_coords[0]
    end_y = maze.end_coords[1]
    not_visited_cells = []
    visited_cells = []

    # set start cell in to not_visited_cells
    cell = Cell(
        maze.start_coords[0], maze.start_coords[1], "start", "start", end_x, end_y, 0
    )
    not_visited_cells.append(cell)

    # Start of a-star
    while len(not_visited_cells) > 0:
        # Set next cords to look from
        current_cell = not_visited_cells[-1]
        x = current_cell.x
        y = current_cell.y
        g = current_cell.g

        # Move from open to closed
        visited_cells.append(not_visited_cells[-1])
        del not_visited_cells[-1]

        # Check if this cell is the final cell
        if pretty_maze[x][y] == "2":
            route = backtrace_route(visited_cells)
            steps = cell_to_cords(visited_cells)
            return {"route": route, "steps": steps}

        #  Check cell right
        if (
            y < len(pretty_maze[0]) - 1
            and is_in_visited_cells(visited_cells, x, y + 1) is False
            and (pretty_maze[x][y + 1] == "0" or pretty_maze[x][y + 1] == "2")
        ):
            cell = Cell(x, y + 1, x, y, end_x, end_y, g + 1)
            not_visited_cells.append(cell)

        #  Check cell down
        if (
            x < len(pretty_maze) - 1
            and is_in_visited_cells(visited_cells, x + 1, y) is False
            and (pretty_maze[x + 1][y] == "0" or pretty_maze[x + 1][y] == "2")
        ):
            cell = Cell(x + 1, y, x, y, end_x, end_y, g + 1)
            not_visited_cells.append(cell)

        #  Check cell left
        if (
            y > 0
            and is_in_visited_cells(visited_cells, x, y - 1) is False
            and (pretty_maze[x][y - 1] == "0" or pretty_maze[x][y - 1] == "2")
        ):
            cell = Cell(x, y - 1, x, y, end_x, end_y, g + 1)
            not_visited_cells.append(cell)

        #  Check cell up
        if (
            x > 0
            and is_in_visited_cells(visited_cells, x - 1, y) is False
            and (pretty_maze[x - 1][y] == "0" or pretty_maze[x - 1][y] == "2")
        ):
            cell = Cell(x - 1, y, x, y, end_x, end_y, g + 1)
            not_visited_cells.append(cell)

        #  Sorting list acending
        not_visited_cells.sort(key=lambda x: x.f, reverse=True)


def resolve_maze(maze_obj, amount=1, solver="dfs"):
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
        if solver == "astar":
            solution = a_star_search(maze)
        time = process_time() - start_time
        maze.Stats.add_solution(solver, solution["route"], solution["steps"], time)
        maze_copy = copy.deepcopy(maze)
        amount -= 1
