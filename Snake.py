import pygame
import sys
import time
import random
from pygame.math import Vector2

pygame.init()
GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)
cell_size = 30
number_of_cells = 25

class Food:
    def __init__(self):
        self.position = vector2(5,6)

    def draw(self):
        pass

screen = pygame.display.set_mode((cell_size*number_of_cells,cell_size*number_of_cells))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill(GREEN)
    
    pygame.display.update()
    clock.tick(60)

