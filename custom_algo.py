from functions import *

# Dijkstra algorithm
def dijkstra(m):
    info = maze_info(m)
    start = info["start"]    

    indices = [(i, j) for i in range(m.shape[0]) for j in range(m.shape[1])]
    unvisited = {cell:float("inf") for cell in indices}
    unvisited[start] = 0
    revPath = {}

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
                revPath[childCell] = currCell
        unvisited.pop(currCell)

    goal = (0,0)
    for c in revPath.keys():
        if c in info["goal"]:
            goal = c
            break
    fwdPath = get_fwd_path(revPath, start, goal)

    return visited, fwdPath

def Tremaux(m, info):
    start = info["start"]
    goal = info["goal"][0]
    explored = {start: 1}
    tremaux_path = {start: None}
    currCell = start

    while currCell != goal:
        unexplored = []
        for childCell in find_next(currCell, m):
            if childCell not in explored:
                unexplored.append(childCell)
        if len(unexplored) > 0:
            # Move to an unexplored cell
            nextCell = unexplored.pop(0)
            explored[nextCell] = 1
            tremaux_path[nextCell] = currCell
            currCell = nextCell
        else:
            # Backtrack to a cell with unexplored neighbors
            backtrack = None
            for childCell in find_next(currCell, m):
                if childCell in explored and explored[childCell] == 1:
                    if len(find_next(childCell, m)) > 1:
                        if backtrack is None or explored[childCell] < explored[backtrack]:
                            backtrack = childCell
            if backtrack is None:
                break
            currCell = backtrack

    # Build the path from start to goal
    if goal in tremaux_path:
        fwdPath = []
        cell = goal
        while cell is not None:
            fwdPath.insert(0, cell)
            cell = tremaux_path[cell]
        return list(explored.keys()), fwdPath
    else:
        return list(explored.keys()), None


def wall_following(m, info):
    direction = {"forward": (-1,0), "left": (1,0), "back": (1,0), "right": (-1,0)}
    currCell = info["start"]
    path = []

    while True:
        if currCell in info["goal"]:
            break
        available_cells = find_next(currCell, m)
        if (currCell[0]+direction["left"][0], currCell[1]+direction["left"][1]) not in available_cells:
            if (currCell[0]+direction["forward"][0], currCell[1]+direction["forward"][1]) not in available_cells:
                direction = RCW(direction)
            else:
                currCell = moveForward(direction, currCell)
                path.append(currCell)
                direction = {"forward": (-1,0), "left": (1,0), "back": (1,0), "right": (-1,0)}

        else:
            direction = RCCW(direction)
            currCell = moveForward(direction, currCell)
            path.append(currCell)
            direction = {"forward": (-1,0), "left": (1,0), "back": (1,0), "right": (-1,0)}

    return path, path

def RCW(direction):
    k = list(direction.keys())
    v = list(direction.values())
    v_rotated = [v[-1]] + v[:-1]
    direction = dict(zip(k, v_rotated))
    return direction


def RCCW(direction):
    k = list(direction.keys())
    v = list(direction.values())
    v_rotated = v[1:] + [v[0]]
    direction = dict(zip(k, v_rotated))
    return direction


def moveForward(direction, cell):
    return (cell[0]+direction["forward"][0], cell[1]+direction["forward"][1])
    # if direction["forward"] == (-1,0):
    #     return (cell[0], cell[1]+1)
    # if direction["forward"] == "left":
    #     return (cell[0], cell[1]-1)
    # if direction["forward"] == "up":
    #     return (cell[0]-1, cell[1])
    # if direction["forward"] == "down":
    #     return (cell[0]+1, cell[1])


