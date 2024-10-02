# Author: Daniel Dang - Student ID: 103528453
# Last modified: 19-04-2023

from functions import *    

# Depth-first search algorithm
def DFS(m):
    info = maze_info(m)
    if "start" in info and "goal" in info:
        start = info["start"]
        explored = [start]
        frontier = [start]
        dfsPath = {}

        while len(frontier) > 0:
            currCell = frontier.pop()
            if currCell in info["goal"]: 
                break
            for childCell in find_next(currCell, m):
                if childCell in explored:
                    continue
                explored.append(childCell)
                frontier.append(childCell)
                dfsPath[childCell] = currCell
        
        goal = (-1,-1)
        for c in dfsPath.keys():
            if c in info["goal"]:
                goal = c
                break
        if goal != (-1, -1):
            fwdPath = get_fwd_path(dfsPath, start, goal)
            return explored, fwdPath
        
        # no goal found
        else:
            return explored, None
    else:
        print("No start or goal found")
    return None, None

    
# Breadth-first search algorithm
def BFS(m):
    info = maze_info(m)
    if "start" in info and "goal" in info:
        start = info["start"]
        explored = [start]
        frontier = [start]
        bfsPath = {}

        while len(frontier) > 0:
            currCell = frontier.pop(0)
            if currCell in info["goal"]:
                break
            for childCell in find_next(currCell, m):
                if childCell in explored:
                    continue
                explored.append(childCell)
                frontier.append(childCell)
                bfsPath[childCell] = currCell
        
        goal = (-1,-1)
        for c in bfsPath.keys():
            if c in info["goal"]:
                goal = c
                break
        if goal != (-1, -1):
            fwdPath = get_fwd_path(bfsPath, start, goal)
            return explored, fwdPath
        
        # no goal found
        else:
            return explored, None
    else:
        print("No start or goal found")

    return None, None
