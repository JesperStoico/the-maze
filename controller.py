from model import MazeGenerator, Singelton_maze
import view
from resolver import resolve_maze
import glob
import os
from file_management import load, save


def start():
    view.start()


def create_new_maze(width, height):
    """Used to creates a new maze and return it"""
    # global current_maze
    current_maze = Singelton_maze()
    current_maze.maze = MazeGenerator().generate(width, height)
    return current_maze.maze


def get_current_maze():
    """Used to getting the current maze that is shown"""
    current_maze = Singelton_maze()
    return current_maze.maze


def run_DFS_on_maze(run_X_times, solver1):
    """Used to run a resolver x amunt of times on the current maze"""
    resolve_maze(get_current_maze, amount=run_X_times, solver=solver1)


def save_maze():
    save(get_current_maze, "json")


def load_maze(filename, data_type):
    current_maze = Singelton_maze()
    current_maze.maze = load(filename)
    return current_maze.maze


def get_files_in_dir(fileformat: str) -> list:
    files = [f for f in glob.glob("mazes/" + "*." + fileformat)]
    if os.name == "nt":
        files = list(map(lambda x: x.split("mazes\\")[1], files))
    else:
        files = list(map(lambda x: x.split("mazes/")[1], files))
    return files


if __name__ == "__main__":
    start()
