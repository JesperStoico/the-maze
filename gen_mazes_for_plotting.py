from time import process_time
from decimal import Decimal

from model import MazeFactory
from model import Maze
from resolver import resolve_maze
from file_management import save
#############################################################################
#  Bulk generating, solving and saving mazes for plotting
#############################################################################


def generate_mazes(size: int, amount: int) -> list:
    mazes = []
    for i in range(amount):
        print("Generating Maze {} of size {}x{}..".format(i + 1, size, size))
        maze = MazeFactory.generate(size, size)
        mazes.append(maze)

    return mazes


def solve_mazes(mazes: list, times: int, solver: str) -> list:
    for idx, maze in enumerate(mazes):
        print(
            "Solving Maze {} of size {}x{} - {} times..".format(
                idx + 1, (maze.width - 1) // 2, (maze.height - 1) // 2, times
            ),
            end=" ",
        )
        resolve_maze(maze, times, solver=solver)
        print("Done!")

    return mazes


def save_mazes(mazes: list):
    for idx, maze in enumerate(mazes):
        print(
            "Saving Maze {} of size {}x{}..".format(
                idx + 1, (maze.width - 1) // 2, (maze.height - 1) // 2
            ),
            end=" ",
        )
        save(maze, 'json')
        print("Done!")


print("#" * 80)
print("Bulk generating, solving and saving mazes for plotting".center(80))
print("#" * 80)


def mass_gen_mazes(Start_size=5, end_size=30, jumps=5, mazes_pr_size=10, dfs_runs=10, astar_runs=10):
    """
    Used to mass generate mazes\n
    Start_size - the size of the first mazes\n
    end_size - the size of the last mazes\n
    jumps - The jump between sizes\n
    mazes_pr_size - How many mazes of each size\n
    dfs_runs - How many times to solve each size with dfs\n
    astar_runs - How many times to solve each size with astar\n
    """
    script_start = process_time()
    for i in range(Start_size, end_size+1, jumps):
        start_time = process_time()
        mazes = generate_mazes(i, mazes_pr_size)
        mazes = solve_mazes(mazes, dfs_runs, "dfs")
        mazes = solve_mazes(mazes, astar_runs, "astar")
        save_mazes(mazes)
        proc_time = round(Decimal(process_time()) - Decimal(start_time), 2)
        print("Processing time: {} seconds".format(proc_time), end="\n\n")

    script_time = round(Decimal(process_time()) - Decimal(script_start), 2)
    print("Processing time: {} seconds".format(script_time), end="\n\n")
