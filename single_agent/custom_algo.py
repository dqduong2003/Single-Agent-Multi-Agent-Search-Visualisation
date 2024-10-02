# Author: Daniel Dang - Student ID: 103528453
# Last modified: 19-04-2023

from functions import *
import time

# Dijkstra algorithm
def dijkstra(m):
    info = maze_info(m)
    if "start" in info and "goal" in info:
        start = info["start"]    

        indices = [(i, j) for i in range(m.shape[0]) for j in range(m.shape[1])]
        unvisited = {cell:float("inf") for cell in indices}
        unvisited[start] = 0
        dijkPath = {}

        visited = {}
        while unvisited:
            currCell = min(unvisited, key=unvisited.get)
            visited[currCell] = unvisited[currCell]
            if currCell in info["goal"]:
                break
            for childCell in find_next(currCell, m):
                if childCell in visited:
                    continue
                tempDist = unvisited[currCell] + 1

                if tempDist < unvisited[childCell]:
                    unvisited[childCell] = tempDist
                    dijkPath[childCell] = currCell
            unvisited.pop(currCell)

        goal = (-1,-1)
        for c in dijkPath.keys():
            if c in info["goal"]:
                goal = c
                break
        if goal != (-1, -1):
            fwdPath = get_fwd_path(dijkPath, start, goal)
            return visited, fwdPath
        
        # no goal found
        else:
            return visited, None

        return visited, fwdPath
    else:
        print("No start or goal found")
    return None, None

def ida_star(m, timeout=5):
    start_time = time.time()

    def check_timeout():
        return time.time() - start_time > timeout
    
    info = maze_info(m)
    if "start" in info and "goal" in info:
        start = info["start"]    
        remaining_goals = goals_distance(info)

        while not remaining_goals.empty():
            # start exploring with the closest goal first
            goal = remaining_goals.get()[1]

            def dfs(currCell, g, bound, idaPath, searchPath):
                if check_timeout():
                    return "TIMEOUT", idaPath, searchPath

                f = g + h(currCell, goal)
                if f > bound:
                    return f, idaPath, searchPath
                if currCell not in searchPath:
                    searchPath.append(currCell)
                if currCell == goal:
                    return "FOUND", idaPath, searchPath
                
                min_cost = float("inf")
                for childCell in find_next(currCell, m):
                    cost, idaPath, searchPath = dfs(childCell, g + 1, bound, idaPath, searchPath)
                    idaPath[childCell] = currCell
                    # print(idaPath)
                    if cost == "FOUND":
                        return "FOUND", idaPath, searchPath
                    if cost != "TIMEOUT":
                        min_cost = min(min_cost, cost)
                return min_cost, idaPath, searchPath
                    
            # Run IDA* algorithm
            bound = h(start, goal)
            idaPath = {}
            searchPath = []
            while True:
                cost, idaPath, searchPath = dfs(start, 0, bound, idaPath, searchPath)
                if cost == "FOUND":
                    fwdPath = get_fwd_path(idaPath, start, goal)
                    return searchPath, fwdPath
                elif cost == float("inf"):
                    print("infinite cost")
                    break
                elif cost == "TIMEOUT":
                    print("Timeout")
                    return None, None
                else:
                    bound = cost

            if check_timeout():
                print("Timeout")
                return None, None

    else:
        print("No start or goal found")  
    # if no available paths are found
    return None, None

