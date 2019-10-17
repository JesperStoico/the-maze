import model
import view
import get_files_in_dir
from resolver import resolve_maze

# from file_creation import create_csv_files

current_maze = []


def start():
    view.start()
    # print(maze1.Stats.get_solutions())
    # print("Times:", maze1.Stats.get_times())
    # print("Min time: {}".format(maze1.Stats.time_min()))
    # print("Max time: {}".format(maze1.Stats.time_max()))
    # print("Avg time: {}".format(maze1.Stats.time_avg()))


def create_new_maze(width, height):
    """Used to creates a new maze and return it"""
    global current_maze
    current_maze = model.MazeGenerator().generate(width, height)
    return current_maze


def get_current_maze():
    """Used to getting the current maze that is shown"""
    return current_maze


def run_DFS_on_maze(run_X_times):
    """Used to run a resolver x amunt of times on the current maze"""
    global current_maze
    # model.Resolver(current_maze).solve(run_X_times)
    resolve_maze(current_maze, amount=run_X_times, solver="dfs")


def save_maze():
    global current_maze
    model.MazeSerializer(current_maze, "json").save()


def load_maze(filename):
    global current_maze
    current_maze = model.MazeDeserializer().load(filename, "json")


def get_file_names():
    files = get_files_in_dir.get_files_in_dir("json", True)
    print(files)


if __name__ == "__main__":
    start()
