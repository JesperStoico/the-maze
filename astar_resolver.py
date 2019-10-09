from model import Maze
import view


def start():
    size = 60
    maze1 = Maze(size, size)
    view.pretty_print(maze1)
    a_star_search(maze1)


class Cell:
    """
        
        g = dfgasdfg
        h = ahdfhadf
        
    """

    def __init__(self, x, y, prev_x, prev_y, end_x, end_y, g):
        self.x = x
        self.y = y
        self.prev_x = prev_x
        self.prev_y = prev_y
        self.g = g
        self.h = ((x + y) - (end_x + end_y)) * -2
        self.f = self.g + self.h


# backtrace route
def find_rute(close_set):
    route = [[close_set[-1].x, close_set[-1].y]]
    cur_obj = close_set[-1]
    while cur_obj.prev_x != "start":
        for i, val in enumerate(close_set):
            if val.x == cur_obj.prev_x and val.y == cur_obj.prev_y:
                route.append([val.x, val.y])
                cur_obj = val
    return route


#  Tjek if object is in close_set list
def is_in_close_set(close_set, x, y):
    for i, val in enumerate(close_set):
        if val.x == x and val.y == y:
            return True
    return False


#  A* search af en maze
def a_star_search(maze):
    pretty_maze = maze.pretty_maze
    end_x = maze.end_coord[0]
    end_y = maze.end_coord[1]
    open_set = []
    close_set = []

    #  set start cell in to open_set
    cell = Cell(
        maze.start_coord[0], maze.start_coord[1], "start", "start", end_x, end_y, g=0
    )
    open_set.append(cell)

    #  Start of a-star
    while len(open_set) > 0:
        #  Set next cords to look from
        x = open_set[-1].x
        y = open_set[-1].y
        g = open_set[-1].g

        #  Move from open to closed
        close_set.append(open_set[-1])
        del open_set[-1]

        #  Tjek if this cell is the final cell
        if pretty_maze[x][y] == "2":
            route = find_rute(close_set)
            print("You reached goal, the route is:")
            print(route)
            print("you used this many steps:")
            print(len(close_set))
            print("Route is this many steps:")
            print(len(route))
            print("Start cords are:")
            print(maze.start_coord)
            print("End cords are:")
            print(maze.end_coord)
            break

        #  Tjek cell right
        if (
            y < len(pretty_maze) - 1
            and is_in_close_set(close_set, x, y + 1) is False
            and (pretty_maze[x][y + 1] == "0" or pretty_maze[x][y + 1] == "2")
        ):
            cell = Cell(x, y + 1, x, y, end_x, end_y, g + 1)
            open_set.append(cell)

        #  Tjek cell down
        if (
            x < len(pretty_maze[0]) - 1
            and is_in_close_set(close_set, x + 1, y) is False
            and (pretty_maze[x + 1][y] == "0" or pretty_maze[x + 1][y] == "2")
        ):
            cell = Cell(x + 1, y, x, y, end_x, end_y, g + 1)
            open_set.append(cell)

        #  Tjek cell left
        if (
            y > 0
            and is_in_close_set(close_set, x, y - 1) is False
            and (pretty_maze[x][y - 1] == "0" or pretty_maze[x][y - 1] == "2")
        ):
            cell = Cell(x, y - 1, x, y, end_x, end_y, g + 1)
            open_set.append(cell)

        #  Tjek cell up
        if (
            x > 0
            and is_in_close_set(close_set, x - 1, y) is False
            and (pretty_maze[x - 1][y] == "0" or pretty_maze[x - 1][y] == "2")
        ):
            cell = Cell(x - 1, y, x, y, end_x, end_y, g + 1)
            open_set.append(cell)

        open_set.sort(key=lambda x: x.f, reverse=True)

        # print("står på:" + str(x) + "," + str(y))
        # for i, val in enumerate(open_set):
        #    print(i, "x =", val.x, "y =", val.y, "g =", val.g, "h =", val.h, "f =", val.f)


if __name__ == "__main__":
    start()
