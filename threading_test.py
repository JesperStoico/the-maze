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


lock = threading.Lock()


def create_maze(s, pool, size, solve_times=10):
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


if __name__ == "__main__":

    # settings parameters for script
    maze_amount = 10
    resolvers = ["dfs", "astar"]
    sizes = [5, 10, 15, 20, 25, 30]
    solve_times = 10

    # defining pools and semaphore
    pool = ThreadPool()
    semaphore_count = cpu_count()
    s = threading.Semaphore(semaphore_count)
    thread_count = 0
    threads = []

    # reading start script time
    script_start = process_time()

    for size in sizes:
        for _ in range(maze_amount):
            thread_count += 1
            t = threading.Thread(
                target=create_maze,
                name="thread_" + str(thread_count),
                args=(s, pool, size, solve_times),
            )

            # starting thread
            t.start()

            # appending thread to threads list
            threads.append(t)

    # joining all threads to main thread get total script time
    for t in threads:
        t.join()

    # calculating end script time
    script_time = round(Decimal(process_time()) - Decimal(script_start), 2)
    print("Processing time: {} seconds".format(script_time), end="\n\n")
