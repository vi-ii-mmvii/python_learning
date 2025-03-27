import pygame
import random

pygame.init()

# Constants
WINDOW_SIZE = 500
BLOCK_SIZE = 20
GRID_SIZE = WINDOW_SIZE // BLOCK_SIZE
INFO_PANEL_WIDTH = 150
FPS = 6

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 150, 0)
RED = (150, 0, 0)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)

# Screen and timer
screen = pygame.display.set_mode((WINDOW_SIZE + INFO_PANEL_WIDTH, WINDOW_SIZE))
clock = pygame.time.Clock()

# Classes
class Snake:
  def __init__(self):
    self.body = [[10, 10]]
    self.dx, self.dy = 1, 0
    self.score = 0
    self.level = 1

  def move(self):
    head = [self.body[0][0] + self.dx, self.body[0][1] + self.dy]

    # Check if the snake goes out of bounds
    if head[0] < 0 or head[0] >= GRID_SIZE or head[1] < 0 or head[1] >= GRID_SIZE:
      return False

    # Check if the snake collides with itself
    if head in self.body:
      return False

    self.body.insert(0, head)

    # Check if the snake eats food
    if head == food.pos:
      self.score += food.weight
      food.respawn(self.body)

      # Increase level every 4 points
      if self.score % 4 == 0:
        self.level += 1
        global FPS
        FPS += 2
    else:
      self.body.pop()
    return True

  def draw(self):
    for segment in self.body:
      pygame.draw.rect(
        screen, GREEN, (segment[0] * BLOCK_SIZE, segment[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


class Food:
  def __init__(self):
    self.respawn()
    self.timer = 0

  def respawn(self, snake_body=[]):
    while True:
      self.pos = [random.randint(0, GRID_SIZE - 1),
            random.randint(0, GRID_SIZE - 1)]
      if self.pos not in snake_body:
        break
    self.weight = random.randint(1, 3)  
    self.timer = 50 

  def update_timer(self):
    if self.timer > 0:
      self.timer -= 1
    else:
      self.respawn(snake.body)

  def draw(self):
    pygame.draw.rect(
      screen, BLUE, (self.pos[0] * BLOCK_SIZE, self.pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


# Initialization
snake = Snake()
food = Food()
running = True

# Game loop
while running:
  screen.fill(WHITE)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_RIGHT and snake.dx == 0:
        snake.dx, snake.dy = 1, 0
      if event.key == pygame.K_LEFT and snake.dx == 0:
        snake.dx, snake.dy = -1, 0
      if event.key == pygame.K_UP and snake.dy == 0:
        snake.dx, snake.dy = 0, -1
      if event.key == pygame.K_DOWN and snake.dy == 0:
        snake.dx, snake.dy = 0, 1

  running = snake.move()
  food.update_timer()

  # Draw grid
  for x in range(0, WINDOW_SIZE, BLOCK_SIZE):
    for y in range(0, WINDOW_SIZE, BLOCK_SIZE):
      pygame.draw.rect(screen, BLACK, (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

  snake.draw()
  food.draw()

  # Information panel
  pygame.draw.rect(screen, WHITE, (WINDOW_SIZE, 0,
           INFO_PANEL_WIDTH, WINDOW_SIZE))
  font = pygame.font.Font(None, 30)
  score_text = font.render(f'Score: {snake.score}', True, RED)
  level_text = font.render(f'Level: {snake.level}', True, RED)
  screen.blit(score_text, (WINDOW_SIZE + 20, 20))
  screen.blit(level_text, (WINDOW_SIZE + 20, 50))

  pygame.display.update()
  clock.tick(FPS)

pygame.quit()
