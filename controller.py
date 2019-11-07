import model
import view
from resolver import resolve_maze
import glob
import os
from file_management import load, save

current_maze = []


def start():
    view.start()


def create_new_maze(width, height):
    """Used to creates a new maze and return it"""
    global current_maze
    current_maze = model.MazeGenerator().generate(width, height)
    return current_maze


def get_current_maze():
    """Used to getting the current maze that is shown"""
    return current_maze


def run_DFS_on_maze(run_X_times, solver1):
    """Used to run a resolver x amunt of times on the current maze"""
    global current_maze
    resolve_maze(current_maze, amount=run_X_times, solver=solver1)


def save_maze():
    global current_maze
    save(current_maze, "json")
    # model.MazeSerializer(current_maze, "json").save()


def load_maze(filename, data_type):
    global current_maze
    current_maze = load(filename)
    # current_maze = model.MazeDeserializer().load(filename, data_type)


def get_files_in_dir(fileformat: str) -> list:
    files = [f for f in glob.glob("mazes/" + "*." + fileformat)]
    if os.name == "nt":
        files = list(map(lambda x: x.split("mazes\\")[1], files))
    else:
        files = list(map(lambda x: x.split("mazes/")[1], files))
    return files


if __name__ == "__main__":
    start()
