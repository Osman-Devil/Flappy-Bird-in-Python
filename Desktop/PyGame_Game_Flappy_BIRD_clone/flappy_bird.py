import pygame
import random

pygame.init()

# Window settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Loading images
bird_img = pygame.image.load("bird2.png")
bird_img = pygame.transform.scale(bird_img, (34, 24))  # Reduse bird size
bird_rect = bird_img.get_rect(center=(100, HEIGHT // 2))

# Game setting 
gravity = 0.5
bird_movement = 0
pipe_width = 50
pipe_gap = 200
pipe_velocity = -3
pipes = []
SCORE = 0
passed_pipes = []  # List of passed pipes
font = pygame.font.Font(None, 36)

def create_pipe():
    height = random.randint(150, 400)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.x += pipe_velocity
    return [pipe for pipe in pipes if pipe.x > -pipe_width]

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

def check_collision():
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    return False

def show_game_over():
    screen.fill(WHITE)
    text = font.render("Game Over", True, RED)
    retry = font.render("Press R to Restart", True, GREEN)
    screen.blit(text, (WIDTH // 2 - 50, HEIGHT // 3))
    screen.blit(retry, (WIDTH // 2 - 80, HEIGHT // 2))
    pygame.display.update()

def restart_game():
    global bird_rect, bird_movement, pipes, SCORE, passed_pipes
    bird_rect.center = (100, HEIGHT // 2)
    bird_movement = 0
    pipes = []
    SCORE = 0
    passed_pipes = []

def main():
    global bird_movement, pipes, SCORE
    clock = pygame.time.Clock()
    spawn_pipe = pygame.USEREVENT
    pygame.time.set_timer(spawn_pipe, 1200)
    running = True
    game_active = True

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird_movement = -8
                if event.key == pygame.K_r and not game_active:
                    game_active = True
                    restart_game()
            if event.type == spawn_pipe and game_active:
                pipes.extend(create_pipe())

        if game_active:
            bird_movement += gravity
            bird_rect.y += bird_movement
            pipes = move_pipes(pipes)
            screen.blit(bird_img, bird_rect)
            draw_pipes(pipes)
            
            # Score counting 
            for pipe in pipes:
                if pipe.right < bird_rect.left and pipe not in passed_pipes:
                    passed_pipes.append(pipe)
                    SCORE += 1  # Add points only for passed pipes
            
            score_text = font.render(f"Score: {SCORE}", True, RED)
            screen.blit(score_text, (10, 10))
            
            if check_collision():
                game_active = False
        else:
            show_game_over()
        
        pygame.display.update()
        clock.tick(30)

    pygame.quit()

main()
