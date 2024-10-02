"""
Extension of SIPP to multi-robot scenarios
CREDIT: Ashwin Bose (@atb033)
"""

import argparse
import yaml
from math import fabs
from graph_generation import SippGraph, load_maze, maze_info, State
# from sipp import SippPlanner
# import sys

class SippPlanner(SippGraph):
    def __init__(self, map, agent_id):
        info = maze_info(map)
        dimension = map.shape
        obstacles = info['walls']
        self.agents = info['agents']

        SippGraph.__init__(self, map)
        self.start = tuple(self.agents[agent_id]["start"])
        self.goal = tuple(self.agents[agent_id]["goal"])
        self.name = self.agents[agent_id]["name"]
        self.open = []

    def get_successors(self, state):
        successors = []
        m_time = 1
        neighbour_list = self.get_valid_neighbours(state.position)

        for neighbour in neighbour_list:
            start_t = state.time + m_time
            end_t = state.interval[1] + m_time
            for i in self.sipp_graph[neighbour].interval_list:
                if i[0] > end_t or i[1] < start_t:
                    continue
                time = max(start_t, i[0]) 
                s = State(neighbour, time, i)
                successors.append(s)
        return successors

    def get_heuristic(self, position):
        return fabs(position[0] - self.goal[0]) + fabs(position[1]-self.goal[1])

    def compute_plan(self):
        self.open = []
        goal_reached = False
        cost = 1

        s_start = State(self.start, 0) 

        self.sipp_graph[self.start].g = 0.
        f_start = self.get_heuristic(self.start)
        self.sipp_graph[self.start].f = f_start

        self.open.append((f_start, s_start))

        while (not goal_reached):
            if self.open == {}: 
                # Plan not found
                return 0
            s = self.open.pop(0)[1]
            successors = self.get_successors(s)
    
            for successor in successors:
                if self.sipp_graph[successor.position].g > self.sipp_graph[s.position].g + cost:
                    self.sipp_graph[successor.position].g = self.sipp_graph[s.position].g + cost
                    self.sipp_graph[successor.position].parent_state = s

                    if successor.position == self.goal:
                        print("Plan successfully calculated!!")
                        goal_reached = True
                        break

                    self.sipp_graph[successor.position].f = self.sipp_graph[successor.position].g + self.get_heuristic(successor.position)
                    self.open.append((self.sipp_graph[successor.position].f, successor))

        # Tracking back
        start_reached = False
        self.plan = []
        current = successor
        while not start_reached:
            self.plan.insert(0,current)
            if current.position == self.start:
                start_reached = True
            current = self.sipp_graph[current.position].parent_state
        return 1
            
    def get_plan(self):
        path_list = []

        # first setpoint
        setpoint = self.plan[0]
        temp_dict = (setpoint.position[0], setpoint.position[1])
        path_list.append(temp_dict)

        for i in range(len(self.plan)-1):
            for j in range(self.plan[i+1].time - self.plan[i].time-1):
                x = self.plan[i].position[0]
                y = self.plan[i].position[1]
                t = self.plan[i].time
                setpoint = self.plan[i]
                temp_dict = {"x":x, "y":y, "t":t+j+1}
                path_list.append(temp_dict)

            setpoint = self.plan[i+1]
            temp_dict = (setpoint.position[0], setpoint.position[1])
            path_list.append(temp_dict)

        data = {self.name:path_list}
        return data


class MultiSipp(object):
    def __init__(self, maze):
        self.maze = maze
        self.info = maze_info(maze)
        self.agents = self.info['agents']

    def search(self):
        output = dict()

        for i in range(len(self.agents)):
            sipp_planner = SippPlanner(self.maze, i)
        
            if sipp_planner.compute_plan():
                plan = sipp_planner.get_plan()
                output.update(plan)
            else: 
                print("Plan not found")

        return output
    
def main():
    maze = load_maze("../mazes/grid_5.txt")
    multi_sipp = MultiSipp(maze)
    output = multi_sipp.search()

    print(output)
if __name__ == "__main__":
    

    main()
