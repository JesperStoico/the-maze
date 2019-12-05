from model import MazeFactory
from file_management import save

maze = MazeFactory.generate(2, 2)
save(maze, "json")

