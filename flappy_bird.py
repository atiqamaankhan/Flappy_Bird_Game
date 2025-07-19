import pygame
import random
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Smooth Animated")

# Game variables
GRAVITY = 0.35
BIRD_JUMP = -8.5
PIPE_SPEED = 3
PIPE_GAP = 150

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 200, 255)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont('Arial', 32)

# Load bird animation frames
bird_frames = [
    pygame.transform.scale(pygame.image.load("bird_up.png"), (34, 24)),
    pygame.transform.scale(pygame.image.load("bird_mid.png"), (34, 24)),
    pygame.transform.scale(pygame.image.load("bird_down.png"), (34, 24))
]
bird_frame_index = 0
bird_frame_counter = 0

# Bird settings
bird = pygame.Rect(100, HEIGHT // 2, 34, 24)
bird_y = float(bird.y)
bird_velocity = 0.0

# Pipes
pipes = []
def create_pipe():
    height = random.randint(100, 400)
    top = pygame.Rect(WIDTH, 0, 52, height)
    bottom = pygame.Rect(WIDTH, height + PIPE_GAP, 52, HEIGHT - height - PIPE_GAP)
    return top, bottom
pipes.extend(create_pipe())

clock = pygame.time.Clock()
score = 0

def move_pipes(pipes):
    for pipe in pipes:
        pipe.x -= PIPE_SPEED
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(SCREEN, GREEN, pipe)

def check_collision(bird, pipes):
    for pipe in pipes:
        if bird.colliderect(pipe):
            return True
    if bird.top <= 0 or bird.bottom >= HEIGHT:
        return True
    return False

# Main Game Loop
running = True
while running:
    dt = clock.tick(60) / 1000  # seconds passed since last frame
    SCREEN.fill(BLUE)

    # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = BIRD_JUMP

    # Bird physics
    bird_velocity += GRAVITY
    bird_y += bird_velocity
    bird.y = int(bird_y)

    # Animate bird
    bird_frame_counter += 1
    if bird_frame_counter % 5 == 0:
        bird_frame_index = (bird_frame_index + 1) % len(bird_frames)

    # Pipe logic
    pipes = move_pipes(pipes)
    if pipes[0].x < -60:
        pipes = pipes[2:] 
        pipes.extend(create_pipe())
        score += 1

    # Collision
    if check_collision(bird, pipes):
        print("Game Over! Final Score:", score)
        pygame.quit()
        sys.exit()

    # Draw
    SCREEN.blit(bird_frames[bird_frame_index], (bird.x, bird.y))
    draw_pipes(pipes)
    score_text = font.render(f"Score: {score}", True, WHITE)
    SCREEN.blit(score_text, (10, 10))
    pygame.display.update() 