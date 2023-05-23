import numpy
from queue import PriorityQueue

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