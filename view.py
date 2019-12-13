import tkinter as tk
from tkinter import simpledialog
from time import sleep
from matplotlib import use

from controller import get_files, get_time_graph, get_step_graph
from controller import create_new_maze, get_current_maze
from controller import mass_generate_mazes, mass_generate_mazes_threading
from controller import run_DFS_on_maze, save_maze, load_maze


# Maze menu funktions
# create and display a new maze
def view_create_new_maze():
    width = simpledialog.askinteger("width", "How wide you want you maze")
    height = simpledialog.askinteger("height", "How high you want you maze")
    create_new_maze(width, height)
    draw_maze(get_current_maze())


# Run solver on current maze
def run_DFS():
    solver = ask_for_solver()
    run_X_times = simpledialog.askinteger("Running times",
                                          "How many times you want to run it")
    run_DFS_on_maze(run_X_times, solver)


# Saves current maze
def view_save_maze():
    save_maze(ask_for_format())
    update_files_listbox()


# Loads maze to be current maze
def view_load_maze():
    selection = lb.get(lb.curselection())
    draw_maze(load_maze(selection))


# Creates and saves multiple mazes
def mass_creation():
    Start_size = simpledialog.askinteger("Start size",
                                         "smallest size labyrant you want",
                                         minvalue=5,
                                         maxvalue=50)
    end_size = simpledialog.askinteger("End size",
                                       "Biggest size labyrant you want",
                                       minvalue=5,
                                       maxvalue=50)
    jumps = simpledialog.askinteger("Jumps",
                                    "Jump between start and end size",
                                    minvalue=1,
                                    maxvalue=10)
    mazes_pr_size = simpledialog.askinteger("Mazes pr size",
                                            "amount of mazes pr size",
                                            minvalue=1,
                                            maxvalue=10)
    dfs_runs = simpledialog.askinteger("DFS runs",
                                       "times to run DFS resolver",
                                       minvalue=1,
                                       maxvalue=10)
    astar_runs = simpledialog.askinteger("A-star runs",
                                         "times to run A-star resolver",
                                         minvalue=1,
                                         maxvalue=10)
    mass_generate_mazes(Start_size, end_size, jumps, mazes_pr_size, dfs_runs,
                        astar_runs)

    # update listbox with content of mazes folders
    update_files_listbox()


def mass_creation_thread():
    mass_generate_mazes_threading()
    update_files_listbox()


# Show graph in existing window
def draw_time_graf_dfs():
    use("TkAgg")  # use Tkinter GUI framework to render matplotlib graph data
    plt = get_time_graph(algo='dfs')
    plt.show()


def draw_time_graf_astar():
    use("TkAgg")  # use Tkinter GUI framework to render matplotlib graph data
    plt = get_time_graph(algo='astar')
    plt.show()


# Show graf in new window
def draw_step_graf():
    use("TkAgg")
    plt = get_step_graph()
    plt.show()


# Draw route on maze
def draw_route():
    maze = get_current_maze()
    resolver_type = ask_for_solver()
    if resolver_type == "dfs":
        color = "orange"
    else:
        color = "cyan"

    # always return first route as they are all the same
    route = maze.Stats.get_solutions(resolver_type)[0]["route"]
    y = 15
    x = 25
    y_next = y
    x_next = x
    count = 0
    length_route = len(route) - 1

    while count < length_route:
        if route[count + 1][0] - route[count][0] == 1:
            x_next = x_next + 9
        elif route[count + 1][0] - route[count][0] == -1:
            x_next = x_next - 9
        elif route[count + 1][1] - route[count][1] == 1:
            y_next = y_next + 9
        elif route[count + 1][1] - route[count][1] == -1:
            y_next = y_next - 9
        maze_canvas.create_line(y, x, y_next, x_next, fill=color, width=3)
        y = y_next
        x = x_next
        count = count + 1
        master.update()
        sleep(0.05)


