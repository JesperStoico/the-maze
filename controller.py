from model import Maze
import view,  resolver
from file_creation import create_csv_files



def start():
    size = 40
    maze1 = Maze(size, size)
    view.pretty_print(maze1)

    resolver = Resolver(maze1)
    resolver.solve(8)

    # print(maze1.Stats.get_solutions())
    print("Times:", maze1.Stats.get_times())
    print("Min time: {}".format(maze1.Stats.time_min()))
    print("Max time: {}".format(maze1.Stats.time_max()))
    print("Avg time: {}".format(maze1.Stats.time_avg()))


if __name__ == "__main__":
    start()
