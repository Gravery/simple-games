import pygame
import random
import os


pygame.init()

# Load sound effects
appear_sound = pygame.mixer.Sound('assets/appear.mp3')
hit_sound = pygame.mixer.Sound('assets/hit.mp3')
miss_sound = pygame.mixer.Sound('assets/miss.mp3')

# Game dimensions for fullscreen
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Font
FONT = pygame.font.Font(None, 74)


def load_highscore():
    if os.path.exists('highscore.txt'):
        with open('highscore.txt', 'r') as file:
            return int(file.read())
    return 0

def save_highscore(score):
    with open('highscore.txt', 'w') as file:
        file.write(str(score))

def display_message(screen, message, color, size, position):
    font = pygame.font.Font(None, size)
    text = font.render(message, True, color)
    rect = text.get_rect(center=position)
    screen.blit(text, rect)

def main_menu():
    highscore = load_highscore()
    
    while True:
        SCREEN.fill(BLACK)
        display_message(SCREEN, "Osu Capenga", WHITE, 100, (WIDTH // 2, HEIGHT // 4))
        display_message(SCREEN, f'Highscore: {highscore}', WHITE, 74, (WIDTH // 2, HEIGHT // 2))
        display_message(SCREEN, "Pressione Enter para jogar", WHITE, 50, (WIDTH // 2, HEIGHT // 1.5))
        display_message(SCREEN, "Pressione Esc para sair", WHITE, 50, (WIDTH // 2, HEIGHT // 1.3))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False

def game_over_screen(score):
    highscore = load_highscore()
    
    while True:
        SCREEN.fill(BLACK)
        display_message(SCREEN, "Game Over", WHITE, 100, (WIDTH // 2, HEIGHT // 4))
        display_message(SCREEN, f'Score: {score}', WHITE, 74, (WIDTH // 2, HEIGHT // 2))
        display_message(SCREEN, f'Highscore: {highscore}', WHITE, 74, (WIDTH // 2, HEIGHT // 1.5))
        display_message(SCREEN, "Pressione Enter para jogar novamente", WHITE, 50, (WIDTH // 2, HEIGHT // 1.3))
        display_message(SCREEN, "Pressione Esc para sair", WHITE, 50, (WIDTH // 2, HEIGHT // 1.2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False

def main_game():
    clock = pygame.time.Clock()
    running = True
    score = 0
    missed = 0
    highscore = load_highscore()
    
    circle_radius = 200  # Circle size
    circle_time = 1500  # Time for a circle to disappear
    circle_delay = 2500 # Delay between circles
    next_circle_time = pygame.time.get_ticks() + circle_delay

    circles = []
    
    while running:
        current_time = pygame.time.get_ticks()
        SCREEN.fill(BLACK)
        
        # Spawn new circle if the delay has passed
        if current_time >= next_circle_time:
            x = random.randint(circle_radius, WIDTH - circle_radius)
            y = random.randint(circle_radius, HEIGHT - circle_radius)
            circle_rect = pygame.Rect(x - circle_radius, y - circle_radius, circle_radius * 2, circle_radius * 2)
            circles.append((circle_rect, current_time + circle_time))
            next_circle_time = current_time + circle_delay
            appear_sound.play()  
        
        # Draw and manage circles
        for circle in circles[:]:
            rect, expiry = circle
            if current_time >= expiry:
                circles.remove(circle)
                missed += 1
                miss_sound.play()  
                if missed >= 3:
                    running = False
                    break
            else:
                pygame.draw.ellipse(SCREEN, RED, rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z or event.key == pygame.K_x:
                    mouse_pos = pygame.mouse.get_pos()
                    for circle in circles[:]:
                        rect, _ = circle
                        if rect.collidepoint(mouse_pos):
                            score += 1
                            circles.remove(circle)
                            hit_sound.play()  
                            circle_delay = max(100, circle_delay - 30)
                            circle_time = max(500, circle_time - 5)
                            circle_radius = max(50, circle_radius - 3)
                            break
        
        display_message(SCREEN, f'Score: {score}', WHITE, 74, (WIDTH // 2, 50))
        display_message(SCREEN, f'Missed: {missed}/3', WHITE, 74, (WIDTH // 2, 150))
        
        pygame.display.flip()
        clock.tick(60)
    
    if score > highscore:
        save_highscore(score)
    
    return score, highscore


def main():
    while True:
        if not main_menu():
            break
        score, highscore = main_game()
        if not game_over_screen(score):
            break
        
    pygame.quit()

if __name__ == "__main__":
    main()
