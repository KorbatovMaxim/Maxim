import pygame
from pygame.locals import *
import random
from typing import Tuple, List, Set, Optional, TypeVar, Iterable



class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        
        self.screen_size = width, height
        
        self.screen = pygame.display.set_mode(self.screen_size)

        
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

    
        self.speed = speed
        self.grid = self.create_grid(True)
        #print("len="+str(self.cell_width))
           
  
    def create_grid(self, randomize: bool=False) -> Optional[List[List[str]]]:
        grid = [["3" for i in range(int(self.width/self.cell_size))]for j in range(int(self.height/self.cell_size))]
        col = 0
        row = 0
        for y in range(0, self.height, self.cell_size):
            for x in range(0, self.width, self.cell_size):
                val = random.randint(0, 1)
                grid[row][col] = val
                col+= 1
            row+= 1
            col=0
        return grid
    
    def get_neighbours(self, cell):
        box_grid = []
        row, col = cell
        #row = args[0]
        #col = args[1]
        inum = 3
        jnum = 3
        isam,jsam = 1,1
        #On the transmitted position we find the starting cell of the square 3x3
        start_row = int(row) - self.cell_size
        start_col = int(col) - self.cell_size

        if (start_col<0):
            start_col = col
            jnum = 2
            isam,jsam = 1,0
        if (start_row<0):
            start_row = row
            inum = 2
            isam,jsam = 0,1
        if (start_row == row) and (start_col == col):
            isam,jsam = 0,0       
        
        if ((start_row + 2*self.cell_size)==self.height):
            if(start_col == col):
                isam,jsam = 1,0
            inum = 2
        
        if ((start_col + 2*self.cell_size)==self.width):
            if(start_row == row):
                isam,jsam = 0,1
            jnum = 2

        #Collect all the values in a 3x3 or 2x2 square
        for i in range(inum):
            for j in range(jnum):
                if (i!=isam) or (j!=jsam): 
                    box_grid.append([int(start_row+i*self.cell_size), int(start_col+j*self.cell_size)])
        return box_grid

    def get_next_generation(self, event):
        grid = self.grid
        elem_box=[]
        grid_new = [[0 for x in range(self.cell_width)] for y in range(self.cell_height)] 
        
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                live_px = 0
                row_new = row*self.cell_size
                col_new = col*self.cell_size
                cell_new = int(row_new),int(col_new)
                box_grid = self.get_neighbours(cell_new)

                for row_box in box_grid:
                    elem_box.clear()
                    for x in row_box:
                        elem_box.append(x)
                    if grid[int(elem_box[0]/self.cell_size)][int(elem_box[1]/self.cell_size)] == 1: 
                            live_px+=1
                grid_new[row][col] = grid[row][col]
                if (grid[row][col]==1) and ((live_px >3) or (live_px<2)):
                    grid_new[row][col] = 0               
                if (grid[row][col]==0) and (live_px >=3):
                    grid_new[row][col] = 1
        self.grid = grid_new        
        return self.grid

    def draw_grid(self) -> None:
        #grid = self.create_grid(True)   
        grid = self.grid
        col = 0
        row = 0       
        for y in range(0, self.height, self.cell_size):
            for x in range(0, self.width, self.cell_size):
                val = int(grid[row][col])
                if (val==1):
                    pygame.draw.rect(self.screen, pygame.Color('green'), (x, y, self.width, self.height)) 
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (x, y, self.width, self.height)) 
                col+= 1
            row+= 1
            col=0
        self.grid = self.get_next_generation(self)
        return None
     
    def draw_lines(self) -> None:
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            self.draw_grid()
            pygame.display.flip()
            #box33 = self.get_neighbours((20,20))
            #print(box33)
            clock.tick(self.speed)
        pygame.quit()
    
    
if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
    grid = game.create_grid(True)
    print(grid)