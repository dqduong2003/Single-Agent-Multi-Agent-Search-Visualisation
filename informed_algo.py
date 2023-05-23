# Author: Daniel Dang - Student ID: 103528453
# Last modified: 19-04-2023

from queue import PriorityQueue
from functions import *

# Greedy best first search algorithm
def GBFS(m):
    info = maze_info(m)
    if "start" in info and "goal" in info:
        start = info["start"]    
        remaining_goals = goals_distance(info)

        while not remaining_goals.empty():
            # start exploring with the closest goal first
            goal = remaining_goals.get()[1]

            indices = [(i, j) for i in range(m.shape[0]) for j in range(m.shape[1])]
            f_score = {cell:float("inf") for cell in indices}
            f_score[start] = h(start, goal)

            frontier = PriorityQueue()
            frontier.put((h(start, goal), start))
            searchPath = [start]
            gbfsPath = {}

            while not frontier.empty():
                currCell = frontier.get()[1]
                searchPath.append(currCell)
                if currCell == goal:
                    break
                for childCell in find_next(currCell, m):
                    temp_f_score = h(childCell, goal)
                    if temp_f_score < f_score[childCell]:
                        f_score[childCell] = temp_f_score
                        frontier.put((h(childCell, goal), childCell))
                        gbfsPath[childCell] = currCell

            fwdPath = get_fwd_path(gbfsPath, start, goal)
            # return the solution if the path is found
            # if no paths are found, continue with the next nearest goal
            if fwdPath != None:
                return searchPath, fwdPath
    else:
        print("No start or goal found")  
    # if no available paths are found
    return None, None
 

"""
A* search algorithm

Description:
    This function implements the A* search algorithm. The function takes in a maze and returns 2 paths:
        1) The search path that the algorithm took to find the best route
        2) The best route that the algorithm found

Parameters:
    m: A numpy array representing the maze

Returns:
    searchPath: A list of tuples representing the cells that the algorithm visited to find the best path
    fwdPath: A list of tuples representing the best route found by the algorithm
"""

# A* search algorithm
def A_star(m):
    info = maze_info(m)
    if "start" in info and "goal" in info:
        start = info["start"]
        remaining_goals = goals_distance(info)

        while not remaining_goals.empty():
            goal = remaining_goals.get()[1]

            indices = [(i, j) for i in range(m.shape[0]) for j in range(m.shape[1])]
            g_score = {cell:float("inf") for cell in indices}
            g_score[start] = 0
            f_score = {cell:float("inf") for cell in indices}
            f_score[start] = h(start, goal)

            frontier = PriorityQueue()
            frontier.put((f_score[start], h(start, goal), start))
            searchPath = [start]
            aPath = {}

            while not frontier.empty():
                currCell = frontier.get()[2]
                searchPath.append(currCell)
                if currCell == goal:
                    break
                for childCell in find_next(currCell, m):
                    temp_g_score = g_score[currCell] + 1
                    temp_f_score = temp_g_score + h(childCell, goal)

                    if temp_f_score < f_score[childCell]:
                        g_score[childCell] = temp_g_score
                        f_score[childCell] = temp_f_score
                        frontier.put((f_score[childCell], h(childCell, goal), childCell))
                        aPath[childCell] = currCell

            fwdPath = get_fwd_path(aPath, start, goal)
            if fwdPath != None:
                return searchPath, fwdPath
    else:
        print("No start or goal found")
        
    # if no available paths are found
    return None, None

