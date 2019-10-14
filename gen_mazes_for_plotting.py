from model import MazeGenerator, MazeSerializer
from model import Resolver


def generate_mazes(size: int, amount: int) -> list:
    mazes = []
    for i in range(amount):
        mg = MazeGenerator()
        maze = mg.generate(size, size)
        mazes.append(maze)

    return mazes


def solve_mazes(mazes: list, times: int) -> list:
    for maze in mazes:
        resolver = Resolver(maze)
        resolver.solve(times)

    return mazes


def save_mazes(mazes: list):
    for maze in mazes:
        maze_export = MazeSerializer(maze, datatype="json")
        maze_export.save()


mazes = generate_mazes(10, 10)
mazes = solve_mazes(mazes, 10)
save_mazes(mazes)
