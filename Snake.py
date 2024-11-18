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
        self.position = self.generate_random_pos()

    def draw(self):
        food_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, (255, 0, 0), food_rect)
        #screen.blit(food_surface,food_rect)
    
    def generate_random_pos(self):
        x = random.randint(0, number_of_cells-1)
        y = random.randint(0, number_of_cells-1)
        position = Vector2(x, y)
        return position

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9),Vector2(5, 9),Vector2(4, 9)]
        self.direction = Vector2(1, 0)

    def draw(self):
        for segment in self.body:
            segment_rect = (segment.x * cell_size, segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7)

    def update(self):
        self.body = self.body[:-1]
        self.body.insert(0,self.body[0] + self.direction)

screen = pygame.display.set_mode((cell_size*number_of_cells,cell_size*number_of_cells))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()


food = Food()
snake = Snake()
#food_surface = pygame.image.load("Graphics/food.png")

# it create custom event
SNAKE_UPDATE = pygame.USEREVENT
# custom snake speed
pygame.time.set_timer(SNAKE_UPDATE, 200)


while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            snake.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != Vector2(0, 1):
                snake.direction = Vector2(0, -1)
            
            if event.key == pygame.K_DOWN and snake.direction != Vector2(0, -1):
                snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and snake.direction != Vector2(1, 0):
                snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and snake.direction != Vector2(-1, 0):
                snake.direction = Vector2(1, 0)
        
    screen.fill(GREEN)
    food.draw()
    snake.draw()

    pygame.display.update()
    clock.tick(60)

