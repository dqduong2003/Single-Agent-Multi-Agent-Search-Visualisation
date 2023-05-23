# Author: Daniel Dang - Student ID: 103528453
# Last modified: 19-04-2023

from custom_algo import *
from uninformed_algo import *
from informed_algo import *
from functions import *

# function the find the path to all goals
def updated_algorithms(m, algo):
    m_copy = m.copy()
    info = maze_info(m_copy)
    if "start" in info and "goal" in info:
        remaining_goals = goals_distance(info)

        explored, path = [], []

        while not remaining_goals.empty():
            # start exploring with the closest goal first
            goal = remaining_goals.get()[1]
            if algo == 0:
                temp_explored, temp_path = DFS(m_copy)
            elif algo == 1:
                temp_explored, temp_path = BFS(m_copy)
            elif algo == 2: 
                temp_explored, temp_path = GBFS(m_copy)
            elif algo == 3:
                temp_explored, temp_path = A_star(m_copy)
            elif algo == 4:
                temp_explored, temp_path = dijkstra(m_copy)
            elif algo == 5:
                temp_explored, temp_path = ida_star(m_copy)
            if temp_explored is not None:
                for c in temp_explored:
                    if c not in explored:
                        explored.append(c)
                for c in temp_path:
                    if c not in path:
                        path.append(c)

                m_copy[temp_path[0]] = 1
                m_copy[temp_path[-1]] = -1
        
        return explored, path