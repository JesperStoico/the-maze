from model import Maze, Resolver
from model import MazeGenerator
from model import MazeSerializer, MazeDeserializer
import view


def start():
    size = 10
    # maze1 = Maze(size, size)
    mg = MazeGenerator()
    maze1 = mg.generate(size, size)

    print(maze1)

    view.pretty_print(maze1)

    maze1_export = MazeSerializer(maze1, datatype="json")

    print(maze1_export.get_output())
    maze1_export.save()

    md = MazeDeserializer()
    maze2 = md.load("maze.json", datatype="json")
    print(type(maze2))


if __name__ == "__main__":
    start()
