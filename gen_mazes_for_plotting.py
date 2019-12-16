# package imports
import os
import threading
from multiprocessing import cpu_count
import logging
from time import process_time
from decimal import Decimal

# project imports
from model import MazeFactory
from resolver import resolve_maze
from file_management import save, _new_file_num

#############################################################################
#  Script style: Bulk generating, solving and saving mazes for plotting
#############################################################################


def generate_mazes(size: int, amount: int) -> list:
    mazes = []
    for i in range(amount):
        print("Generating Maze {} of size {}x{}..".format(i + 1, size, size))
        maze = MazeFactory.generate(size, size)
        mazes.append(maze)

    return mazes


def solve_mazes(mazes: list, times: int, solver: str) -> list:
    for idx, maze in enumerate(mazes):
        print(
            "Solving Maze {} of size {}x{} - {} times..".format(
                idx + 1, (maze.width - 1) // 2, (maze.height - 1) // 2, times),
            end=" ",
        )
        resolve_maze(maze, times, solver=solver)
        print("Done!")

    return mazes


def save_mazes(mazes: list):
    for idx, maze in enumerate(mazes):
        print(
            "Saving Maze {} of size {}x{}..".format(idx + 1,
                                                    (maze.width - 1) // 2,
                                                    (maze.height - 1) // 2),
            end=" ",
        )
        save(maze, 'json')
        print("Done!")


def mass_gen_mazes(Start_size=5,
                   end_size=30,
                   jumps=5,
                   mazes_pr_size=10,
                   dfs_runs=10,
                   astar_runs=10):
    """
    Used to mass generate mazes\n
    Start_size - the size of the first mazes\n
    end_size - the size of the last mazes\n
    jumps - The jump between sizes\n
    mazes_pr_size - How many mazes of each size\n
    dfs_runs - How many times to solve each size with dfs\n
    astar_runs - How many times to solve each size with astar\n
    """
    print("#" * 80)
    print("Bulk generating, solving and saving mazes for plotting".center(80))
    print("#" * 80)
    script_start = process_time()
    for i in range(Start_size, end_size + 1, jumps):
        start_time = process_time()
        mazes = generate_mazes(i, mazes_pr_size)
        mazes = solve_mazes(mazes, dfs_runs, "dfs")
        mazes = solve_mazes(mazes, astar_runs, "astar")
        save_mazes(mazes)
        proc_time = round(Decimal(process_time()) - Decimal(start_time), 2)
        print("Processing time: {} seconds".format(proc_time), end="\n\n")

    script_time = round(Decimal(process_time()) - Decimal(script_start), 2)
    print("Processing time: {} seconds".format(script_time), end="\n\n")


#############################################################################
#  Threading version: Bulk generating, solving and saving mazes for plotting
#############################################################################

logging.basicConfig(level=logging.DEBUG,
                    format="(%(threadName)-9s) %(message)s")


class ThreadPool(object):
    def __init__(self):
        super(ThreadPool, self).__init__()
        self.active = []
        self.lock = threading.Lock()

    def makeActive(self, name):
        with self.lock:
            self.active.append(name)
            logging.debug("Running: %s", self.active)

    def makeInactive(self, name):
        with self.lock:
            self.active.remove(name)
            logging.debug("Running: %s", self.active)


def create_maze(s, pool, size, solve_times, resolvers, lock):
    name = threading.currentThread().getName()
    logging.debug("Waiting to join the pool")
    with s:
        pool.makeActive(name)

        logging.info("Generating Maze of size {x}x{y}..".format(x=size,
                                                                y=size))
        maze = MazeFactory.generate(size, size)
        logging.info("Solving Maze of size {x}x{y}..".format(x=size, y=size))
        for solver in resolvers:
            resolve_maze(maze, solve_times, solver=solver)

        # locking to acquire unique filename number
        lock.acquire()
        save(maze, "json")

        # releasing again to allow other threads
        lock.release()

        pool.makeInactive(name)


def mass_gen_mazes_threading():

    # settings parameters for script
    maze_amount = 10
    resolvers = ["dfs", "astar"]
    sizes = [5, 10, 15, 20, 25, 30]
    solve_times = 10

    # defining pools and semaphore
    pool = ThreadPool()
    semaphore_count = cpu_count()
    s = threading.Semaphore(semaphore_count)
    lock = threading.Lock()
    thread_count = 0

    for size in sizes:
        for _ in range(maze_amount):
            thread_count += 1
            t = threading.Thread(
                target=create_maze,
                name="thread_" + str(thread_count),
                args=(s, pool, size, solve_times, resolvers, lock),
            )

            # starting thread
            t.start()