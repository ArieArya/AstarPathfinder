# A-star Pathfinding Algorithm and Visualization

The A-star algorithm is a graph traversal and pathfinding algorithm commonly used due to its optimal complexity. The algorithm utilizes both the path cost as well as heuristics (information of distance to the goal node) to guide its search. In short, the algorithm selects and explores nodes which minimizes the function below:

<h3><i>f(n) = h(n) + g(n)</i></h3>

h(n) is the heuristic function, and estimates the distance of the current node to the goal node. In the case of a 2D matrix, a simple Euclidian distance can be used for this estimation. g(n) is simply the cost of the path from the start node to the current node. The sum of these two costs make up f(n), known as the f-cost.

Typically, the A-star algorithm is implemented using a priority queue for more optimal search time (to more effectively select nodes with minimum f-costs), but due to the smaller scope of this project, such a priority queue is not used.

The rules for this algorithm are as follows:
- From each node, you can move up, down, left, right, but not diagonally
- You cannot traverse through obstacle (black) nodes
- If a path is possible, the shortest path will be displayed once it is found

An example of the algorithm in action is shown below:

<img src='/images/initial.JPG' width="40%">

The green nodes represent the start and end nodes. Once you press space bar to start the algorithm, an optimal path will be found.

<img src='/images/completed.JPG' width="40%">

The dark blue nodes represents the nodes that have been visited by the algorithm, whilst the red nodes represent the shortest path from the start to end nodes.

The raw algorithm without the visualization using pygames is given in the script A-star_algorithm.py, and its input matrix can be initialized in the text file input_matrix.txt. The output of this will simply show the initial 2D matrix and the solved 2D matrix with the shortest path marked with '*'.

<img src='/images/raw_algorithm.JPG' width="40%">
