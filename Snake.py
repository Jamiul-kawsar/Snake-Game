import pygame
import sys
import time
import random
import heapq
from pygame.math import Vector2

pygame.init()
title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0,0,0)
RED = (255,0,0)
GRAY = (128,128,128)
cell_size = 16
number_of_cells = 25

# width of the border
OFFSET = 75

# heuristic for a* algorithm
def heuristic(pos, goal):
    # Manhatten distance heuristic calculations
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

# get valid neighbor cells
def get_neighbors(position, grid):
    neighbors = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] #down , right , up, left
    for dx, dy in directions:
        x, y = position[0] + dx, position[1] + dy
        if 0 <= x < number_of_cells and 0 <= y < number_of_cells and grid[y][x] == 0:
            neighbors.append((x,y))
    return neighbors

# A* algorithm find the shortest path
def a_star(start, goal, grid):
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {} #track perant nodes
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_list:
        # element of open_list tuple _ is priority
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        # calculate the heuristic value of neighbor cells
        for neighbor in get_neighbors(current, grid):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None # no path found

class Food:
    def __init__(self, snake_bodies):
        self.position = self.generate_random_pos(snake_bodies)

    def draw(self):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, RED, food_rect)
        #screen.blit(food_surface,food_rect)
    
    def generate_random_cell(self):
        x = random.randint(0, number_of_cells-1)
        y = random.randint(0, number_of_cells-1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_bodies):
        position = self.generate_random_cell()
        while position in snake_bodies:
            position = self.generate_random_cell()

        return position

# Snake class
class Snake:
    def __init__(self, start_pos, color):
        # negative i because of move is opposite direction of body
        self.body = [start_pos + Vector2(-i,0) for i in range(3)]
        self.direction = Vector2(1, 0)
        self.add_segment = False
        self.color = color

    def draw(self):
        for segment in self.body:
            segment_rect = (OFFSET+segment.x * cell_size, OFFSET+segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, self.color, segment_rect, 0, 7)

    def update(self):
        self.body.insert(0,self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:
            self.body = self.body[:-1]
    
    def reset(self, start_pos):
        self.body = [start_pos + Vector2(-i,0) for i in range(3)]
        self.direction = Vector2(1, 0)
    
    #find the shortest path to food using A*
    def find_path_to_food(self, food_pos, other_snake):
        grid = [[0 for _ in range(number_of_cells)] for _ in range(number_of_cells)]
        # Mark this snake's body as obstacles
        for segment in self.body[1:]:
            grid[int(segment.y)][int(segment.x)] = 1
        # Mark the other snake's body as obstacles
        for segment in other_snake.body[1:]:
            grid[int(segment.y)][int(segment.x)] = 1
        
        start = (int(self.body[0].x), int(self.body[0].y))
        goal = (int(food_pos.x), int(food_pos.y))
        path = a_star(start, goal, grid)
        return path        

class Game:
    def __init__(self):
        self.snake_human = Snake(Vector2(10,10), GREEN)
        self.snake_ai = Snake(Vector2(5, 5), BLUE)
        self.food = Food(self.snake_human.body)
        # game score
        self.score_human = 0
        self.score_ai = 0
        self.state = "RUNNING"
        self.path_ai = None
    
    def draw(self):
        self.food.draw()
        self.snake_human.draw()
        self.snake_ai.draw()

    def update(self):
        # AI snake update
        if self.path_ai and len(self.path_ai) > 0:
            next_cell = self.path_ai.pop(0)
            next_pos = Vector2(next_cell[0],next_cell[1])
            self.snake_ai.direction = next_pos - self.snake_ai.body[0]
        self.snake_ai.update()

        # recalculate AI path if needed
        if not self.path_ai or self.snake_ai.body[0] == self.food.position:
            self.path_ai = self.snake_ai.find_path_to_food(self.food.position, self.snake_human)

        # check collision for AI snake
        self.check_collision(self.snake_ai, "AI")

        # update human snake
        self.snake_human.update()

        # check collision for Human snake
        self.check_collision(self.snake_human, "HUMAN")

    def check_collision(self, snake , player_type):
        if snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos([self.snake_human, self.snake_ai])
            if player_type == "HUMAN":
                self.score_human += 1
            else:
                self.score_ai += 1
            snake.add_segment = True

        # Check collision with edges
        if (snake.body[0].x >= number_of_cells or snake.body[0].x < 0 or snake.body[0].y >= number_of_cells or snake.body[0].y < 0):
            snake.reset(Vector2(10, 10) if player_type == "HUMAN" else Vector2(15, 15))

        # Check collision with itself
        if snake.body[0] in snake.body[1:]:
            snake.reset(Vector2(10, 10) if player_type == "HUMAN" else Vector2(15, 15))

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
            if event.key == pygame.K_UP and game.snake_human.direction != Vector2(0, 1):
                game.snake_human.direction = Vector2(0, -1)
            
            if event.key == pygame.K_DOWN and game.snake_human.direction != Vector2(0, -1):
                game.snake_human.direction = Vector2(0, 1)

            if event.key == pygame.K_LEFT and game.snake_human.direction != Vector2(1, 0):
                game.snake_human.direction = Vector2(-1, 0)

            if event.key == pygame.K_RIGHT and game.snake_human.direction != Vector2(-1, 0):
                game.snake_human.direction = Vector2(1, 0)

    # screen fill with black color 
    screen.fill(BLACK)
    # draw bordar
    pygame.draw.rect(screen, GRAY, (OFFSET-10, OFFSET-10,cell_size*number_of_cells+20,cell_size*number_of_cells+20), 10)
    game.draw()
    title_surface = title_font.render("Snake Game", True, GRAY)
    score_surface = score_font.render(f"Human: {game.score_human}  AI: {game.score_ai}", True, GRAY)
    screen.blit(title_surface, (OFFSET-10, 20))
    screen.blit(score_surface, (OFFSET -5, OFFSET + cell_size*number_of_cells + 10))

    pygame.display.update()
    clock.tick(60)

