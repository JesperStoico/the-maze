from model import Maze
import view

def start():
    size = 16
    maze1 = Maze(size, size)
    view.pretty_print(maze1)

if __name__ == "__main__":
    start()