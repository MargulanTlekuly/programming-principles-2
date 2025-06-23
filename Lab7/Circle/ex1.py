import pygame

pygame.init()

WIDTH, HEIGHT = 600, 600 
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BALL_SIZE = 50
STEP = 20 

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

x = WIDTH // 2 - BALL_SIZE // 2
y = HEIGHT // 2 - BALL_SIZE // 2

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
      
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if x - STEP >= 0:
                    x -= STEP
            elif event.key == pygame.K_RIGHT:
                if x + STEP <= WIDTH - BALL_SIZE:
                    x += STEP
            elif event.key == pygame.K_UP:
                if y - STEP >= 0:
                    y -= STEP
            elif event.key == pygame.K_DOWN:
                if y + STEP <= HEIGHT - BALL_SIZE:
                    y += STEP

    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (x + BALL_SIZE // 2, y + BALL_SIZE // 2), BALL_SIZE // 2)
    
    pygame.display.flip()

pygame.quit()