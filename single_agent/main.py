# Author: Daniel Dang - Student ID: 103528453
# Last modified: 18-05-2024

import tkinter as tk
from tkinter import filedialog, Tk, Canvas
import customtkinter
from generate_maze import generate_maze
from uninformed_algo import *
from informed_algo import *
from custom_algo import *
from all_goals import *
from functions import *
import time
import random


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
        self.all_goals = customtkinter.StringVar(value="off")
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
        self.round_rectangle(776.0, 578.0, 1151.0, 647.0, r=20,fill="white")
        self.round_rectangle( 776.0, 660.0, 1151.0, 729.0,r=20,fill="white")

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

        canvas.create_text( 809.0, 612.5, anchor="w", text="Explored nodes:", fill="#000000", font=("Inter", 18) )
        canvas.create_text( 809.0, 694.5, anchor="w", text="Path length:", fill="#000000", font=("Inter", 18) )
        
        def toggle_switch():
            if self.toggle:
                self.toggle = False
                self.all_goals = customtkinter.StringVar(value="off")
            else:
                self.toggle = True
                self.all_goals = customtkinter.StringVar(value="on")


        switch_1 = customtkinter.CTkSwitch(master=canvas, text="Find all goals", command=toggle_switch, progress_color="#184E77", button_color="white",
                                        variable=self.all_goals, onvalue="on", offvalue="off",font=("Inter", 18))
        switch_1.place(x=880.0, y=420)




    def round_rectangle(self, x1, y1, x2, y2, r=10, **kwargs):    
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        return self.canvas.create_polygon(points, **kwargs, smooth=True)
    

    # draw the maze
    def draw_maze(self, maze):
        # Create a Canvas widget
        W = 700
        H = 535
        canvas = self.maze_area
        canvas.delete('all')
        canvas.place(x=30, y=30)

        # Define the dimensions of the grid
        rows, cols = maze.shape

        # Define the size of each cell in the grid
        cell_width = H/maze.shape[0]-2
        if cell_width > W/maze.shape[1]-2:
            cell_width = W/maze.shape[1]-2

        self.cell_width = cell_width
        # Draw the grid
        for row in range(rows):
            for col in range(cols):
                x1 = col * cell_width+10
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

    # draw the buttons to choose algorithm
    def draw_buttons(self):
        button_1 = customtkinter.CTkButton(self,text="Load Maze",width=151.0,height=53.0, font=("Inter", 18, "bold"),fg_color="#184E77",text_color=("white", "#ffffff"),command=lambda : self.import_maze())
        button_1.configure()
        button_1.place( x=784.0, y=75) 

        button_2 = customtkinter.CTkButton(self,text="Random Maze", width=169.0, height=53.0, font=("Inter", 18, "bold"),fg_color="#184E77",text_color=("white", "#ffffff"),command=lambda : self.randomize_maze())
        button_2.place(x=969.0, y=75)

        button_9 = customtkinter.CTkButton(self,text="Create Maze", width=169.0, height=53.0, font=("Inter", 18, "bold"),fg_color="#184E77",text_color=("white", "#ffffff"),command=lambda : self.create_maze())
        button_9.place(x=870.0, y=150)

        button_3 = customtkinter.CTkButton(self,text="DFS", font=("Inter", 20, "bold"),width=97.0,height=56.0,command=lambda : self.draw_solution(self.maze_area, 0, button_3))
        button_3.configure(fg_color="white",text_color=("black", "#000000"),hover_color=("#0A9396", "0A9396"))
        button_3.place(x=776.0,y=232.99999999999994)

        button_4 = customtkinter.CTkButton(self,text="BFS", font=("Inter", 20, "bold"), width=97.0,height=56.0, command=lambda : self.draw_solution(self.maze_area, 1, button_4))
        button_4.configure(fg_color="white",text_color=("black", "#000000"),hover_color=("#0A9396", "0A9396"))
        button_4.place( x=776.0, y=315.99999999999994, )

        button_5 = customtkinter.CTkButton(self,text="GBFS", font=("Inter", 20, "bold"), width=97.0,height=56.0, command=lambda : self.draw_solution(self.maze_area, 2, button_5))
        button_5.configure(fg_color="white",text_color=("black", "#000000"),hover_color=("#0A9396", "0A9396"))
        button_5.place( x=900.0, y=315.99999999999994, )

        button_6 = customtkinter.CTkButton(self,text="A*", font=("Inter", 20, "bold"), width=97.0,height=56.0, command=lambda : self.draw_solution(self.maze_area, 3, button_6))
        button_6.configure(fg_color="white",text_color=("black", "#000000"),hover_color=("#0A9396", "0A9396"))
        button_6.place( x=900.0, y=232.99999999999994, )

        button_7 = customtkinter.CTkButton(self,text="IDA*", font=("Inter", 20, "bold"), width=127.0,height=56.0, command=lambda : self.draw_solution(self.maze_area, 5, button_7))
        button_7.configure(fg_color="white",text_color=("black", "#000000"),hover_color=("#0A9396", "0A9396"))
        button_7.place( x=1024.0, y=315.99999999999994, )

        button_8 = customtkinter.CTkButton(self,text="Dijkstra", font=("Inter", 20, "bold"), width=127.0,height=56.0, command=lambda : self.draw_solution(self.maze_area, 4, button_8))
        button_8.configure(fg_color="white",text_color=("black", "#000000"),hover_color=("#0A9396", "0A9396"))
        button_8.place( x=1024.0, y=232.99999999999994, )

    # highlight the button of the chosen algorithm
    def change_selected_button(self,button):
        if self.selected_button is not None:
            self.selected_button.configure(fg_color="white",text_color=("black", "#000000"))
        button.configure(fg_color="#0A9396")
        self.selected_button = button

    # highlight the explored cells and the path
    def draw_path(self,explored,path,canvas):
        self.draw_maze(self.maze)
        for cell in explored:
            x1 = cell[1] * self.cell_width+10
            y1 = cell[0] * self.cell_width 
            x2 = x1 + self.cell_width
            y2 = y1 + self.cell_width
            canvas.create_rectangle(x1, y1, x2, y2, fill="grey")
            self.update_idletasks()
            time.sleep(0.03)

        for cell in path:
            x1 = cell[1] * self.cell_width+10
            y1 = cell[0] * self.cell_width
            x2 = x1 + self.cell_width
            y2 = y1 + self.cell_width
            canvas.create_rectangle(x1, y1, x2, y2, fill="orange")
            self.update_idletasks()
            time.sleep(0.05)

    # draw the explored cells and path of the algorithms
    def draw_solution(self, canvas, algo, button):
        self.change_selected_button(button)
        self.canvas.delete(self.explored_nodes)
        self.canvas.delete(self.path_length)
        self.canvas.delete(self.no_solution)
        explored, path = None, None

        # if the user wants to find all the goals
        if self.all_goals.get() == "on":
            explored, path = updated_algorithms(self.maze, algo)
        
        # if the user wants to the path to the first goal
        else:
            if algo == 0:
                explored, path = DFS(self.maze)
            elif algo == 1:
                explored, path = BFS(self.maze)
            elif algo == 2: 
                explored, path = GBFS(self.maze)
            elif algo == 3:
                explored, path = A_star(self.maze)
            elif algo == 4:
                explored, path = dijkstra(self.maze)
            elif algo == 5:
                explored, path = ida_star(self.maze)

        if path != None:    
            self.draw_path(explored, path, canvas)
            self.explored_nodes = self.canvas.create_text( 1110.0, 612.5, anchor="e", text=len(explored), fill="#000000", font=("Inter", 18, "bold"))
            self.path_length = self.canvas.create_text( 1110.0, 694.5, anchor="e", text=len(path), fill="#000000", font=("Inter", 18, "bold"))
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
        height = random.randint(8, 20)
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
            if -1 in self.maze:
                # Already a start cell, do not allow setting another
                print("Start cell already exists")
                return
            else:
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