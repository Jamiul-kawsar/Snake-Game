import pygame
import sys
import time
import random
from pygame.math import Vector2

pygame.init()
title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

GREEN = (0, 255, 0)
BLACK = (0,0,0)
RED = (255,0,0)
GRAY = (128,128,128)
cell_size = 16
number_of_cells = 25

# width of the border
OFFSET = 75

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, RED, food_rect)
        #screen.blit(food_surface,food_rect)
    
    def generate_random_cell(self):
        x = random.randint(0, number_of_cells-1)
        y = random.randint(0, number_of_cells-1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()

        return position

class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9),Vector2(5, 9),Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET+segment.x * cell_size, OFFSET+segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, GREEN, segment_rect, 0, 7)

    def update(self):
        self.body.insert(0,self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]
    
    def reset(self):
        self.body = [Vector2(6, 9),Vector2(5, 9),Vector2(4, 9)]
        self.direction = Vector2(1, 0)
            

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        # game score
        self.score = 0
        self.state = "RUNNING"
    
    def draw(self):
        self.food.draw()
        self.snake.draw()

    def update(self):
        if self.state == "RUNNING":   
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tails()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.score += 1
            self.snake.add_segment = True
    
    def check_collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        print("Score: ",self.score)
        #restart the game score
        self.score = 0
        self.state = "STOPPED"

    def check_collision_with_tails(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()

# screen
screen = pygame.display.set_mode((2 * OFFSET + cell_size*number_of_cells,  2 * OFFSET + cell_size*number_of_cells))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

game = Game()
#food_surface = pygame.image.load("Graphics/food.png")

# it create custom event
SNAKE_UPDATE = pygame.USEREVENT
# custom snake speed
pygame.time.set_timer(SNAKE_UPDATE, 200)


while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game.state == "STOPPED":
                game.state = "RUNNING"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)

            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)

            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)

    # screen fill with black color 
    screen.fill(BLACK)
    # draw bordar
    pygame.draw.rect(screen, GRAY, (OFFSET-10, OFFSET-10,cell_size*number_of_cells+20,cell_size*number_of_cells+20), 10)
    game.draw()
    title_surface = title_font.render("Snake Game", True, GRAY)
    score_surface = score_font.render("Score: " + str(game.score), True, GRAY)
    screen.blit(title_surface, (OFFSET-10, 20))
    screen.blit(score_surface, (OFFSET -5, OFFSET + cell_size*number_of_cells + 10))

    pygame.display.update()
    clock.tick(60)

