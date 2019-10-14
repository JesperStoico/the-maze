from model import Maze
from model import MazeGenerator
from model import MazeSerializer, MazeDeserializer
import view, resolver


def start():
    size = 2    
    mg = MazeGenerator()
    maze = mg.generate(size, size)
    
    print(maze.Stats.__dict__)
    resolver.resolve_maze(maze, 5, 'dfs')
    print(maze.Stats.__dict__)


if __name__ == "__main__":
    start()
