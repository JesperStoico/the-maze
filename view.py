# import controller


# Takes a converted (pretty) maze and pretty prints it
def pretty_print(maze):
    for a in maze.pretty_maze:
        string = ""
        for b in a:
            string += b
        print(string)
    print("")
