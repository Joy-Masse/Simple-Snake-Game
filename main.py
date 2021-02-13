import pygame
import os
import random

# Pygame initialization
pygame.init()

# Screen
WIDTH = 800
HEIGHT = 800

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
FPS = 30

# Grid file
# 0 - off, 1 - on
grid_file = open("draw_grid.txt", "r")
draw_grid = bool(int(grid_file.read()))
grid_file.close()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 50, 0)

# Font
TEXT_FONT = pygame.font.Font("fonts/ARCADECLASSIC.TTF", 128)

class GridCell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def place(self, x, y):
        if x == 760:
            self.x = 0
            self.y = y + 40
            print("DOE JH")
            print(self.x, self.y)
        else:
            self.x = x + 40
            self.y = y
            print(self.x, self.y)

class Grid:
    def __init__(self):
        pass

# A head of a snake
class SnakeHead:
    def __init__(self, x, y, length, direction, can_move, alive):
        self.x = x
        self.y = y
        self.lenght = length
        self.direction = direction
        self.can_move = True
        self.alive = True

    # Changes snake's direction
    def change_direction(self, new_dir):
        self.direction = new_dir

    # Moves snake in needed direction
    def move(self):
        if self.direction == "left":
            self.x -= 40
        elif self.direction == "right":
            self.x += 40
        elif self.direction == "up":
            self.y -= 40
        elif self.direction == "down":
            self.y += 40

    # R.I.P
    def die(self):
        global draw_grid
        draw_grid = False
        self.direction = "no"
        self.x = -3000
        self.y = -3000
        self.alive = False

# A cell of a snake
class SnakeCell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Places food exactly in the cell without snake in it
    def place(self, cell_x, cell_y):
        self.x = cell_x
        self.y = cell_y

# A function to redraw screen every iteration
def redraw_screen():
    global grid_cells, snake_cells

    SCREEN.fill(BLACK)

    if draw_grid:
        for i in range(20):
            pygame.draw.line(SCREEN, WHITE, (grid_cells[i].x, grid_cells[i].y), (grid_cells[i].x, 800))

        horizontal_line_y = 40
        for i in range(20):
            pygame.draw.line(SCREEN, WHITE, (0, horizontal_line_y), (800, horizontal_line_y))
            horizontal_line_y += 40
    elif not draw_grid and not snake.alive:
        text = TEXT_FONT.render("OUCH!", True, (255, 255, 255))
        SCREEN.blit(text, (235, 368))

    if snake.alive:
        # Snake
        pygame.draw.rect(SCREEN, WHITE, pygame.Rect(snake.x, snake.y, 40, 40))
        pygame.draw.rect(SCREEN, RED, pygame.Rect(snake.x + 15, snake.y + 15, 10, 10))

        # Snake cells
        for i in range(len(snake_cells)):
            pygame.draw.rect(SCREEN, WHITE, pygame.Rect(snake_cells[i].x, snake_cells[i].y, 40, 40))

        # Food
        pygame.draw.rect(SCREEN, RED, pygame.Rect(food.x, food.y, 40, 40))

    # Updates what happened on the screen
    pygame.display.update()

# Main function
def main():
    global grid_cells, snake, food, snake_cells

    # Clock
    clock = pygame.time.Clock()

    # Placing grid cells
    grid_cells = []
    for i in range(400):
        grid_cells.append(GridCell(0, 0))

    for i in range(len(grid_cells)):
        grid_cells[i].place(grid_cells[i - 1].x, grid_cells[i - 1].y)

    # Snake head
    snake = SnakeHead(400, 400, 1, "right", True, True)
    snake_move_timer = 0
    snake_movement_history_x = []
    snake_movement_history_y = []

    # A variable to determine if snake head is now on the cell
    # Used to prevent direction changing before aquiering(?) new coords
    snake_on_new = True

    # Snake cells
    snake_cells = []

    for i in range(snake.lenght):
        snake_cells.append(SnakeCell(snake.x - 40, snake.y))

    # Available grid cells
    av_cell_x = []
    av_cell_y = []

    # Food
    food = Food(560, 400)

    # Main loop
    running = True
    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Key pressing for movement
        pressed_keys = pygame.key.get_pressed()

        # Movement
        if snake.alive and snake_on_new:
            if pressed_keys[pygame.K_a] and not snake.direction == "right":
                snake.change_direction("left")
                snake_on_new = False
            elif pressed_keys[pygame.K_d] and not snake.direction == "left":
                snake.change_direction("right")
                snake_on_new = False
            if pressed_keys[pygame.K_w] and not pressed_keys[pygame.K_RIGHT] and not pressed_keys[pygame.K_LEFT] and not snake.direction == "down":
                snake.change_direction("up")
                snake_on_new = False
            elif pressed_keys[pygame.K_s] and not pressed_keys[pygame.K_RIGHT] and not pressed_keys[pygame.K_LEFT] and not snake.direction == "up":
                snake.change_direction("down")
                snake_on_new = False

        # Movement timer
        if not snake.can_move and snake_move_timer < 10:
            snake_move_timer += 1
        else:
            snake.can_move = True
            snake_move_timer = 0
            snake_movement_history_x.append(snake.x)
            snake_movement_history_y.append(snake.y)

            # Snake cells movement
            for i in range(snake.lenght):
                if i == 0:
                    snake_cells[i].move(snake_movement_history_x[-1], snake_movement_history_y[-1])
                else:
                    snake_cells[i].move(snake_movement_history_x[-i - 1], snake_movement_history_y[-i - 1])              

        # Moves the snake
        if snake.can_move:
            snake.move()
            snake_on_new = True
            snake.can_move = False

        # Eating food
        if snake.x == food.x and snake.y == food.y:
            snake.lenght += 1
            snake_cells.append(SnakeCell(snake_movement_history_x[-1], snake_movement_history_y[-1]))

            # Available grid cells
            av_cell_x = []
            av_cell_y = []

            for i in range(len(grid_cells)):
                if grid_cells[i].x != snake.x and grid_cells[i].y != snake.y:
                    for j in range(len(snake_cells)):
                        if grid_cells[i].x != snake_cells[j].x and grid_cells[i].y != snake_cells[j].y:
                            av_cell_x.append(grid_cells[i].x)
                            av_cell_y.append(grid_cells[i].y)

            # Placing food
            food.place(av_cell_x[random.randint(0, len(av_cell_x) - 1)], av_cell_y[random.randint(0, len(av_cell_y) - 1)])

        if snake.alive:
            # Screen boundaries
            if snake.x < 0 or snake.x > WIDTH or snake.y < 0 or snake.y > HEIGHT:
                snake.die()

            # Collision with cells
            for i in range(len(snake_cells)):
                if snake.x == snake_cells[i].x and snake.y == snake_cells[i].y:
                    snake.die()

        redraw_screen()

main()

