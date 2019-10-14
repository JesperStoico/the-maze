from model import MazeGenerator, MazeSerializer
from model import Maze
from resolver import resolve_maze
from time import process_time
from decimal import Decimal

#############################################################################
#  Bulk generating, solving and saving mazes for plotting
#############################################################################


def generate_mazes(size: int, amount: int) -> list:
    mazes = []
    for i in range(amount):
        print("Generating Maze {} of size {}x{}..".format(i + 1, size, size))
        mg = MazeGenerator()
        maze = mg.generate(size, size)
        mazes.append(maze)

    return mazes


def solve_mazes(mazes: list, times: int) -> list:
    for idx, maze in enumerate(mazes):
        print(
            "Solving Maze {} of size {}x{} - {} times..".format(
                idx + 1, (maze.width - 1) // 2, (maze.height - 1) // 2, times
            ),
            end=" ",
        )
        resolve_maze(maze, times, solver="dfs")
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
        maze_export = MazeSerializer(maze, datatype="json")
        maze_export.save()
        print("Done!")


print("#" * 80)
print("Bulk generating, solving and saving mazes for plotting".center(80))
print("#" * 80)

for i in range(5, 31, 5):
    start_time = process_time()
    mazes = generate_mazes(i, 10)
    mazes = solve_mazes(mazes, 10)
    save_mazes(mazes)
    proc_time = round(Decimal(process_time()) - Decimal(start_time), 2)
    print("Processing time: {} seconds".format(proc_time), end="\n\n")
