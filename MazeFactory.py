from model import Maze
from random import shuffle


class MazeFactory:
    @classmethod
    def generate(cls, width: int, height: int) -> Maze:
        empty_maze = [[[] for b in range(width)] for a in range(height)]
        raw_maze = cls._dfg(empty_maze)
        pretty_maze = cls._convert(raw_maze)
        start_coords = (1, 1)
        end_coords = (len(pretty_maze) - 2, len(pretty_maze[0]) - 2)

        # set entrace on maze
        pretty_maze[start_coords[0]][start_coords[1]] = "3"

        # awr exit on maze
        pretty_maze[end_coords[0]][end_coords[1]] = "2"

        return Maze(
            pretty_maze, len(pretty_maze[0]), len(pretty_maze), start_coords, end_coords
        )

    # Recursive backtracker.
    # Looks at its neighbors randomly, if unvisitied, visit and recurse
    @classmethod
    def _dfg(cls, maze, coords=(0, 0)):
        #  0,1 = right, 1,0 = down, 0,-1 = left, -1,0 = up
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        shuffle(directions)
        for direction in directions:
            new_coords = (coords[0] + direction[0], coords[1] + direction[1])
            if (
                (0 <= new_coords[0] < len(maze))
                and (0 <= new_coords[1] < len(maze[0]))
                and not maze[new_coords[0]][new_coords[1]]
            ):
                maze[coords[0]][coords[1]].append(direction)
                maze[new_coords[0]][new_coords[1]].append(
                    (-direction[0], -direction[1])
                )
                cls._dfg(maze, new_coords)
        return maze

    @classmethod
    def _convert(cls, maze):
        cls.pretty_maze = [
            ["1"] * (2 * len(maze[0]) + 1) for a in range(2 * len(maze) + 1)
        ]
        for y, row in enumerate(maze):
            for x, col in enumerate(row):
                cls.pretty_maze[2 * y + 1][2 * x + 1] = "0"
                for direction in col:
                    cls.pretty_maze[2 * y + 1 + direction[0]][
                        2 * x + 1 + direction[1]
                    ] = "0"
        return cls.pretty_maze
