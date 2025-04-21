import pygame
import random
import psycopg2

from config import db_config
from levels import LEVEL_WALLS

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


def parse_walls(layout):
    walls = []
    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            if cell == "*":
                walls.append([x, y])
    return walls

# Function to get walls for the current level


def get_walls(level):
    layout = LEVEL_WALLS.get(level, [])
    return parse_walls(layout)

# Function to determine the level based on the score


def get_level_from_score(score):
    # Each level spans 5 points (e.g., 0-5 for level 1, 6-10 for level 2, etc.)
    return (score // 5) + 1

# Database connection


def connect():
    try:
        return psycopg2.connect(**db_config)
    except Exception as e:
        exit()


def initialize_database():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_score (
            username VARCHAR(50) PRIMARY KEY,
            level INT NOT NULL,
            score INT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


initialize_database()


def get_username():
    input_box = pygame.Rect(WINDOW_SIZE // 2 - 100,
                            WINDOW_SIZE // 2 - 20, 200, 40)
    font = pygame.font.Font(None, 28)
    username = ""
    active = True

    while active:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

        # Draw input box and text
        pygame.draw.rect(screen, BLACK, input_box, 2)
        text_surface = font.render(username, True, BLACK)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(200, text_surface.get_width() + 10)

        # Display instructions
        instructions = font.render("Username:", True, BLACK)
        screen.blit(instructions, (WINDOW_SIZE //
                    2 - 100, WINDOW_SIZE // 2 - 60))

        pygame.display.flip()
        clock.tick(30)

    return username


def display_message(text, y_offset=0, font_size=28):
    font = pygame.font.Font(None, font_size)
    message = font.render(text, True, BLACK)
    screen.blit(message, (WINDOW_SIZE // 2 - message.get_width() //
                2, WINDOW_SIZE // 2 + y_offset))


# User login
def user_login():
    conn = connect()
    cursor = conn.cursor()
    username = get_username()
    cursor.execute(
        "SELECT level, score FROM user_score WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user:
        screen.fill(WHITE)
        display_message(f"Welcome back, {username}!", -40)
        display_message(f"Level: {user[0]}, Score: {user[1]}", 0)
        pygame.display.flip()
        pygame.time.wait(2000)
        return username, user[0], user[1]
    else:
        cursor.execute(
            "INSERT INTO user_score (username, level, score) VALUES (%s, %s, %s)", (username, 1, 0))
        conn.commit()
        screen.fill(WHITE)
        display_message(f"New user created: {username}", -20)
        pygame.display.flip()
        pygame.time.wait(2000)
        return username, 1, 0


# Save game state
def save_game(username, level, score):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_score SET level = %s, score = %s WHERE username = %s", (level, score, username))
    conn.commit()
    conn.close()
    display_message("Game state saved!", 0)
    pygame.display.flip()
    pygame.time.wait(2000)

# Reset player data in the database


def reset_player(username):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE user_score SET level = %s, score = %s WHERE username = %s", (1, 0, username))
    conn.commit()
    conn.close()


def draw_walls(walls):
    for wall in walls:
        pygame.draw.rect(
            screen, RED, (wall[0] * BLOCK_SIZE, wall[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


# Classes
class Snake:
    def __init__(self):
        self.body = [[10, 10]]
        self.dx, self.dy = 1, 0
        self.score = 0
        self.level = 1

    def move(self):
        global walls  # Declare global walls at the start of the method
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
            food.respawn(self.body, walls)

            # Update level based on score
            new_level = get_level_from_score(self.score)
            if new_level > self.level:
                self.level = new_level
                walls = get_walls(self.level)  # Update walls for the new level
                global FPS
                FPS += 2
        else:
            self.body.pop()

        # Check if the snake collides with walls (after movement is complete)
        if head in walls:
            return False

        return True

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(
                screen, GREEN, (segment[0] * BLOCK_SIZE, segment[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


class Food:
    def __init__(self):
        self.respawn()
        self.timer = 0

    def respawn(self, snake_body=[], walls=[]):
        while True:
            self.pos = [random.randint(0, GRID_SIZE - 1),
                        random.randint(0, GRID_SIZE - 1)]
            # Ensure food does not spawn on the snake or walls
            if self.pos not in snake_body and self.pos not in walls:
                break
        self.weight = random.randint(1, 3)
        self.timer = 50

    def update_timer(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.respawn(snake.body, walls)

    def draw(self):
        pygame.draw.rect(
            screen, BLUE, (self.pos[0] * BLOCK_SIZE, self.pos[1] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


# Initialization
username, snake_level, snake_score = user_login()
snake = Snake()
# Initialize level based on score
snake.level = get_level_from_score(snake_score)
snake.score = snake_score
walls = get_walls(snake.level)  # Initialize walls for the starting level
food = Food()
running = True
paused = False

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
            if event.key == pygame.K_p:  # Pause and save
                paused = not paused
                if paused:
                    save_game(username, snake.level, snake.score)
                    screen.fill(WHITE)
                    display_message("Game paused. Press 'P' to resume.", 0)
                    pygame.display.flip()
                    pygame.time.wait(2000)

    if paused:
        continue

    running = snake.move()
    if not running:  # If the player loses
        reset_player(username)  # Reset player data in the database
        screen.fill(WHITE)
        # Display "Game Over" message
        display_message("Game Over!", 0, font_size=36)
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before exiting
        break

    food.update_timer()

    # Draw grid
    for x in range(0, WINDOW_SIZE, BLOCK_SIZE):
        for y in range(0, WINDOW_SIZE, BLOCK_SIZE):
            pygame.draw.rect(screen, BLACK, (x, y, BLOCK_SIZE, BLOCK_SIZE), 1)

    draw_walls(walls)  # Draw cached walls
    snake.draw()
    food.draw()

    # Information panel
    pygame.draw.rect(screen, WHITE, (WINDOW_SIZE, 0,
                     INFO_PANEL_WIDTH, WINDOW_SIZE))
    font = pygame.font.Font(None, 28)
    score_text = font.render(f'Score: {snake.score}', True, RED)
    level_text = font.render(f'Level: {snake.level}', True, RED)
    screen.blit(score_text, (WINDOW_SIZE + 20, 20))
    screen.blit(level_text, (WINDOW_SIZE + 20, 50))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
