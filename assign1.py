import numpy
from uninformed_algo import *
from informed_algo import *
from custom_algo import *
import sys

def load_maze(file):
    f = open(file, "r")
    lines = f.readlines()
    f.close()

    info = {}
    rows, cols = eval(lines[0])
    n, m = eval(lines[0])
    start = eval(lines[1])
    goals = [eval(g) for g in lines[2].split('|')]
    walls = [eval(w) for w in lines[3:]]

    # create empty grid
    maze = numpy.zeros((rows, cols))

    try:
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

def visualise_path(path, maze):
    if path is not None:
        for c in path:
            maze[c] = 3
        print(maze) 

        directions = []
        compass = {(0,1): "right", (0,-1): "left", (1,0): "down", (-1,0): "up"}
        
        for i, p in enumerate(path):
            if i > 0:
                dir = tuple(map(lambda i, j: i - j, path[i], path[i-1]))
                directions.append(compass[dir])
        print(directions)
    else:
        print("No path found")


def main(algo):
    # parse the text file to create the maze
    file = "mazes/grid_5.txt"
    # file = "mazes/RobotNav-test.txt"
    maze = load_maze(file)
    # print(maze)
    if maze is not None:
        if algo == 0:
            explored, path = DFS(maze)
        elif algo == 1:
            explored, path = BFS(maze)
        elif algo == 2:
            explored, path = GBFS(maze)
        elif algo == 3:
            explored, path = A_star(maze)
        elif algo == 4:
            explored, path = dijkstra(maze)
        elif algo == 5:
            explored, path = wall_following(maze)

        # print(explored)
        print(path)
        print("Path length: " + str(len(path)))
        print("Explored nodes: " + str(len(explored)))

        visualise_path(path, maze)
    

if __name__ == "__main__":
    algo = int(sys.argv[1])
    main(algo)