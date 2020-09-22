import pygame
import math
import numpy as np

# Initialize global variables
WIDTH = 900
DARK_BLUE = (58, 145, 181)
LIGHT_BLUE = (129, 198, 227)
DARK_GREEN = (64, 125, 88)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_GREEN = (96, 224, 147)
GREY = (128, 128, 128)
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding with A* Algorithm")

# Define class for each colored block
class Block:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.width = width
        
        # starting position of the drawn cubes
        self.x = row * width
        self.y = col * width
        
        # initialize all blocks to white
        self.color = WHITE
        self.font = pygame.font.Font('freesansbold.ttf', 10)
        self.score = ''
        
    def set_score(self, score):
        self.score = score
    
    def get_pos(self):
        return self.col, self.row
    
    def is_visited(self):
        return self.color == DARK_BLUE
    
    def is_checked(self):
        return self.color == LIGHT_BLUE

    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == LIGHT_GREEN

    def is_end(self):
        return self.color == DARK_GREEN

    def reset(self):
        self.color = WHITE
        
    def make_start(self):
        self.color = LIGHT_GREEN
        
    def make_visited(self):
        if not self.is_start() and not self.is_end():
            self.color = DARK_BLUE
        
    def make_checked(self):
        if not self.is_start() and not self.is_end():
            self.color = LIGHT_BLUE
    
    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = DARK_GREEN
        
    def make_path(self):
        self.color = RED
        
    # draw the cube
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        text_surface = self.font.render(self.score, True, WHITE, None)
        text_rect = (self.x + 0.4*(self.width), self.y + 0.4*(self.width))
        win.blit(text_surface, text_rect)

# initialize the grid  
def make_grid(num_rows, width):
    grid = []
    gap = width // num_rows
    for i in range(num_rows):
        grid.append([])
        for j in range(num_rows):
            block = Block(i, j, gap)
            grid[i].append(block)
    
    return grid

def draw_grid(win, num_rows, width):
    gap = width // num_rows
    for i in range(num_rows):
        # draw a horizontal line to separate every row
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        
    for j in range(num_rows):
        # draw a vertical line to separate every column
        pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

# draw the grids and each spots
def draw(win, grid, num_rows, width):
    win.fill(WHITE)
    
    for row in grid:
        for block in row:
            block.draw(win)
            
    draw_grid(win, num_rows, width)
    pygame.display.update()
    
# helper function to return row and col number from coordinates
def get_clicked_pos(pos, num_rows, width):
    gap = width // num_rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

# ---------------------------- Main Functions for the A-Star Algorithm ----------------------------
def calcDistEnd(x, y, end_x, end_y):
    return round(math.sqrt((end_x-x)**2 + (end_y-y)**2))


