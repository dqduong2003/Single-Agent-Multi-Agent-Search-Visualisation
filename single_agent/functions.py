# Author: Daniel Dang - Student ID: 103528453
# Last modified: 18-05-2024

import numpy
from queue import PriorityQueue
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
    
# return all possible adjacent cells
# This function find_next takes two arguments - current cell and maze
# First, it creates an empty list to store all the adjacent cells
# Then, it checks if the adjacent cells are valid or not
# If the adjacent cells are valid, it adds them to the list. 
# Finally, it returns the list. 
def find_next(currCell, m):
    next_coordinates = []
    possibles = [(-1,0), (0,-1), (1,0) , (0,1)]
    for d in possibles:
        childCell = (currCell[0]+d[0], currCell[1]+d[1])
        if childCell[0] < 0 or childCell[0] >= m.shape[0] or childCell[1] < 0 or childCell[1] >= m.shape[1]:
            continue
        if m[childCell] == 1:
            continue
        next_coordinates.append(childCell)
    return next_coordinates

# get the forward path from the reverse path
def get_fwd_path(revPath, start, goal):
    if goal in revPath:
        fwdPath = []
        cell = goal
        while cell != start:
            fwdPath.insert(0, cell)
            cell = revPath[cell]
        fwdPath.insert(0, start)
        return fwdPath
    else:
        return None
    
# get the start and goal of the maze
def maze_info(maze):
    info = {}
    info["goal"] = []
    for (x, y), element in numpy.ndenumerate(maze):
        if maze[(x,y)] == -1:
            info["start"] = (x,y)
        elif maze[(x,y)] == 2:
            info["goal"].append((x,y))

    return info

# rank all the goals by their distance to the start cell 
def goals_distance(info):
    start = info["start"]    
    goals = info["goal"]
    distance = PriorityQueue()
    for g in goals:
        distance.put((h(start,g), g))
    return distance

# heuristic function
# get the manhattan distance between 2 cells
def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1-x2) + abs(y1-y2)