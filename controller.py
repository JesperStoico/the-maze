import view
from model import MazeFactory, Singelton_maze
from resolver import resolve_maze
from file_management import load, save, get_files_in_dir
from plotting import get_step_plot, get_time_plot


def start():
    view.start()


def get_files():
    return get_files_in_dir('*')


def create_new_maze(width, height):
    """Used to creates a new maze and return it"""
    current_maze = Singelton_maze()
    current_maze.maze = MazeFactory.generate(width, height)
    return current_maze.maze


def get_current_maze():
    """Used to getting the current maze that is shown"""
    current_maze = Singelton_maze()
    return current_maze.maze


def run_DFS_on_maze(run_X_times, solver1):
    """Used to run a resolver x amunt of times on the current maze"""
    resolve_maze(get_current_maze(), amount=run_X_times, solver=solver1)


def save_maze(format):
    save(get_current_maze(), format)


def load_maze(filename):
    current_maze = Singelton_maze()
    current_maze.maze = load(filename)
    return current_maze.maze


def get_time_graph():
    return get_time_plot


def get_step_graph():
    return get_step_plot


if __name__ == "__main__":
    start()
