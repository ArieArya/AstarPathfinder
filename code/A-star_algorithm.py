import numpy as np
import math

def calcDistEnd(x, y, end_x, end_y):
    return round(math.sqrt((end_x-x)**2 + (end_y-y)**2))

def updateDistMtx(cur_x, cur_y, inp_mtx, dist_mtx, visit_mtx, gcost_mtx, mtx_width, mtx_height, end_x, end_y):
    # x + 1
    if cur_x < mtx_width - 1 and inp_mtx[cur_y,cur_x+1] != '#':
        if visit_mtx[cur_y, cur_x+1] == False:
            if gcost_mtx[cur_y, cur_x+1] >= gcost_mtx[cur_y, cur_x] + 1:
                gcost_mtx[cur_y, cur_x+1] = gcost_mtx[cur_y, cur_x] + 1
                dist_mtx[cur_y, cur_x+1] = gcost_mtx[cur_y, cur_x+1] + calcDistEnd(cur_x+1, cur_y, end_x, end_y)
            
            
    # x - 1
    if cur_x > 0 and inp_mtx[cur_y, cur_x-1] != '#':
        if visit_mtx[cur_y, cur_x-1] == False:
            if gcost_mtx[cur_y, cur_x-1] >= gcost_mtx[cur_y, cur_x] + 1:
                gcost_mtx[cur_y, cur_x-1] = gcost_mtx[cur_y, cur_x] + 1
                dist_mtx[cur_y, cur_x-1] = gcost_mtx[cur_y, cur_x-1] + calcDistEnd(cur_x-1, cur_y, end_x, end_y)
            
    # y + 1
    if cur_y < mtx_height - 1 and inp_mtx[cur_y + 1, cur_x] != '#':
        if visit_mtx[cur_y+1, cur_x] == False:
            if gcost_mtx[cur_y+1, cur_x] >= gcost_mtx[cur_y, cur_x] + 1:
                gcost_mtx[cur_y+1, cur_x] = gcost_mtx[cur_y, cur_x] + 1
                dist_mtx[cur_y+1, cur_x] = gcost_mtx[cur_y+1, cur_x] + calcDistEnd(cur_x, cur_y+1, end_x, end_y)

    # y - 1
    if cur_y > 0 and inp_mtx[cur_y - 1, cur_x] != '#':
        if visit_mtx[cur_y-1, cur_x] == False:
            if gcost_mtx[cur_y-1, cur_x] >= gcost_mtx[cur_y, cur_x] + 1:
                gcost_mtx[cur_y-1, cur_x] = gcost_mtx[cur_y, cur_x] + 1
                dist_mtx[cur_y-1, cur_x] = gcost_mtx[cur_y-1, cur_x] + calcDistEnd(cur_x, cur_y-1, end_x, end_y)
            
def findMinDistPoint(dist_mtx, visit_mtx, mtx_width, mtx_height):
    min_point = float("inf")
    next_x = 0
    next_y = 0
    for i in range(mtx_width):
        for k in range(mtx_height):
            if visit_mtx[k, i] == False:
                if dist_mtx[k, i] < min_point:
                    min_point = dist_mtx[k, i]
                    next_x = i
                    next_y = k
    return next_x, next_y

