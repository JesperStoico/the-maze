from model import Maze, Resolver
import view


def start():
    size = 8
    maze1 = Maze(size, size)
    view.pretty_print(maze1)

    resolver = Resolver(maze1)
    resolver.solve(100)

    # print(maze1.Stats.get_solutions())
    print('Times:', maze1.Stats.get_times())
    print('Min time: {}'.format(maze1.Stats.time_min()))
    print('Max time: {}'.format(maze1.Stats.time_max()))
    print('Avg time: {}'.format(maze1.Stats.time_avg()))


if __name__ == "__main__":
    start()
