# Author: Daniel Dang - Student ID: 103528453
# Last modified: 18-05-2024

import tkinter as tk
from tkinter import filedialog, Tk, Canvas
import customtkinter
from generate_maze import generate_maze
import time
import random
import sys
sys.path.append('cbs') 
from cbs import cbs
sys.path.append('sipp') 
from multi_sipp import MultiSipp
import colorsys
from functions import *
# import pyautogui


class Application(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x800")
        self.title("Maze Solving Algorithms")
        self.resizable(False, False)
        self.configure(fg_color = "#D4D4D4")
        self.cell_width = 0
        self.canvas = Canvas(self,bg="#D4D4D4",height = 800,width = 1200,bd = 0,highlightthickness = 0)
        self.maze_area = Canvas(self, bg="#D4D4D4",width=700, height=535,highlightthickness = 0)
        self.selected_button = None
        # self.no_solution = False
        self.show_path = customtkinter.StringVar(value="off")
        self.toggle = False

        self.mouse_x = 0.0
        self.mouse_y = 0.0
        self.create_mode = 1
        self.highlight_colors = {1: "#FFD60A", 2: "green", 3: "black", 4: "white"}
        self.in_create_mode = False

        self.explored_nodes = self.canvas.create_text( 1091.0, 601.0, anchor="nw", text="", fill="#000000", font=("Inter Bold", 20 * -1) )
        self.path_length = self.canvas.create_text( 1091.0, 683.0, anchor="nw", text="", fill="#000000", font=("Inter Bold", 20 * -1) )
        self.no_solution = self.canvas.create_text( 860.0, 526.0, anchor="nw", text="", fill="red", font=("Inter", 20, "bold") )

        # parse the text file to create the maze
        self.maze = load_maze("mazes/grid_5.txt")
        self.agents = maze_info(self.maze)['agents']
        self.draw()


    # draw everything to the screen
    def draw(self):
        self.create_widgets()
        self.draw_maze(self.maze)
        self.draw_buttons()


    def create_widgets(self):
        canvas = self.canvas
        canvas.place(x = 0, y = 0)

        self.round_rectangle(40.0, 567.0, 706.0, 753.0, r=20,fill="white")
        self.round_rectangle(806.0, 578.0, 1121.0, 647.0, r=20,fill="white")

        canvas.create_rectangle( 521.0, 598.0, 560.0, 637.0, fill="#000000", outline="")
        canvas.create_rectangle( 119, 598.0, 158, 637.0, fill="#FFD60A", outline="")
        canvas.create_rectangle( 321, 598.0, 360, 637.0, fill="#008000", outline="")
        canvas.create_rectangle( 322, 685.0, 360, 724.0, fill="orange", outline="")
        canvas.create_rectangle( 119, 685.0, 158, 724.0, fill="grey", outline="")
        canvas.create_text( 172, 605.0, anchor="nw", text=": Start", fill="#000000", font=("Inter", 16 ) )
        canvas.create_text( 375, 605.0, anchor="nw", text=": Goal", fill="#000000", font=("Inter", 16) )
        canvas.create_text( 576.0, 603.0, anchor="nw", text=": Wall", fill="#000000", font=("Inter", 16) )
        canvas.create_text( 172, 692.0, anchor="nw", text=": Discovered", fill="#000000", font=("Inter", 16) )
        canvas.create_text( 375, 692.0, anchor="nw", text=": Path", fill="#000000", font=("Inter", 16) )

        canvas.create_text( 839.0, 612.5, anchor="w", text="Result:", fill="#000000", font=("Inter", 18) )
        # canvas.create_text( 809.0, 694.5, anchor="w", text="Path length:", fill="#000000", font=("Inter", 18) )
        
        def toggle_switch():
            if self.toggle:
                self.toggle = False
                self.show_path = customtkinter.StringVar(value="off")
            else:
                self.toggle = True
                self.show_path = customtkinter.StringVar(value="on")


        switch_1 = customtkinter.CTkSwitch(master=canvas, text="Show path", command=toggle_switch, progress_color="#184E77", button_color="white",
                                        variable=self.show_path, onvalue="on", offvalue="off",font=("Inter", 18))
        switch_1.place(x=900.0, y=390)


    def round_rectangle(self, x1, y1, x2, y2, r=10, **kwargs):    
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        return self.canvas.create_polygon(points, **kwargs, smooth=True)
    
    def draw_maze(self, maze):
        agents = self.agents
        # Create a Canvas widget
        W = 700
        H = 535
        canvas = self.maze_area
        canvas.delete('all')
        canvas.place(x=30, y=30)

        # Define the dimensions of the grid
        rows, cols = maze.shape

        # Define the size of each cell in the grid
        cell_width = H / maze.shape[0] - 2
        if cell_width > W / maze.shape[1] - 2:
            cell_width = W / maze.shape[1] - 2

        self.cell_width = cell_width
        # Draw the grid
        for row in range(rows):
            for col in range(cols):
                x1 = col * cell_width + 10
                y1 = row * cell_width
                x2 = x1 + cell_width
                y2 = y1 + cell_width
                cell_color = "white"
                # Check if mouse is within the cell
                if x1 <= self.mouse_x <= x2 and y1 <= self.mouse_y <= y2 and self.in_create_mode:
                    cell_color = self.highlight_colors[self.create_mode]  # Change color if mouse is within the cell
                if maze[(row, col)] == 1:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                elif maze[(row, col)] == -1:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="#FFD60A")
                elif maze[(row, col)] == 2:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, fill=cell_color)
                
        # Draw agents and their goals
        # for agent in agents:
        #     start_row, start_col = agent['start']
        #     goal_row, goal_col = agent['goal']
            # Draw agent number at start position
            # canvas.create_text(start_col * cell_width + cell_width / 2 + 10, start_row * cell_width + cell_width / 2,
            #                 text=agent['name'], fill='white')
            # # Draw goal number at goal position
            # canvas.create_text(goal_col * cell_width + cell_width / 2 + 10, goal_row * cell_width + cell_width / 2,
            #                 text=agent['name'], fill='white')
    # draw the buttons to choose algorithm
    def draw_buttons(self):
        button_1 = customtkinter.CTkButton(self,text="Load Maze",width=151.0,height=53.0, font=("Inter", 18, "bold"),fg_color="#184E77",text_color=("white", "#ffffff"),command=lambda : self.import_maze())
        button_1.configure()
        button_1.place( x=784.0, y=75) 

        button_2 = customtkinter.CTkButton(self,text="Random Maze", width=169.0, height=53.0, font=("Inter", 18, "bold"),fg_color="#184E77",text_color=("white", "#ffffff"),command=lambda : self.randomize_maze())
        button_2.place(x=969.0, y=75)

        button_9 = customtkinter.CTkButton(self,text="Create Maze", width=169.0, height=53.0, font=("Inter", 18, "bold"),fg_color="#184E77",text_color=("white", "#ffffff"),command=lambda : self.create_maze())
        button_9.place(x=870.0, y=150)

        button_3 = customtkinter.CTkButton(self,text="CBS", font=("Inter", 20, "bold"),width=97.0,height=56.0,command=lambda : self.draw_solution(self.maze_area, 0, button_3))
        button_3.configure(fg_color="white",text_color=("black", "#000000"),hover_color=("#0A9396", "0A9396"))
        button_3.place(x=970.0,y=274.5)

        button_4 = customtkinter.CTkButton(self,text="SIPP", font=("Inter", 20, "bold"), width=97.0,height=56.0, command=lambda : self.draw_solution(self.maze_area, 1, button_4))
        button_4.configure(fg_color="white",text_color=("black", "#000000"),hover_color=("#0A9396", "0A9396"))
        button_4.place( x=840.0, y=274.5)

    # highlight the button of the chosen algorithm
    def change_selected_button(self,button):
        if self.selected_button is not None:
            self.selected_button.configure(fg_color="white",text_color=("black", "#000000"))
        button.configure(fg_color="#0A9396")
        self.selected_button = button

    def get_agent_color(self, agent_index, num_agents):
        # Calculate the hue angle for each agent
        hue = (agent_index / num_agents) * 360
        # Convert hue to RGB color
        rgb = colorsys.hsv_to_rgb(hue / 360, 0.7, 0.9)  # Saturation and value are fixed
        # Convert RGB to hexadecimal color code
        color_code = '#%02x%02x%02x' % tuple(int(c * 255) for c in rgb)
        return color_code

    # highlight the explored cells and the path
    def draw_path(self,paths,canvas):
        collision = False

        self.draw_maze(self.maze)
        max_moves = max(len(path) for path in paths.values())
        # Initialize a dictionary to store the rectangles drawn for each agent
        agent_rectangles = {}
        self.canvas.delete("agent_text")
        
        # Iterate over the maximum number of moves
        for i in range(max_moves):
            current_positions = []
            # Clear the previous move's rectangles from the canvas
            if self.show_path.get() == "off":
                for agent_rects in agent_rectangles.values():
                    for rect in agent_rects:
                        canvas.delete(rect)
            agent_rectangles.clear()  # Clear the dictionary for the new move

            for agent, path in paths.items():
                # Check if the agent has moves left
                if i < len(path):
                    # Get the current cell for the agent
                    cell = path[i]
                    if cell in current_positions:
                        # Draw "FAIL" in red if there are collisions
                        collision = True
                        self.canvas.create_text(1040.0, 612.5, text="FAIL", anchor="e", fill="red", font=("Inter", 20, "bold"), tags="agent_text")
                    else:
                        current_positions.append(cell)
                    x1 = cell[1] * self.cell_width + 10
                    y1 = cell[0] * self.cell_width
                    x2 = x1 + self.cell_width
                    y2 = y1 + self.cell_width
                    index = agent[-1]
                    # Assign a color based on the agent
                    color = self.get_agent_color(int(index), len(paths))
                    # Draw the rectangle and store its ID
                    rect_id = canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                    # Store the rectangle's ID in the dictionary
                    agent_rectangles.setdefault(agent, []).append(rect_id)

            self.update_idletasks()
            time.sleep(0.2)
        print(collision)
        if not collision:
            self.canvas.create_text(1070.0, 612.5, text="SUCCESS", anchor="e", fill="green", font=("Inter", 20, "bold"), tags="agent_text")


    # draw the explored cells and path of the algorithms
    def draw_solution(self, canvas, algo, button):
        self.change_selected_button(button)
        self.canvas.delete(self.explored_nodes)
        self.canvas.delete(self.path_length)
        self.canvas.delete(self.no_solution)
        path = None

        if algo == 0:
            path = cbs.CBS(self.maze).search()
        elif algo == 1:
            path = MultiSipp(self.maze).search()

        if path != None:    
            self.draw_path(path, canvas)
        # if no solution is found
        else:
            self.no_solution = self.canvas.create_text( 860.0, 526.0, anchor="nw", text="No Path Found", fill="red", font=("Inter", 20, "bold") )
    