def backtrackPoint(cur_x, cur_y, coord_traversed, inp_mtx, dist_mtx, gcost_mtx, mtx_width, mtx_height):
    min_point = float("inf")
    next_x = cur_x
    next_y = cur_y
    # x + 1
    if cur_x < mtx_width - 1 and inp_mtx[cur_y, cur_x+1] != '#' and [cur_x+1, cur_y] not in coord_traversed:
        if dist_mtx[cur_y, cur_x+1] < min_point:
            min_point = dist_mtx[cur_y, cur_x+1]
            next_x = cur_x+1
            next_y = cur_y

    # x - 1
    if cur_x > 0 and inp_mtx[cur_y, cur_x-1] != '#' and [cur_x-1, cur_y] not in coord_traversed:
        if dist_mtx[cur_y, cur_x-1] < min_point:
            min_point = dist_mtx[cur_y, cur_x-1]
            next_x = cur_x-1
            next_y = cur_y
        elif dist_mtx[cur_y, cur_x-1] == min_point:
            if gcost_mtx[cur_y, cur_x-1] < gcost_mtx[next_y, next_x]:
                min_point = dist_mtx[cur_y, cur_x-1]
                next_x = cur_x-1
                next_y = cur_y

    # y + 1
    if cur_y < mtx_height - 1 and inp_mtx[cur_y + 1, cur_x] != '#' and [cur_x, cur_y+1] not in coord_traversed:
        if dist_mtx[cur_y+1, cur_x] < min_point:
            min_point = dist_mtx[cur_y+1, cur_x]
            next_x = cur_x
            next_y = cur_y+1
        elif dist_mtx[cur_y+1, cur_x] == min_point:
            if gcost_mtx[cur_y+1, cur_x] < gcost_mtx[next_y, next_x]:
                min_point = dist_mtx[cur_y+1, cur_x]
                next_x = cur_x
                next_y = cur_y+1

    # y - 1
    if cur_y > 0 and inp_mtx[cur_y - 1, cur_x] != '#' and [cur_x, cur_y-1] not in coord_traversed:
        if dist_mtx[cur_y-1, cur_x] < min_point:
            min_point = dist_mtx[cur_y-1, cur_x]
            next_x = cur_x
            next_y = cur_y-1
        elif dist_mtx[cur_y-1, cur_x] == min_point:
            if gcost_mtx[cur_y-1, cur_x] < gcost_mtx[next_y, next_x]:
                min_point = dist_mtx[cur_y-1, cur_x]
                next_x = cur_x
                next_y = cur_y-1
    
    return next_x, next_y

def AStarMethod():
    inp_list = []

    with open("input_matrix.txt", "r") as filestream:
        for line in filestream:
            inp_row = line.split(", ")
            inp_row = inp_row[:len(inp_row)-1]
            inp_list.append(inp_row)

    inp_mtx = np.array(inp_list)
    
    print("---------- INITIAL MATRIX ---------")
    print(inp_mtx)
    
    mtx_height = len(inp_mtx[:, 0])
    mtx_width = len(inp_mtx[0, :])

    start_point = np.where(inp_mtx == 'S')
    start_y = start_point[0][0]
    start_x = start_point[1][0]

    end_point = np.where(inp_mtx == 'E')
    end_y = end_point[0][0]
    end_x = end_point[1][0]

    # store numpy distances list
    dist_mtx = np.zeros((mtx_height, mtx_width))
    gcost_mtx = np.zeros((mtx_height, mtx_width))

    # initialize with an infinite distance
    dist_mtx += float("inf")
    gcost_mtx += float("inf")

    # store numpy visited list
    visit_mtx = np.zeros((mtx_height, mtx_width))
    visit_mtx[visit_mtx == 0] = False

    # initialize starting position
    gcost_mtx[start_y, start_x] = 0
    dist_mtx[start_y, start_x] = 0
    visit_mtx[start_y, start_x] = True
    ###
    cur_x = start_x
    cur_y = start_y

    # move forward and track all nodes
    counter = 0
    while cur_x != end_x or cur_y != end_y:
        counter += 1
        visit_mtx[cur_y, cur_x] = True
        updateDistMtx(cur_x, cur_y, inp_mtx, dist_mtx, visit_mtx,
                      gcost_mtx, mtx_width, mtx_height, end_x, end_y)
        cur_x, cur_y = findMinDistPoint(
            dist_mtx, visit_mtx, mtx_width, mtx_height)
        if counter > mtx_height * mtx_width:
            return "no path possible"    

    # trace backwards
    coord_traversed = []
    coord_traversed.append([cur_x, cur_y])
    cur_x, cur_y = backtrackPoint(
        cur_x, cur_y, coord_traversed, inp_mtx, dist_mtx, gcost_mtx, mtx_width, mtx_height)
    while cur_x != start_x or cur_y != start_y:
        coord_traversed.append([cur_x, cur_y])
        inp_mtx[cur_y, cur_x] = '*'
        cur_x, cur_y = backtrackPoint(
            cur_x, cur_y, coord_traversed, inp_mtx, dist_mtx, gcost_mtx, mtx_width, mtx_height)
        
    print("---------- SOLVED MATRIX ----------")
    print(inp_mtx)
    return inp_mtx

    
if __name__ == "__main__":
    AStarMethod()


    
    
    
    
    
    




