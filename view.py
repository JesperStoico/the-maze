import controller

# Takes a converted (pretty) maze and pretty prints it
def pretty_print(maze):
    for a in maze.maze:
        string = ""
        for b in a:
            string += b
        print(string)
    print("")


def display(maze):
    for a in maze.maze:
        string = ""
        for b in a:
            if b == "1":
                string += "#"
            if b == "0":
                string += " "
            if b == "3":
                string += "S"
            if b == "2":
                string += "E"

        print(string)
    print("")
