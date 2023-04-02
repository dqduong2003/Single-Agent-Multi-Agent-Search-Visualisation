import tkinter as tk
from tkinter import filedialog, Tk, Canvas, Entry, Text, Button, PhotoImage
import customtkinter
from generate_maze import generate_maze
from assign1 import *
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
        self.maze_area = Canvas(self, bg="#D4D4D4",width=700, height=500,highlightthickness = 0)
        self.selected_button = None
        self.no_solution = False

        self.explored_nodes = self.canvas.create_text( 1091.0, 601.0, anchor="nw", text="", fill="#000000", font=("Inter Bold", 20 * -1) )
        self.path_length = self.canvas.create_text( 1091.0, 683.0, anchor="nw", text="", fill="#000000", font=("Inter Bold", 20 * -1) )

        # parse the text file to create the maze
        self.maze = load_maze("mazes/grid_5.txt")
        self.draw()


    def draw(self):
        self.create_widgets()
        self.draw_maze(self.maze)
        self.draw_buttons()


    def create_widgets(self):
        canvas = self.canvas
        canvas.place(x = 0, y = 0)

        self.round_rectangle(40.0, 549.0, 706.0, 759.0, r=20,fill="white")
        self.round_rectangle(776.0, 578.0, 1151.0, 647.0, r=20,fill="white")
        self.round_rectangle( 776.0, 660.0, 1151.0, 729.0,r=20,fill="white")

        canvas.create_rectangle( 521.0, 598.0, 560.0, 637.0, fill="#000000", outline="")
        canvas.create_rectangle( 118.99999999999994, 598.0, 158, 637.0, fill="#FFD60A", outline="")
        canvas.create_rectangle( 320.99999999999994, 598.0, 360, 637.0, fill="#008000", outline="")
        canvas.create_rectangle( 321.99999999999994, 685.0, 360, 724.0, fill="#EE9B00", outline="")
        canvas.create_rectangle( 118.99999999999994, 685.0, 158, 724.0, fill="#5E5E5E", outline="")
        canvas.create_text( 171.99999999999994, 605.0, anchor="nw", text=": Start", fill="#000000", font=("Inter", 16 ) )
        canvas.create_text( 374.99999999999994, 605.0, anchor="nw", text=": Goal", fill="#000000", font=("Inter", 16) )
        canvas.create_text( 576.0, 603.0, anchor="nw", text=": Wall", fill="#000000", font=("Inter", 16) )
        canvas.create_text( 171.99999999999994, 692.0, anchor="nw", text=": Discovered", fill="#000000", font=("Inter", 16) )
        canvas.create_text( 374.99999999999994, 692.0, anchor="nw", text=": Path", fill="#000000", font=("Inter", 16) )

        canvas.create_text( 809.0, 612.5, anchor="w", text="Explored nodes:", fill="#000000", font=("Inter", 18) )
        canvas.create_text( 809.0, 694.5, anchor="w", text="Path length:", fill="#000000", font=("Inter", 18) )
        if self.no_solution:
            canvas.create_text( 879.0, 526.0, anchor="nw", text="No Path Found", fill="#E80000", font=("Inter Bold", 24 * -1) )

    def round_rectangle(self, x1, y1, x2, y2, r=10, **kwargs):    
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        return self.canvas.create_polygon(points, **kwargs, smooth=True)
    
    def draw_maze(self, maze):
        # Create a Canvas widget
        W = 700
        H = 500
        # canvas = tk.Canvas(self., width=W, height=H)
        canvas = self.maze_area
        canvas.delete('all')
        canvas.place(x=30, y=40)

        # canvas.config(bg="blue")

        # Define the dimensions of the grid
        rows, cols = maze.shape

        # Define the size of each cell in the grid
        if rows >= cols:
            cell_width = H/maze.shape[0]-2
        else:
            cell_width = W/maze.shape[1]-2

        self.cell_width = cell_width
        # Draw the grid
        for row in range(rows):
            for col in range(cols):
                x1 = col * cell_width+10
                y1 = row * cell_width
                x2 = x1 + cell_width
                y2 = y1 + cell_width
                if maze[(row, col)] == 1:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                elif maze[(row, col)] == -1:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="yellow")
                elif maze[(row, col)] == 2:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="white")


    def draw_buttons(self):
        button_1 = customtkinter.CTkButton(self,text="Load Maze",width=151.0,height=53.0, font=("Inter", 18, "bold"),fg_color="#184E77",text_color=("white", "#ffffff"),command=lambda : self.import_maze())
        button_1.configure()
        button_1.place( x=784.0, y=88.99999999999994, ) 

        button_2 = customtkinter.CTkButton(self,text="Random Maze", width=169.0, height=53.0, font=("Inter", 18, "bold"),fg_color="#184E77",text_color=("white", "#ffffff"),command=lambda : self.randomize_maze())
        button_2.place(x=969.0, y=88.99999999999994)

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

        button_7 = customtkinter.CTkButton(self,text="Trémaux", font=("Inter", 20, "bold"), width=127.0,height=56.0, command=lambda : self.draw_solution(self.maze_area, 5, button_7))
        button_7.configure(fg_color="white",text_color=("black", "#000000"),hover_color=("#0A9396", "0A9396"))
        button_7.place( x=1024.0, y=315.99999999999994, )

        button_8 = customtkinter.CTkButton(self,text="Dijkstra", font=("Inter", 20, "bold"), width=127.0,height=56.0, command=lambda : self.draw_solution(self.maze_area, 4, button_8))
        button_8.configure(fg_color="white",text_color=("black", "#000000"),hover_color=("#0A9396", "0A9396"))
        button_8.place( x=1024.0, y=232.99999999999994, )

    def change_selected_button(self,button):
        if self.selected_button is not None:
            self.selected_button.configure(fg_color="white",text_color=("black", "#000000"))
        button.configure(fg_color="#0A9396")
        self.selected_button = button


    def import_maze(self):
        file = filedialog.askopenfilename(initialdir="mazes", title="Select A File")

        # parse the text file to create the maze
        maze = load_maze(file)
        if maze is not None:
            self.maze = maze
            self.draw_maze(self.maze)

        if self.selected_button is not None:
            self.selected_button.configure(fg_color="white",text_color=("black", "#000000"))

    def randomize_maze(self):
        width = random.randint(8, 25)
        height = random.randint(8, 20)
        self.maze = generate_maze(width, height)
        self.draw_maze(self.maze)
        if self.selected_button is not None:
            self.selected_button.configure(fg_color="white",text_color=("black", "#000000"))


    def draw_path(self,explored,path,canvas):
        self.draw_maze(self.maze)
        for cell in explored:
            x1 = cell[1] * self.cell_width+10
            y1 = cell[0] * self.cell_width 
            x2 = x1 + self.cell_width
            y2 = y1 + self.cell_width
            canvas.create_rectangle(x1, y1, x2, y2, fill="grey")
            self.update_idletasks()
            time.sleep(0.04)

        for cell in path:
            x1 = cell[1] * self.cell_width+10
            y1 = cell[0] * self.cell_width
            x2 = x1 + self.cell_width
            y2 = y1 + self.cell_width
            canvas.create_rectangle(x1, y1, x2, y2, fill="orange")
            self.update_idletasks()
            time.sleep(0.08)


    def draw_solution(self, canvas, algo, button):
        self.change_selected_button(button)
        self.canvas.delete(self.explored_nodes)
        self.canvas.delete(self.path_length)
        explored, path = None, None
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
            explored, path = Tremaux(self.maze)
        elif algo == 6:
            explored, path = wall_following(self.maze)
        if path != None:    
            self.draw_path(explored, path, canvas)
            self.explored_nodes = self.canvas.create_text( 1110.0, 612.5, anchor="e", text=len(explored), fill="#000000", font=("Inter", 18, "bold"))
            self.path_length = self.canvas.create_text( 1110.0, 694.5, anchor="e", text=len(path), fill="#000000", font=("Inter", 18, "bold"))
        else:
            print("No path found")        


root = customtkinter.CTk()
app = Application()
app.mainloop()