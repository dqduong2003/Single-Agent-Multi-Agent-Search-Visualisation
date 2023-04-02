import numpy

# return all possible adjacent cells
def find_next(currCell, m):
    next_coordinates = []
    possibles = [(0,-1), (0,1), (1,0) , (-1,0)]
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
    # goal = numpy.where(maze == -1)
    # info["start"] = (goal[0][0], goal[1][0])
    info["goal"] = []

    # twos = numpy.where(maze == 2)
    # for c in twos:
    #     info["goal"].append(tuple(c[::-1]))
    # print(info)
    for (x, y), element in numpy.ndenumerate(maze):
        if maze[(x,y)] == -1:
            info["start"] = (x,y)
        elif maze[(x,y)] == 2:
            info["goal"].append((x,y))

    return info
