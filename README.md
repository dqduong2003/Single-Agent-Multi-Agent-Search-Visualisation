# Maze Search Algorithms Visualisation
![Screenshot](screenshots/demo.jpg)

## Algorithms:
* Depth-First Search (DFS)
* Breadth-First Search (BFS)
* A* Search
* Greedy Best First Search (GBFS)
* Dijkstra's Algorithm
* Iterative Deepening A*

# Search Algorithms' Performance Evaluation
## Experimental Setup
In this study, my aim was to evaluate the performance of various search algorithms on 100 different mazes, generated using _Randomized Prim's Algorithm_. Each maze had a random width and height ranging from 30 to 60 cells, a start cell, and 1 to 3 randomly placed goal cells. The performance of the algorithms was assessed based on three metrics: **path length**, **explored cells**, and **execution time**.

## Results
### Path Length
![Screenshot](screenshots/path.png)\
The results of the experiment indicate that DFS algorithm had the longest average path length among the six algorithms tested, with an average of 81.14 cells. This is likely due to the nature of DFS, which explores a single path as far as possible before backtracking and exploring another path. This means that DFS is susceptible to getting trapped in local minimums and taking longer paths as it doesn't take into account the distance from the starting point to the current node. On the other hand, the other algorithms (BFS, GBFS, A*, Dijkstra, IDA*) use heuristics and/or distance calculations to determine the optimal path, resulting in shorter average path lengths of 71.6 cells. Although GBFS does not always guarantee the shortest path, for my generated maze, GBFS shows similar performance with other informed searches. Therefore, the results suggest that these algorithms are more effective than DFS for solving mazes with respect to finding the shortest path.

### Explored Cells
![Screenshot](screenshots/explored.png)\
The results suggest that DFS and BFS algorithms expand a significantly larger number of cells as compared to informed search algorithms such as GBFS, A*, and IDA*. This is because DFS and BFS are blind search algorithms that explore the search tree exhaustively without using any heuristic information, resulting in a large number of expanded cells. In contrast, informed search algorithms such as GBFS, A*, and IDA* use heuristic information to guide the search towards the goal, which helps in reducing the number of explored cells. Dijkstra's algorithm, on the other hand, is not an informed search algorithm, but rather a weighted graph search algorithm that explores the graph in a breadth-first manner. Although it guarantees to find the optimal path, it explores all nodes uniformly, including those that are not promising, leading to a higher number of expanded cells than the informed algorithms that use heuristics.

### Execution Time
![Screenshot](screenshots/time.png)\
DFS, GBFS, and A* algorithms have relatively similar execution times, while BFS has a slightly longer execution time. Dijkstra's algorithm has a significantly higher execution time than the other algorithms, while IDA* has the highest execution time among all the algorithms tested. The higher execution time for Dijkstra's algorithm may be attributed to its need to explore all the nodes uniformly to guarantee to find the optimal solution. On the other hand, the higher execution time for IDA* may be due to the fact that it uses iterative deepening, which repeatedly applies the depth-first search until the solution is found, leading to a higher number of iterations and a longer execution time. Overall, the results suggest that informed search algorithms such as GBFS and A* are more efficient in terms of execution time compared to blind search algorithms such as DFS and BFS, while Dijkstra and IDA* may be more suitable for specific applications that require finding the optimal solution.