def updateDistMtx(cur_x, cur_y, inp_mtx, dist_mtx, visit_mtx, gcost_mtx, mtx_width, mtx_height, end_x, end_y):
    # x + 1
    if cur_x < mtx_width - 1 and not inp_mtx[cur_y, cur_x+1].is_barrier():
        if visit_mtx[cur_y, cur_x+1] == False:
            inp_mtx[cur_y, cur_x+1].make_checked()
            if gcost_mtx[cur_y, cur_x+1] >= gcost_mtx[cur_y, cur_x] + 1:
                gcost_mtx[cur_y, cur_x+1] = gcost_mtx[cur_y, cur_x] + 1
                dist_mtx[cur_y, cur_x+1] = gcost_mtx[cur_y, cur_x+1] + \
                    calcDistEnd(cur_x+1, cur_y, end_x, end_y)
                inp_mtx[cur_y, cur_x+1].set_score(str(int(dist_mtx[cur_y, cur_x+1])))

    # x - 1
    if cur_x > 0 and not inp_mtx[cur_y, cur_x-1].is_barrier():
        if visit_mtx[cur_y, cur_x-1] == False:
            inp_mtx[cur_y, cur_x-1].make_checked()
            if gcost_mtx[cur_y, cur_x-1] >= gcost_mtx[cur_y, cur_x] + 1:
                gcost_mtx[cur_y, cur_x-1] = gcost_mtx[cur_y, cur_x] + 1
                dist_mtx[cur_y, cur_x-1] = gcost_mtx[cur_y, cur_x-1] + \
                    calcDistEnd(cur_x-1, cur_y, end_x, end_y)
                inp_mtx[cur_y, cur_x-1].set_score(str(int(dist_mtx[cur_y, cur_x-1])))
                
    # y + 1
    if cur_y < mtx_height - 1 and not inp_mtx[cur_y + 1, cur_x].is_barrier():
        if visit_mtx[cur_y+1, cur_x] == False:
            inp_mtx[cur_y+1, cur_x].make_checked()
            if gcost_mtx[cur_y+1, cur_x] >= gcost_mtx[cur_y, cur_x] + 1:
                gcost_mtx[cur_y+1, cur_x] = gcost_mtx[cur_y, cur_x] + 1
                dist_mtx[cur_y+1, cur_x] = gcost_mtx[cur_y+1, cur_x] + \
                    calcDistEnd(cur_x, cur_y+1, end_x, end_y)
                inp_mtx[cur_y+1, cur_x].set_score(str(int(dist_mtx[cur_y+1, cur_x])))

    # y - 1
    if cur_y > 0 and not inp_mtx[cur_y - 1, cur_x].is_barrier():
        if visit_mtx[cur_y-1, cur_x] == False:
            inp_mtx[cur_y-1, cur_x].make_checked()
            if gcost_mtx[cur_y-1, cur_x] >= gcost_mtx[cur_y, cur_x] + 1:
                gcost_mtx[cur_y-1, cur_x] = gcost_mtx[cur_y, cur_x] + 1
                dist_mtx[cur_y-1, cur_x] = gcost_mtx[cur_y-1, cur_x] + \
                    calcDistEnd(cur_x, cur_y-1, end_x, end_y)
                inp_mtx[cur_y-1, cur_x].set_score(str(int(dist_mtx[cur_y-1, cur_x])))


def findMinDistPoint(dist_mtx, visit_mtx, mtx_width, mtx_height):
    min_point = 10000
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
    min_point = 10000
    next_x = cur_x
    next_y = cur_y
    # x + 1
    if cur_x < mtx_width - 1 and not inp_mtx[cur_y, cur_x+1].is_barrier() and [cur_x+1, cur_y] not in coord_traversed:
        if dist_mtx[cur_y, cur_x+1] < min_point:
            min_point = dist_mtx[cur_y, cur_x+1]
            next_x = cur_x+1
            next_y = cur_y

    # x - 1
    if cur_x > 0 and not inp_mtx[cur_y, cur_x-1].is_barrier() and [cur_x-1, cur_y] not in coord_traversed:
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
    if cur_y < mtx_height - 1 and not inp_mtx[cur_y + 1, cur_x].is_barrier() and [cur_x, cur_y+1] not in coord_traversed:
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
    if cur_y > 0 and not inp_mtx[cur_y - 1, cur_x].is_barrier() and [cur_x, cur_y-1] not in coord_traversed:
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

def findStartEnd(inp_mtx, start, width):
    for i in range(width):
        for k in range(width):
            if start:
                if inp_mtx[i][k].is_start():
                    return k, i
            else:
                if inp_mtx[i][k].is_end():
                    return k, i