# Draw current maze
def draw_maze(maze):
    """
    Taking a maze\n
    ajusting the canvas\n
    drawing the maze
    """
    maze_canvas.delete("all")
    start_x = 2
    slut_x = 10

    # iterating through all rows to draw maze one cell at the time
    for count in range(len(maze.maze)):
        start_x = start_x + 9
        slut_x = slut_x + 9
        start_y = 2
        slut_y = 10

        for cords in maze.maze[count]:
            if cords == "1":
                maze_canvas.create_rectangle(
                    start_y,
                    start_x,
                    slut_y,
                    slut_x,
                    fill="gray90",
                    outline="gray90",
                )
            if cords == "3":
                maze_canvas.create_oval(
                    start_y,
                    start_x,
                    slut_y,
                    slut_x,
                    fill="green",
                )
            if cords == "2":
                maze_canvas.create_oval(start_y,
                                        start_x,
                                        slut_y,
                                        slut_x,
                                        fill="red")
            start_y = start_y + 9
            slut_y = slut_y + 9

            # can be enabled for slower rendering of maze
            # master.update()

    # Create vertical scrollbar on canvas
    ver_scroll = tk.Scrollbar(master, orient=tk.VERTICAL)
    ver_scroll.grid(row=0, column=1, sticky="ns")
    ver_scroll.config(command=maze_canvas.yview)
    maze_canvas.config(yscrollcommand=ver_scroll.set,
                       scrollregion=maze_canvas.bbox("all"))

    # Create horisontal scrollbar on canvas
    hor_scroll = tk.Scrollbar(master, orient=tk.HORIZONTAL)
    hor_scroll.grid(row=1, column=0, sticky="we")
    hor_scroll.config(command=maze_canvas.xview)
    maze_canvas.config(xscrollcommand=hor_scroll.set,
                       scrollregion=maze_canvas.bbox("all"))
    master.update()


# Close the app
def close_window():
    master.destroy()


# Ask user for solver
def ask_for_solver():
    solver = "empty"
    while solver.lower() != 'dfs' and solver.lower() != 'astar':
        solver = simpledialog.askstring(
            "Reolver", "Choice resolving metode: dfs or astar")
    return solver


# Ask user for format
def ask_for_format():
    format = "empty"
    while format.lower() != 'json' and format.lower() != 'csv':
        format = simpledialog.askstring("Format", "Choice format: json or csv")
    return format


# Updates listbox with files
def update_files_listbox():
    file_list = get_files()
    file_list.sort(key=len)
    lb.delete(0, tk.END)
    for count, maze in enumerate(file_list):
        lb.insert(count, maze)


def update_logger_label(message):
    logger_label.config(text=message)


def start():
    master.mainloop()


master = tk.Tk()
master.title("The Maze")
window_height = master.winfo_screenheight()
window_width = master.winfo_screenwidth()
master.geometry("{width}x{height}".format(width=window_width,
                                          height=window_height))

# Create canvas and insert in master object
maze_canvas = tk.Canvas(
    master,
    background="black",
    width=window_width - 300,
    height=window_height - 150,
)

# Add canvas to grid
maze_canvas.grid(row=0, column=0)

# Add listbox with button to grid
lb = tk.Listbox(master, selectmode="SINGLE", width=40)
lb.grid(row=0, column=2, sticky="ns")
btn = tk.Button(master,
                text="Load",
                width=30,
                activebackground='green',
                command=view_load_maze)
btn.grid(row=1, column=2, sticky="ns")

# Add menu bar
menu = tk.Menu(master)
master.config(menu=menu)

# Add menues in the menu bar
file_menu = tk.Menu(menu)
maze_menu = tk.Menu(menu)

menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=close_window)

menu.add_cascade(label="Maze", menu=maze_menu)
maze_menu.add_command(label="Create new maze", command=view_create_new_maze)
maze_menu.add_command(label="Run solver on maze", command=run_DFS)
maze_menu.add_command(label="Show rute", command=draw_route)
maze_menu.add_command(label="Save maze", command=view_save_maze)
maze_menu.add_command(label="Mass creation", command=mass_creation)
maze_menu.add_command(label="Mass creation (threading)",
                      command=mass_creation_thread)
maze_menu.add_command(label="Show graph with time (DFS)",
                      command=draw_time_graf_dfs)
maze_menu.add_command(label="Show graph with time (Astar)",
                      command=draw_time_graf_astar)
maze_menu.add_command(label="Show graph with steps", command=draw_step_graf)

# Add label for logging
logger_label = tk.Label(master, text='', bd=1, relief=tk.SUNKEN, anchor=tk.W)
logger_label.grid(row=2, column=0, columnspan=3, sticky='we')

# Populate listbox with files in mazes folder
update_files_listbox()
