"""
Graph generation for sipp 
CREDIT: Ashwin Bose (@atb033)
"""

import argparse
import yaml
from bisect import bisect
import sys
import numpy

class State(object):
    def __init__(self, position=(-1,-1), t=0, interval=(0,float('inf'))):
        self.position = tuple(position)
        self.time = t
        self.interval = interval

class SippGrid(object):
    def __init__(self):
        # self.position = ()
        self.interval_list = [(0, float('inf'))]
        self.f = float('inf')
        self.g = float('inf')
        self.parent_state = State()

    def split_interval(self, t, last_t = False):
        """
        Function to generate safe-intervals
        """
        for interval in self.interval_list:
            if last_t:
                if t<=interval[0]:
                    self.interval_list.remove(interval)
                elif t>interval[1]:
                    continue
                else:
                    self.interval_list.remove(interval)
                    self.interval_list.append((interval[0], t-1))
            else:
                if t == interval[0]:
                    self.interval_list.remove(interval)
                    if t+1 <= interval[1]:
                        self.interval_list.append((t+1, interval[1]))
                elif t == interval[1]:
                    self.interval_list.remove(interval)
                    if t-1 <= interval[0]:
                        self.interval_list.append((interval[0],t-1))
                elif bisect(interval,t) == 1:
                    self.interval_list.remove(interval)
                    self.interval_list.append((interval[0], t-1))
                    self.interval_list.append((t+1, interval[1]))
            self.interval_list.sort()

class SippGraph(object):
    def __init__(self, map):
        self.map = map
        self.dimensions = map.shape
        info = maze_info(map)
        obstacles = info['walls']
        self.obstacles = [tuple(v) for v in info['walls']]        
        self.dyn_obstacles = []

        self.sipp_graph = {}
        self.init_graph()
        self.init_intervals()

    def init_graph(self):
        for i in range(self.dimensions[0]):
            for j in range(self.dimensions[1]):
                grid_dict = {(i,j):SippGrid()}
                self.sipp_graph.update(grid_dict)

    def init_intervals(self):
        if not self.dyn_obstacles: return
        for schedule in self.dyn_obstacles.values():
            # for location in schedule:
            for i in range(len(schedule)):
                location = schedule[i]
                last_t = i == len(schedule)-1

                position = (location["x"],location["y"])
                t = location["t"]

                self.sipp_graph[position].split_interval(t, last_t)
                # print(str(position) + str(self.sipp_graph[position].interval_list))     

    def is_valid_position(self, position):
        dim_check = position[0] in range(self.dimensions[0]) and  position[1] in range(self.dimensions[1])
        obs_check = position not in self.obstacles
        # print(dim_check)
        return dim_check and obs_check

    def get_valid_neighbours(self, position):
        neighbour_list = []

        up = (position[0], position[1]+1)
        if self.is_valid_position(up): neighbour_list.append(up)

        down = (position[0], position[1]-1)
        if self.is_valid_position(down): neighbour_list.append(down)

        left = (position[0]-1, position[1])
        if self.is_valid_position(left): neighbour_list.append(left)

        right = (position[0]+1, position[1])
        if self.is_valid_position(right): neighbour_list.append(right)

        return neighbour_list

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
        start = [eval(g) for g in lines[1].split('|')]
        goals = [eval(g) for g in lines[2].split('|')]
        walls = [eval(w) for w in lines[3:]]

        # create empty grid
        maze = numpy.zeros((rows, cols))

        # place start and goals
        # maze[start[1], start[0]] = -1
        # info["start"] = (start[1], start[0])
        # info["goal"] = []
        print(start)
        for x, y in start:
            maze[y, x] = -1
        for x, y in goals:
            maze[y, x] = 2
            # info["goal"].append((y,x))
        
        # place walls
        for x, y, w, h in walls:
            maze[y:y+h, x:x+w] = 1

        # print(maze)
        return maze
    except:
        print("Invalid file format")
        return None
    
def maze_info(maze):
    info = {}
    info["start"] = []
    info["goal"] = []
    info["agents"] = []
    info["walls"] = []
    for (x, y), element in numpy.ndenumerate(maze):
        if maze[(x,y)] == -1:
            info["start"].append((x,y))
        elif maze[(x,y)] == 2:
            info["goal"].append((x,y))
        elif maze[(x,y)] == 1:
            info["walls"].append((x,y))
    if len(info["start"]) != len(info["goal"]):
        raise ValueError("Number of start and goal cells do not match")
    for i in range(len(info["start"])):
        info["agents"].append({'start': info["start"][i], 'goal': info["goal"][i], 'name': f'agent{i}'})
        
    return info

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("map", help="input file containing map and dynamic dyn_obstacles")
    args = parser.parse_args()
    
    with open(args.map, 'r') as map_file:
        try:
            map = yaml.load(map_file, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)

    graph = SippGraph(map)

if __name__ == "__main__":
    main()

