import hashlib

# hashlib algorithms
# ['sha256', 'sha3_384', 'sha1', 'sha384', 'blake2s', 'shake_128', 'sha3_512', 'shake_256', 'blake2b', 'sha3_256', 'md5', 'sha512', 'sha224', 'sha3_224']
# md5 is the shortest hash

# flattened_maze = [cell for row in maze for cell in row]
# line_maze = "".join([cell for row in maze for cell in row])


def hash_maze(maze: list) -> str:
    line_maze = "".join([cell for row in maze for cell in row])
    hash_object = hashlib.md5(line_maze.encode("utf-8"))
    return hash_object.hexdigest()


maze = [["0", "1", "0"], ["1", "0", "1"], ["1", "1", "0"]]


datatype = "json"
filename = "maze_{}x{}_{}.{}".format(len(maze[0]), len(maze), hash_maze(maze), datatype)
print("maze: {}\nhash: {}".format(maze, hash_maze(maze)))
print("filename: {}".format(filename))
