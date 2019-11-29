import unittest

import model


class TestMazeGeneration(unittest.TestCase):
    def test_empty_maze(self):
        width = 5
        height = 5
        empty_maze = model.MazeFactory.generate_empty_maze(width, height)
        self.assertEqual(len(empty_maze), 5)
        self.assertEqual(len(empty_maze[0]), 5)
        # Testing a none square maze
        width = 4
        height = 7
        empty_maze = model.MazeFactory.generate_empty_maze(width, height)
        self.assertEqual(len(empty_maze), 7)
        self.assertEqual(len(empty_maze[0]), 4)

    def test_dfg(self):
        empty_maze = model.MazeFactory.generate_empty_maze(5), 5)
        raw_maze = model.MazeFactory._dfg(empty_maze)


if __name__ == "__main__":
    unittest.main()