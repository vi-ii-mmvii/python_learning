import pygame

pygame.init()

WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

RED, WHITE = (255, 0, 0), (255, 255, 255)

x, y, step, radius = WIDTH // 2, HEIGHT // 2, 20, 25

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    x = max(radius, min(WIDTH - radius, x + (keys[pygame.K_d] - keys[pygame.K_a]) * step))
    y = max(radius, min(HEIGHT - radius, y + (keys[pygame.K_s] - keys[pygame.K_w]) * step))

    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (x, y), radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
