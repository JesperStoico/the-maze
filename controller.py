import view

from model import MazeFactory, Singelton_maze, Logging, Log_subcriber
from resolver import resolve_maze
from file_management import load, save, get_files_in_dir
from plotting import get_step_plot, get_time_plot
import gen_mazes_for_plotting

# Initializing logging object
logger = Logging()


def start():
    view.start()


def get_files():
    # Always returns all files(mazes) in the directory
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


def run_DFS_on_maze(run_X_times, solver):
    """Used to run a resolver x amunt of times on the current maze"""
    resolve_maze(get_current_maze(), amount=run_X_times, solver=solver)
    logger.dispatch(
        'You have resolved your maze with {resolver} {amount} times'.format(
            resolver=solver, amount=run_X_times))


def save_maze(filetype):
    save(get_current_maze(), filetype)


def load_maze(filename):
    current_maze = Singelton_maze()
    current_maze.maze = load(filename)
    return current_maze.maze


def get_time_graph():
    return get_time_plot()


def get_step_graph():
    return get_step_plot()


def mass_generate_mazes(Start_size, end_size, jumps, mazes_pr_size, dfs_runs,
                        astar_runs):
    logger.dispatch('Your mass generation is now started...')
    gen_mazes_for_plotting.mass_gen_mazes(Start_size, end_size, jumps,
                                          mazes_pr_size, dfs_runs, astar_runs)
    logger.dispatch('You have created {amount} mazes'.format(
        amount=int((((end_size - Start_size) / jumps) + 1) * mazes_pr_size)))


def mass_generate_mazes_threading():
    logger.dispatch('Your mass generation is now started...')
    gen_mazes_for_plotting.mass_gen_mazes_threading()
    logger.dispatch('All mazes created!')
    # logger.dispatch('You have created {amount} mazes'.format(amount=int((((end_size - Start_size) / jumps) + 1) * mazes_pr_size)))


if __name__ == "__main__":
    # Initializing logger module publisher and subscriber
    logger = Logging()
    # View subscriber, displaying log in view statusline
    log_view = Log_subcriber('view')
    logger.register(log_view, log_view.update_view)
    # File subscriber, saving log lines to log file.
    log_file = Log_subcriber('file')
    logger.register(log_file, log_file.save_to_file)
    start()
