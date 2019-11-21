import tkinter as tk
from tkinter import simpledialog
from time import sleep
from matplotlib import use

from controller import get_files, get_time_graph, get_step_graph
from controller import create_new_maze, get_current_maze
from controller import run_DFS_on_maze, save_maze, load_maze


class Window(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.window_height = self.master.winfo_screenheight()
        self.window_width = self.master.winfo_screenwidth()

        # Add listbox woth button
        self.lb = tk.Listbox(self.master, selectmode="SINGLE", width=40)
        self.lb.grid(row=0, column=2, sticky="ns")
        self.btn = tk.Button(self.master, text="Load",
                                width=30, activebackground='green',
                                command=self.load_maze)
        self.btn.grid(row=1, column=2, sticky="ns")
        self.get_maze_files()

        # Add menu bar
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        # Add menues in the menu bar
        file_menu = tk.Menu(menu)
        maze_menu = tk.Menu(menu)

        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.close_window)

        menu.add_cascade(label="Maze", menu=maze_menu)
        maze_menu.add_command(label="Create new maze", command=self.create_new_maze)
        maze_menu.add_command(label="Run solver on maze", command=self.run_DFS)
        maze_menu.add_command(label="Show rute", command=self.draw_route)
        maze_menu.add_command(label="Save maze", command=self.save_maze)
        maze_menu.add_command(label="Mass creation", command=self.mass_creation)
        maze_menu.add_command(label="Show graph with time", comman=self.draw_time_graf)
        maze_menu.add_command(label="Show graph with steps", comman=self.draw_step_graf)

    # Maze menu funktions
    # create and display a new maze
    def create_new_maze(self):
        width = simpledialog.askinteger("width", "How wide you want you maze")
        height = simpledialog.askinteger("height", "How high you want you maze")
        create_new_maze(width, height)
        self.draw_maze(get_current_maze())

    # Run solver on current maze
    def run_DFS(self):
        solver = self.ask_for_solver()
        run_X_times = simpledialog.askinteger(
            "Running times", "How many times you want to run it"
        )
        run_DFS_on_maze(run_X_times, solver)

    # Saves current maze
    def save_maze(self):
        save_maze(self.ask_for_format())
        self.get_maze_files()

    # Loads maze to be current maze
    def load_maze(self):
        selection = self.lb.get(self.lb.curselection())
        self.draw_maze(load_maze(selection))

    # Creates and saves multiple mazes
    def mass_creation(self):
        Number_of_mazes = simpledialog.askinteger(
            "Running times", "How many mazes you want to make"
        )
        width = simpledialog.askinteger("width", "How wide you want you maze")
        height = simpledialog.askinteger("height", "How high you want you maze")
        run_X_times = simpledialog.askinteger(
            "Running times", "How many times you want to run DFS"
        )
        for x in range(Number_of_mazes):
            create_new_maze(width, height)
            run_DFS_on_maze(run_X_times)
            self.save_maze()
        self.get_maze_files()

        # Draw graf on canvas

    # Show graph in existing window
    def draw_time_graf(self):
        use("TkAgg")
        plt = get_time_graph()
        plt.show()

    # Show graf in new window
    def draw_step_graf(self):
        use("TkAgg")
        plt = get_step_graph()
        plt.show()

    # Draw route on maze
    def draw_route(self):
        maze = get_current_maze()
        resolver_type = self.ask_for_solver()
        if resolver_type == "dfs":
            color = "orange"
        else:
            color = "cyan"
        route = maze.Stats.get_solutions(resolver_type)[0]["route"]
        y = 15
        x = 25
        y_next = y
        x_next = x
        count = 0
        while count < len(route) - 1:
            if route[count + 1][0] - route[count][0] == 1:
                x_next = x_next + 9
            elif route[count + 1][0] - route[count][0] == -1:
                x_next = x_next - 9
            elif route[count + 1][1] - route[count][1] == 1:
                y_next = y_next + 9
            elif route[count + 1][1] - route[count][1] == -1:
                y_next = y_next - 9
            self.maze_canvas.create_line(y, x, y_next, x_next, fill=color, width=3)
            y = y_next
            x = x_next
            count = count + 1
            self.master.update()
            sleep(0.05)

    # Draw current maze
    def draw_maze(self, maze):
        """
        Taking a maze\n
        ajusting the canvas\n
        drawing the maze
        """
        # self.maze_canvas.delete("all")
        self.maze_canvas = tk.Canvas(
            self.master,
            background="black",
            width=self.window_width - 300,
            height=self.window_height - 150,
        )
        self.maze_canvas.grid(row=0, column=0)
        self.start_x = 2
        self.slut_x = 10
        self.count = 0
        for cords in maze.maze:
            self.start_x = self.start_x + 9
            self.slut_x = self.slut_x + 9
            self.start_y = 2
            self.slut_y = 10
            for cords in maze.maze[self.count]:
                if cords == "1":
                    self.maze_canvas.create_rectangle(
                        self.start_y,
                        self.start_x,
                        self.slut_y,
                        self.slut_x,
                        fill="gray90",
                        outline="gray90",
                    )
                if cords == "3":
                    self.maze_canvas.create_oval(
                        self.start_y,
                        self.start_x,
                        self.slut_y,
                        self.slut_x,
                        fill="green",
                    )
                if cords == "2":
                    self.maze_canvas.create_oval(
                        self.start_y, self.start_x, self.slut_y, self.slut_x, fill="red"
                    )
                self.start_y = self.start_y + 9
                self.slut_y = self.slut_y + 9
            self.count = self.count + 1
        ver_scroll = tk.Scrollbar(self.master, orient=tk.VERTICAL)
        ver_scroll.grid(row=0, column=1, sticky="ns")
        ver_scroll.config(command=self.maze_canvas.yview)
        self.maze_canvas.config(
            yscrollcommand=ver_scroll.set, scrollregion=self.maze_canvas.bbox("all")
        )
        hor_scroll = tk.Scrollbar(self.master, orient=tk.HORIZONTAL)
        hor_scroll.grid(row=1, column=0, sticky="we")
        hor_scroll.config(command=self.maze_canvas.xview)
        self.maze_canvas.config(
            xscrollcommand=hor_scroll.set, scrollregion=self.maze_canvas.bbox("all")
        )
        self.master.update()

    # Close the app
    def close_window(self):
        self.master.destroy()

    # Ask user for solver
    def ask_for_solver(self):
        solver = "empty"
        while solver.lower() != 'dfs' and solver.lower() != 'astar':
            solver = simpledialog.askstring("Reolver", "Choice resolving metode: dfs or astar")
        return solver

    # Ask user for format
    def ask_for_format(self):
        format = "empty"
        while format.lower() != 'json' and format.lower() != 'csv':
            format = simpledialog.askstring("Format", "Choice format: json or csv")
        return format

    # Updates listbox with files
    def get_maze_files(self):
        file_list = get_files()
        file_list = sorted(set(file_list), key=lambda x: int(x.split("x")[0].split("_")[1]) * int(x.split("x")[1].split(".")[0]))
        self.lb.delete(0, tk.END)
        for count, maze in enumerate(file_list):
            self.lb.insert(count, maze)


def start():
    root = tk.Tk()
    root.title("The Maze")
    window_height = root.winfo_screenheight()
    window_width = root.winfo_screenwidth()
    root.geometry("%dx%d+0+0" % (window_width, window_height))
    Window(root)
    root.mainloop()
