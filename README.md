# Project Maze
## Advanced Programming course project

This repo contains a python code to generate and solve random mazes using various algorithms.

******

### TODO
* ~~Write comments in model.py~~ __done!__
* ~~Implement CSV methods for se-/deserializing mazes~~__done__
* ~~Test se-/deserializing mazes with stats~~ __done!__
* Refactor timing method in Resolver to output more readable numbers
* ~~Refactor resolver class to methods in separate file~~ __done!__
* ~~refactor MazeGenerator to facade pattern~~
* ~~Implement AStar resolver~~ __done!__
* Controller functions
  * ~~get list of~~ __done!__
  * ~~load maze and stats from file~~ __done!__
  * ~~generate new maze~~ __done!__
* ~~Refactor A-start to return tuples instead of cells to solution~~ __done!__
* ~~Rewrite overloading of __str__, so we can see what object it is~~ __done!__
* ~~MazeGenerator - generate - User typed start/finish?~~ __won't fix__
* ~~Simplify MazeSerializer/Deserializer~~ __done refactored__
* ~~Create function to create plot data~~ __done!__
* Rewrite get_files function to not retrieve stats files
* Consolidate plotting files to one file
* Plotting in view
* Handle mazes with only one resolver type
* Run mass generation from view
* Threading

### Optional
* ~~Extend file save/load methods to allow for other filenames than maze.json~~ __done!__
* ~~Extend file IO to automatically find appropriate filename for saving~~ __done!__
* Thoughts: should mazes have an ID or hash value to make them unique so we can save a maze again under the same name

******

Project will include the following concepts:
* Object Oriented Programming (OOP)
* Model - View - Controller pattern (MVC)
* Use of differente Maze generating and solving algorithms

The repo is maintained by:
* [Jan Nyman](https://github.com/M19259)
* [Erik Møiniche-Kiebe](https://github.com/codatr0n)
* [Jesper Stoico](https://github.com/JesperStoico)
