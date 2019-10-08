import os

maze_dir = 'mazes/'
filename = 'maze2.json'

if os.path.isfile(maze_dir+filename):
    print('yay {} exists in {}'.format(filename, maze_dir))
else:
    print('bummer, can\'t find {} in {}'.format(filename, maze_dir))

