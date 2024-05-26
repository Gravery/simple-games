import pygame
import random
import sys
import os
import pickle

pygame.init()

# Screen config
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 40)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# CONSTANTS
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_HEIGHT = 500
GAP_SIZE = 200
PIPE_MOVE_SPEED = 3
PROJECTILE_SPEED = 5
PIPE_MIN_Y = 150
PIPE_MAX_Y = SCREEN_HEIGHT - 150
PIPE_SPAWN_TIME = 2500  # Timer for pipes to spawn

def load_highscore(filename="highscore.dat"):
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
    return 0

def save_highscore(highscore, filename="highscore.dat"):
    with open(filename, 'wb') as f:
        pickle.dump(highscore, f)

highscore = load_highscore()

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT//2))
        self.velocity = 0
    
    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity
        if self.rect.bottom >= SCREEN_HEIGHT or self.rect.top <= 0:
            self.kill()
    
    def flap(self):
        self.velocity = FLAP_STRENGTH

class PipePair(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((PIPE_WIDTH, SCREEN_HEIGHT))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect(midtop=(x, 0))
        self.pipe_gap_y = random.randint(PIPE_MIN_Y, PIPE_MAX_Y)
        self.moving = False
        self.move_direction = 1
        self.distance_move = 0
        self.distance_counter = 0
    
    def update(self):
        self.rect.x -= PIPE_MOVE_SPEED
        if self.moving:
            if self.distance_counter == 0:
                self.distance_move = random.randint(10, 30)
            self.pipe_gap_y += self.move_direction
            self.distance_counter += 1
            if self.distance_counter >= self.distance_move:
                self.move_direction *= -1
                self.distance_counter = 0
        
        if self.rect.right < 0:
            self.kill()
    
    def draw(self, surface):
        top_rect = pygame.Rect(self.rect.x, self.pipe_gap_y - PIPE_HEIGHT - GAP_SIZE//2, PIPE_WIDTH, PIPE_HEIGHT)
        bottom_rect = pygame.Rect(self.rect.x, self.pipe_gap_y + GAP_SIZE//2, PIPE_WIDTH, PIPE_HEIGHT)
        pygame.draw.rect(surface, GREEN, top_rect)
        pygame.draw.rect(surface, GREEN, bottom_rect)
    
    def check_collision(self, player):
        player_rect = player.rect
        top_rect = pygame.Rect(self.rect.x, self.pipe_gap_y - PIPE_HEIGHT - GAP_SIZE//2, PIPE_WIDTH, PIPE_HEIGHT)
        bottom_rect = pygame.Rect(self.rect.x, self.pipe_gap_y + GAP_SIZE//2, PIPE_WIDTH, PIPE_HEIGHT)
        return player_rect.colliderect(top_rect) or player_rect.colliderect(bottom_rect)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        self.rect.x -= PROJECTILE_SPEED
        if self.rect.right < 0:
            self.kill()

def game():
    global highscore
    
    player = Player()
    all_sprites = pygame.sprite.Group(player)
    pipes = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    
    # Timer for pipes and projectiles
    pipe_timer = pygame.USEREVENT + 1
    projectile_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(pipe_timer, PIPE_SPAWN_TIME)
    pygame.time.set_timer(projectile_timer, 2000)

    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.flap()
            if event.type == pipe_timer:
                pipe_pair = PipePair(SCREEN_WIDTH)
                if score >= 15:
                    pipe_pair.moving = True
                pipes.add(pipe_pair)
                all_sprites.add(pipe_pair)
            if event.type == projectile_timer and score >= 30:
                y = random.randint(50, SCREEN_HEIGHT - 50)
                projectile = Projectile(SCREEN_WIDTH, y)
                projectiles.add(projectile)
                all_sprites.add(projectile)
        
        all_sprites.update()

        # Check collisions
        for pipe in pipes:
            if pipe.check_collision(player):
                running = False
        
        if pygame.sprite.spritecollideany(player, projectiles):
            running = False
        
        screen.fill(BLACK)
        for entity in all_sprites:
            if isinstance(entity, PipePair):
                entity.draw(screen)
            else:
                screen.blit(entity.image, entity.rect)
        draw_text(f'Score: {score}', FONT, WHITE, screen, SCREEN_WIDTH//2, 50)
        pygame.display.flip()
        
        # Score counting
        passed_pipes = [pipe for pipe in pipes if pipe.rect.right < player.rect.left]
        for pipe in passed_pipes:
            pipes.remove(pipe)
            score += 1
        
        clock.tick(30)
    
    if score > highscore:
        highscore = score
        save_highscore(highscore)
        game_over(screen, score, True)
    else:
        game_over(screen, score, False)

def game_over(screen, score, new_highscore):
    screen.fill(BLACK)
    draw_text('Game Over', FONT, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)
    draw_text(f'Score: {score}', FONT, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    if new_highscore:
        draw_text('New Highscore!', FONT, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
    draw_text('Press Space to Play Again', FONT, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def main_menu():
    screen.fill(BLACK)
    draw_text('Flappy Square', FONT, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)
    draw_text('Press Space to Start', FONT, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    draw_text(f'Highscore: {highscore}', FONT, WHITE, screen, SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# Main loop
while True:
    main_menu()
    game()
