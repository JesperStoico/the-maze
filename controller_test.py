from model import Maze, Resolver
from model import MazeGenerator, MazeDeserializer
from model import MazeSerializer
import view
from file_load_save import convert_data_to_json, save_to_json, load_from_json


def start():
    size = 10
    # maze1 = Maze(size, size)
    mg = MazeGenerator()
    maze1 = mg.generate(size, size)

    view.pretty_print(maze1)

    print(maze1.hash())

    # maze1_export = MazeSerializer(maze1, datatype="json")

    # print(maze1_export.output)
    # maze1_export.save()


if __name__ == "__main__":
    start()
