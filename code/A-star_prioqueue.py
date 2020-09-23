import numpy as np
import math
from queue import PriorityQueue


def heuristics(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def printMap(mtx_gridnode, width, height):
    for y in range(height):
        for x in range(width):
            gridnode = mtx_gridnode[y, x]
            print(gridnode.get_symbol(), end=" ")
        print('')
    

class GridNode:
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.cur_neighbors = []
        self.symbol = symbol

    def is_start(self):
        return self.symbol == 'S'
    
    def is_end(self):
        return self.symbol == 'E'
    
    def is_block(self):
        return self.symbol == '#'
    
    def is_passable(self):
        return self.symbol == '.'
    
    def get_neighbors(self):
        return self.cur_neighbors
    
    def add_neighbor(self, neighbor):
        self.cur_neighbors.append(neighbor)
        return
    
    def get_coords(self):
        return self.x, self.y
    
    def get_symbol(self):
        return self.symbol

    def set_symbol(self, symbol):
        self.symbol = symbol
        
    # Used for priority queue to allow for a less than comparison
    def __lt__(self, other):
        return False
    
def initializeNeighbors(mtx_gridnode, width, height):
    for y in range(height):
        for x in range(width):
            gridnode = mtx_gridnode[y, x]
            # x + 1
            if x + 1 < width:
                if not mtx_gridnode[y, x+1].is_block():
                    gridnode.add_neighbor(mtx_gridnode[y, x+1])
            
            # x - 1
            if x - 1 >= 0:
                if not mtx_gridnode[y, x-1].is_block():
                    gridnode.add_neighbor(mtx_gridnode[y, x-1])
            
            # y + 1
            if y + 1 < height:
                if not mtx_gridnode[y+1, x].is_block():
                    gridnode.add_neighbor(mtx_gridnode[y+1, x])
            
            # y - 1
            if y - 1 >= 0:
                if not mtx_gridnode[y-1, x].is_block():
                    gridnode.add_neighbor(mtx_gridnode[y-1, x])
                    
    return

def reconstructPath(came_from, current):
    count = 0
    while current in came_from:
        count += 1
        if current.get_symbol() != 'S' and current.get_symbol() != 'E':
            current.set_symbol('*')
        current = came_from[current]
    # return length of path
    return count


def AStarMethod():
    #---------- Initialize Input Matrix -----------
    
    inp_list = []
    with open("input_matrix.txt", "r") as filestream:
        for line in filestream:
            inp_row = line.split(", ")
            inp_row = inp_row[:len(inp_row)-1]
            inp_list.append(inp_row)

    if len(inp_list) == 0:
        return 
    
    height_mtx = len(inp_list)
    width_mtx = len(inp_list[0])
    
    inp_mtx = []
    start = None
    end = None
    
    # Create the grid
    for y in range(height_mtx):
        inp_row = []
        for x in range(width_mtx):
            gridnode = GridNode(x, y, inp_list[y][x])
            if gridnode.is_start():
                start = gridnode
            if gridnode.is_end():
                end = gridnode
            inp_row.append(gridnode)
        inp_mtx.append(inp_row)
    
    inp_mtx = np.array(inp_mtx)
    print("----------- INITIAL MATRIX ------------")
    printMap(inp_mtx, width_mtx, height_mtx)
    
    if start == None or end == None:
        print("Please insert an 'S' for start and 'E' for end")
        return
    
    # initialize the neighbors in the grid
    initializeNeighbors(inp_mtx, width_mtx, height_mtx)
    
    # ------------ Begin A-star Algorithm -----------
    came_from = {}
    
    # A hash array with the gridnodes as a key
    g_score = {gridnode: float("inf") for row in inp_mtx for gridnode in row}
    g_score[start] = 0
    f_score = {gridnode: float("inf") for row in inp_mtx for gridnode in row}
    f_score[start] = heuristics(
        start.get_coords()[0], start.get_coords()[1], end.get_coords()[0],end.get_coords()[0])
    
    # priority queue will take the item with the minimum first value, i.e. the f score
    open_set = PriorityQueue()
    open_set.put((f_score[start], start))
    open_set_hash = {start}
    
    while not open_set.empty():
        # obtains the gridnode with minimum f score
        current = open_set.get()[1]
        open_set_hash.remove(current)
        
        if current == end:
            reconstructPath(came_from, current)
            print("------------ SOLVED MATRIX ------------")
            printMap(inp_mtx, width_mtx, height_mtx)
            return 
            
        for neighbor in current.get_neighbors():
            temp_gscore = g_score[current] + 1
            if temp_gscore < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_gscore
                f_score[neighbor] = g_score[neighbor] + heuristics(
                    neighbor.get_coords()[0], neighbor.get_coords()[1], end.get_coords()[0], end.get_coords()[1])
                if neighbor not in open_set_hash:
                    open_set.put((f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
    
    print("No path possible")
    return
            


if __name__ == "__main__":
    AStarMethod()
