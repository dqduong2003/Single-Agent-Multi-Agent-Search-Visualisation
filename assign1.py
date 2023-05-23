# Author: Daniel Dang - Student ID: 103528453
# Last modified: 19-04-2023

import numpy
from uninformed_algo import *
from informed_algo import *
from custom_algo import *
from all_goals import *
import sys

def load_maze(file):
    try:
        f = open(file, "r")
        lines = f.readlines()
        f.close()
    except IOError:
        print("No file found")
        return None
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    info = {}
    try:
        rows, cols = eval(lines[0])
        start = eval(lines[1])
        goals = [eval(g) for g in lines[2].split('|')]
        walls = [eval(w) for w in lines[3:]]

        # create empty grid
        maze = numpy.zeros((rows, cols))

        # place start and goals
        maze[start[1], start[0]] = -1
        info["start"] = (start[1], start[0])
        info["goal"] = []
        for x, y in goals:
            maze[y, x] = 2
            info["goal"].append((y,x))
        
        # place walls
        for x, y, w, h in walls:
            maze[y:y+h, x:x+w] = 1

        return maze
    except:
        print("Invalid file format")
        return None

def visualise_path(path, maze): 
    if path is not None:

        directions = []
        compass = {(0,1): "right", (0,-1): "left", (1,0): "down", (-1,0): "up"}
        
        for i, p in enumerate(path):
            if i > 0:
                dir = tuple(map(lambda i, j: i - j, path[i], path[i-1]))
                directions.append(compass[dir])
        directions_str = "; ".join(directions)
        print(directions_str)
        print("------------------------------------------------------------------")


        for c in path:
            maze[c] = 3
        print(maze) 
    else:
        print("No path found")


def main(file, algo):
    # parse the text file to create the maze
    # file = "mazes/grid_4.txt"
    # file = "mazes/RobotNav-test.txt"
    maze = load_maze(f"mazes\{file}")
    print(maze)
    print("------------------------------------------------------------------")
    if maze is not None:
        if algo.lower() == "dfs":
            explored, path = DFS(maze)
        elif algo.lower() == "bfs":
            explored, path = BFS(maze)
        elif algo.lower() == "gbfs":
            explored, path = GBFS(maze)
        elif algo.lower() == "a*":
            explored, path = A_star(maze)
        elif algo.lower() == "dijkstra":
            explored, path = dijkstra(maze)
        elif algo.lower() == "ida*":
            explored, path = ida_star(maze)

        # print(explored)
        # print(path)
        if explored is not None:
            print(f"{file} {algo.upper()} {len(explored)}")
        else:
            print(f"{file} {algo.upper()} {explored}")
            # print("Path length: " + str(len(path)))
            # print("Explored nodes: " + str(len(explored)))

        visualise_path(path, maze)
    

if __name__ == "__main__":
    file = sys.argv[1]
    algo = sys.argv[2]
    main(file, algo)