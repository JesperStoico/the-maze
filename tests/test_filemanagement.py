import sys

# adding to sys path to gain access to files in folder one level up
sys.path.append("..")

import os
import unittest

import file_management
from model import Maze, MazeFactory


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

    ##############################
    # Unit tests
    ##############################

    def test_check_os_path(self):
        # Windows
        if os.name == "nt":
            self.assertEqual(file_management.check_os_path(), "\\",
                             "Should be '\\'")
        # Mac
        if os.name == 'posix':
            self.assertEqual(file_management.check_os_path(), "/",
                             "Should be '/'")

    def test_new_file_num(self):
        if os.name == 'nt':
            path = 'mazes\\'
        else:
            path = 'mazes/'

        filenames = ["maze10_20x20.json", "maze12_20x20.json"]

        write_test_file(path, filenames)

        self.assertEqual(file_management._new_file_num(path), 13,
                         "Should be 13")

        del_test_file(path, filenames)

    def test_load_unsupported_file_fails(self):
        self.assertRaises(TypeError,
                          file_management.load,
                          "maze.xml",
                          logging=False)

    def test_load_returns_maze_object(self):
        if os.name == 'nt':
            path = 'mazes\\'
        else:
            path = 'mazes/'

        filename = ["maze1_2x2.json"]
        maze_json = '{"maze": [["1", "1", "1", "1", "1"],["1", "3", "1", "0", "1"],["1", "0", "1", "0", "1"],["1", "0", "0", "2", "1"],["1", "1", "1", "1", "1"]],"width": 5,"height": 5,"start_coords": [1, 1],"end_coords": [3, 3],"stats": []}'
        write_test_file(path, filename, maze_json)

        self.assertIsInstance(
            file_management._load_from_json(filename[0], logging=False),
            Maze,
            "Should return instance of Maze class",
        )

        del_test_file(path, filename)

    def test_get_files_in_dir_returns_expected_files(self):
        if os.name == 'nt':
            path = 'mazes\\'
        else:
            path = 'mazes/'

        filenames = [
            "maze1_15x15.json", "maze2_20x20.json", "maze3_30x30.json"
        ]
        write_test_file(path, filenames)

        files = file_management.get_files_in_dir("json")
        del_test_file(path, filenames)

        # check if the list contains expected elements, regardsless of order
        self.assertCountEqual(files, filenames,
                              "should contain {}".format(filenames))

    def test_get_files_in_dir_only_return_expected_file_types(self):
        if os.name == 'nt':
            path = 'mazes\\'
        else:
            path = 'mazes/'

        filenames = ["maze1_15x15.json", "maze2_20x20.json", "maze3_30x30.csv"]
        write_test_file(path, filenames)

        files = file_management.get_files_in_dir("csv")
        del_test_file(path, filenames)

        self.assertCountEqual(files, ["maze3_30x30.csv"],
                              "should contain {}".format("maze3_30x30.csv"))

    ##############################
    # Integration tests
    ##############################

    def test_integration_generate_save_check_file_count(self):
        if os.name == 'nt':
            path = 'mazes\\'
        else:
            path = 'mazes/'

        filenames = ["maze1_5x5.json", "maze2_5x5.json", "maze3_5x5.json"]
        write_test_file(path, filenames)

        new_maze = MazeFactory.generate(5, 5)
        file_management.save(new_maze, "json", logging=False)

        files = file_management.get_files_in_dir("json")

        self.assertCountEqual(
            files, [
                "maze1_5x5.json", "maze2_5x5.json", "maze3_5x5.json",
                "maze4_5x5.json"
            ],
            'Should be ["maze1_5x5.json", "maze2_5x5.json", "maze3_5x5.json", "maze4_5x5.json"]'
        )

        # cleanup test files
        filenames.append('maze4_5x5.json')
        del_test_file(path, filenames)


unittest.main()