#####################################################################################
# MAZE GENERATION
    # load maze from imported file
    def import_maze(self):
        self.in_create_mode = False
        file = filedialog.askopenfilename(initialdir="mazes", title="Select A File")

        if file != "":
            # parse the text file to create the maze
            maze = load_maze(file)
            if maze is not None:
                self.maze = maze
                self.draw_maze(self.maze)

            self.canvas.delete(self.explored_nodes)
            self.canvas.delete(self.path_length)
            self.canvas.delete(self.no_solution)

            if self.selected_button is not None:
                self.selected_button.configure(fg_color="white",text_color=("black", "#000000"))

    # generate a random maze 
    def randomize_maze(self):
        self.in_create_mode = False
        width = random.randint(8, 25)
        height = random.randint(8, 25)
        self.maze = generate_maze(width, height)
        self.draw_maze(self.maze)
        self.canvas.delete(self.explored_nodes)
        self.canvas.delete(self.path_length)
        self.canvas.delete(self.no_solution)

        if self.selected_button is not None:
            self.selected_button.configure(fg_color="white",text_color=("black", "#000000"))

    def create_maze(self):
        self.in_create_mode = True
        dialogue = customtkinter.CTkInputDialog(text="Number of rows:", title="Maze Dimension", font=("Inter", 15),button_fg_color="#184E77")
        rows = dialogue.get_input()
        dialogue = customtkinter.CTkInputDialog(text="Number of columns:", title="Maze Dimension",font=("Inter", 15),button_fg_color="#184E77")
        cols = dialogue.get_input()
        self.maze = numpy.zeros((int(rows), int(cols)))
        self.draw_maze(self.maze)
        self.canvas.delete(self.explored_nodes)
        self.canvas.delete(self.path_length)
        self.canvas.delete(self.no_solution)
        if self.selected_button is not None:
            self.selected_button.configure(fg_color="white",text_color=("black", "#000000"))

        if self.in_create_mode:
            self.maze_area.bind('<Motion>', self.motion)

            # Bind number key presses to update create mode
            self.bind('1', lambda event: self.update_create_mode(1))  # Start
            self.bind('2', lambda event: self.update_create_mode(2))  # Goal
            self.bind('3', lambda event: self.update_create_mode(3))  # Wall
            self.bind('4', lambda event: self.update_create_mode(4))  # Empty cell

            # Bind left mouse button click event to update cell based on create mode
            self.maze_area.bind("<Button-1>", self.update_cell_handler)

    def motion(self, event):
        if self.in_create_mode:
            self.mouse_x = event.x
            self.mouse_y = event.y
            self.draw_maze(self.maze)
        # print('{}, {}'.format(self.mouse_x, self.mouse_y))
        # self.canvas.create_text( 820.0, 526.0, anchor="nw", text='{}, {}'.format(self.mouse_x, self.mouse_y), fill="black", font=("Inter", 10, "bold") )

    def update_create_mode(self, mode):
        self.create_mode = mode
        if mode == 1:
            print("Create mode: Start")
        elif mode == 2:
            print("Create mode: Goal")
        elif mode == 3:
            print("Create mode: Wall")
        else:
            print("Create mode: Empty cell")

    def update_cell(self, row, col):
        if self.create_mode == 1:  # Start
            self.maze[(row, col)] = -1
        elif self.create_mode == 2:  # Goal
            self.maze[(row, col)] = 2
        elif self.create_mode == 3:  # Wall
            self.maze[(row, col)] = 1
        else:  # Empty cell
            self.maze[(row, col)] = 0
        self.draw_maze(self.maze)

    def update_cell_handler(self, event):
        if self.in_create_mode:
            # Calculate row and column based on mouse position
            row = int((event.y) // self.cell_width)
            col = int((event.x - 10) // self.cell_width)
            self.update_cell(row, col)


if __name__ == "__main__":
    customtkinter.deactivate_automatic_dpi_awareness()
    app = Application()
    app.mainloop()