def solveAStar(draw, grid, start, end, width):
    inp_list = grid

    inp_mtx = np.array(inp_list)
    mtx_height = len(inp_mtx[:, 0])
    mtx_width = len(inp_mtx[0, :])

    start_x, start_y = findStartEnd(inp_mtx, True, width)
    end_x, end_y = findStartEnd(inp_mtx, False, width)
    

    # store numpy distances list
    dist_mtx = np.zeros((mtx_height, mtx_width))
    gcost_mtx = np.zeros((mtx_height, mtx_width))

    # initialize with an infinite distance
    dist_mtx += 10000
    gcost_mtx += 10000

    # store numpy visited list
    visit_mtx = np.zeros((mtx_height, mtx_width))
    visit_mtx[visit_mtx == 0] = False

    # initialize starting position
    gcost_mtx[start_y, start_x] = 0
    dist_mtx[start_y, start_x] = calcDistEnd(start_x, start_y, end_x, end_y)
    visit_mtx[start_y, start_x] = True
    inp_mtx[start_y, start_x].set_score(str(int(dist_mtx[start_y, start_x])))

    cur_x = start_x
    cur_y = start_y

    # begin the forward search process of the A-star algorithm
    counter = 0
    solvable = True
    while (cur_x != end_x or cur_y != end_y) and solvable:
        # add an option to quit in the middle of the algorithm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        counter += 1
        visit_mtx[cur_y, cur_x] = True
        if not inp_mtx[cur_y, cur_x].is_start() or not inp_mtx[cur_y, cur_x].is_end():
            inp_mtx[cur_y, cur_x].make_visited()
            
        updateDistMtx(cur_x, cur_y, inp_mtx, dist_mtx, visit_mtx,
                      gcost_mtx, mtx_width, mtx_height, end_x, end_y)
        cur_x, cur_y = findMinDistPoint(
            dist_mtx, visit_mtx, mtx_width, mtx_height)
        
        # indicates that no path exists
        if counter > mtx_height * mtx_width:
            solvable = False
        draw()
        
    # trace backwards and identify the shortest path
    coord_traversed = []
    coord_traversed.append([cur_x, cur_y])
    cur_x, cur_y = backtrackPoint(
        cur_x, cur_y, coord_traversed, inp_mtx, dist_mtx, gcost_mtx, mtx_width, mtx_height)
    draw()
    while (cur_x != start_x or cur_y != start_y) and solvable:
        # add an option to quit in the middle of the algorithm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        coord_traversed.append([cur_x, cur_y])
        # set the path blocks to the corresponding path color
        inp_mtx[cur_y, cur_x].make_path()
        cur_x, cur_y = backtrackPoint(
            cur_x, cur_y, coord_traversed, inp_mtx, dist_mtx, gcost_mtx, mtx_width, mtx_height)
        draw()

    return

# -------------------------- End of the functions for the A-Star Algorithm --------------------------

def main(win, width):
    pygame.init()
    num_rows = 30
    grid = make_grid(num_rows, width)
    
    # player decides start and end location
    start = None
    end = None
    
    run = True
    started = False
    finished = False
    
    while run:
        draw(win, grid, num_rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            # prevent user from triggering events when algorithm is underway
            if started and not finished:
                continue
            
            # [0] indicates left mouse button
            if not started: 
                if pygame.mouse.get_pressed()[0]:
                    # obtains mouse position
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, num_rows, width)
                    
                    # access the block object
                    block = grid[row][col]
                    
                    # if the "starting" block has not been initialized, set it first
                    if not start and block != end:
                        start = block
                        start.make_start()
                        
                    # if the "end" block has not been initialized, set it second
                    elif not end and block != start:
                        end = block
                        end.make_end()
                        
                    # next, just initialize all the barriers
                    elif block != start and block != end:
                        block.make_barrier()
                    
                # [2] indicates right mouse button to reset spots
                elif pygame.mouse.get_pressed()[2]:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, num_rows, width)
                    block = grid[row][col]
                    block.reset()
                    if block == start:
                        start = None
                    if block == end:
                        end = None

            if event.type == pygame.KEYDOWN:
                # Click space to trigger the algorithm
                if event.key == pygame.K_SPACE and not started and start and end:
                    started = True
                    solveAStar(lambda:draw(win, grid, num_rows, width), grid, start, end, num_rows)
                    finished = True
                
                # Click escape to restart the grid
                if event.key == pygame.K_ESCAPE and started:
                    # reset and empty grid
                    for i in range(num_rows):
                        for k in range(num_rows):
                            block = grid[i][k]
                            block.reset()
                            block.set_score('')
                    draw(win, grid, num_rows, width)
                    started = False
                    finished = False
                    start = None
                    end = None
    pygame.quit()
    
if __name__ == "__main__":
    main(WIN, WIDTH)
