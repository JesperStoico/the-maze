import sys

# adding to sys path to gain access to files in folder one level up
sys.path.append("..")

import os
import unittest

import file_management
from model import Maze


def write_test_file(path: str, filenames: list, content="test"):
    """ Creates test files """
    for filename in filenames:
        with open(path + filename, "w") as file:
            file.write(content)


def del_test_file(path: str, filenames: list):
    """ Deletes test files """
    for filename in filenames:
        if os.path.exists(path + filename):
            os.remove(path + filename)
        else:
            print("The file does not exist")


class TestFileManagement(unittest.TestCase):
    def test_new_file_num(self):
        path = file_management.check_os_path()
        filenames = ["maze10_20x20.json", "maze12_20x20.json"]

        write_test_file(path, filenames)

        self.assertEqual(file_management._new_file_num(path), 13, "Should be 13")

        del_test_file(path, filenames)

    def test_check_os_path(self):
        if os.name == "nt":
            self.assertEqual(
                file_management.check_os_path(), "mazes\\", "Should be " "mazes\\"
            )
        else:
            self.assertEqual(
                file_management.check_os_path(), "mazes/", "Should be " "mazes/"
            )

    def test_load_unsupported_file_fails(self):
        self.assertRaises(TypeError, file_management.load, "maze.xml")

    def test_load_returns_maze_object(self):
        path = file_management.check_os_path()
        filenames = ["maze1_2x2.json"]
        maze_json = '{"maze": [["1", "1", "1", "1", "1"],["1", "3", "1", "0", "1"],["1", "0", "1", "0", "1"],["1", "0", "0", "2", "1"],["1", "1", "1", "1", "1"]],"width": 5,"height": 5,"start_coords": [1, 1],"end_coords": [3, 3],"stats": []}'
        write_test_file(path, filenames, maze_json)

        self.assertEqual(
            type(file_management.load(filenames[0])), Maze, "Should return type Maze"
        )

        del_test_file(path, filenames)


if __name__ == "__main__":
    unittest.main()
