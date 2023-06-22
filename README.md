# Maze Search Algorithms Visualisation
![Screenshot](screenshots/capture1.png)

## Algorithms:
* Depth-First Search (DFS)
* Breadth-First Search (BFS)
* A* Search
* Greedy Best First Search (GBFS)
* Dijkstra's Algorithm
* Iterative Deepening A*

## Instructions:
### Console-based version
1. Open the terminal/command prompt.
2. Navigate to the directory where the **assign1.exe** file is located.
3. For Windows users, use the following command in the terminal:
   ```
   .\assign1.exe <filename> <algorithm>
   ```
   Here, <filename> should be one of the files in the "mazes" folder, and <algorithm> should be one of the search algorithms: DFS, BFS, A*, GBFS, Dijkstra, or IDA*.\
   For example:
   ```
   .\assign1.exe RobotNav-test.txt dfs
   ```
   The program will output the maze encoded by numbers, followed by the solution and the solved maze. The solution will be displayed in the following format:
   ```
   filename method number_of_nodes
   path
   ```
Here, _number_of_nodes_ refers to the number of nodes in the search tree, and _path_ is a sequence of moves that goes from the start to the goal cell.\
Please ensure that the _<filename>_ includes the ".txt" extension, and the <algorithm> is case-insensitive (e.g., bfs or BFS are both acceptable). If you want to test the program with other text files, please place them in the "mazes" folder.\
If no path is found, the program will display **"No path found"**.

### GUI version
Run **assign1_gui.exe** or navigate to the folder and type _.\assign1_gui.exe_ in the terminal to run it.\
On the left is a maze with labels for each colour representing the start, the goal, the wall, the discovered cells, and the path. The ”**Load Maze**” button allows you to import a .txt file with a particular format. ”**Random Maze**” will generate a maze at random for the program.\
When an algorithm is selected, the discovered cells will initially be drawn in grey. After locating the goal cell, an orange path will be drawn from the starting point to the target.
![Screenshot](screenshots/capture2.png)
![Screenshot](screenshots/capture3.png)
The number of cells explored and the length of each algorithm’s path will be displayed in the bottom-right corner of the program.\
**NOTE:** The program will not respond when the path is being drawn to the screen, please wait until everything has been displayed to proceed with the next action.

# Search Algorithms' Performance Evaluation
## Experimental Setup
In this study, my aim was to evaluate the performance of various search algorithms on 100 different mazes, generated using _Randomized Prim's Algorithm_. Each maze had a random width and height ranging from 30 to 60 cells, a start cell, and 1 to 3 randomly placed goal cells. The performance of the algorithms was assessed based on three metrics: **path length**, **explored cells**, and **execution time**.

## Results
### Path Length
![Screenshot](screenshots/path.png)\
The experiment results indicate that DFS algorithm had the longest average path length among the six algorithms tested, with an average of 81.14 cells. This is likely due to the nature of DFS, which explores a single path as far as possible before backtracking and exploring another path. This means that DFS is susceptible to getting trapped in local minimums and taking longer paths as it doesn't take into account the distance from the starting point to the current node. On the other hand, the other algorithms (BFS, GBFS, A*, Dijkstra, IDA*) use heuristics and/or distance calculations to determine the optimal path, resulting in shorter average path lengths of 71.6 cells. Although GBFS does not always guarantee the shortest path, for my generated maze, GBFS shows similar performance with other informed searches. Therefore, the results suggest that these algorithms are more effective than DFS for solving mazes with respect to finding the shortest path.

### Explored Cells
![Screenshot](screenshots/explored.png)\
The results suggest that DFS and BFS algorithms expand a significantly larger number of cells as compared to informed search algorithms such as GBFS, A*, and IDA*. This is because DFS and BFS are blind search algorithms that explore the search tree exhaustively without using any heuristic information, resulting in a large number of expanded cells. In contrast, informed search algorithms such as GBFS, A*, and IDA* use heuristic information to guide the search towards the goal, which helps in reducing the number of explored cells. Dijkstra's algorithm, on the other hand, is not an informed search algorithm, but rather a weighted graph search algorithm that explores the graph in a breadth-first manner. Although it guarantees to find the optimal path, it explores all nodes uniformly, including those that are not promising, leading to a higher number of expanded cells than the informed algorithms that use heuristics.

### Execution Time
![Screenshot](screenshots/time.png)\
DFS, GBFS, and A* algorithms have relatively similar execution times, while BFS has a slightly longer execution time. Dijkstra's algorithm has a significantly higher execution time than the other algorithms, while IDA* has the highest execution time among all the algorithms tested. The higher execution time for Dijkstra's algorithm may be attributed to its need to explore all the nodes uniformly to guarantee finding the optimal solution. On the other hand, the higher execution time for IDA* may be due to the fact that it uses iterative deepening, which repeatedly applies the depth-first search until the solution is found, leading to a higher number of iterations and a longer execution time. Overall, the results suggest that informed search algorithms such as GBFS and A* are more efficient in terms of execution time compared to blind search algorithms such as DFS and BFS, while Dijkstra and IDA* may be more suitable for specific applications that require finding the optimal solution.
