import pygame
import random
import os

# Inicializando o Pygame
pygame.init()

# Constantes
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
FPS = 60
GRAVITY = 1
JUMP_STRENGTH = 20
SPEED_INCREMENT = 0.01  # Incremento suave da velocidade
MAX_SPEED = 10  # Velocidade máxima
MIN_OBSTACLE_DISTANCE = 200  # Distância mínima entre obstáculos
OBSTACLE_SPAWN_DISTANCE = 30  # Distância que o obstáculo deve percorrer antes de um novo ser gerado

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuração da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Runner")

# Carregar imagens
player_image = pygame.Surface((50, 50))
player_image.fill(BLACK)
ground_image = pygame.Surface((SCREEN_WIDTH, 20))
ground_image.fill(BLACK)
obstacle_image = pygame.Surface((20, 50))
obstacle_image.fill(BLACK)
obstacle_air_image = pygame.Surface((20, 20))
obstacle_air_image.fill((255, 0, 0))  # Cor vermelha para obstáculos aéreos
coin_image = pygame.Surface((20, 20))
coin_image.fill((255, 223, 0))  # Cor dourada para moedas

# Carregar fontes
font = pygame.font.SysFont(None, 48)

# Função para exibir texto centralizado
def draw_text_centered(text, font, color, surface, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(SCREEN_WIDTH / 2, y))
    surface.blit(textobj, textrect)

# Classe do jogador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(midbottom=(100, SCREEN_HEIGHT - 20))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.vel = pygame.math.Vector2(0, 0)
        self.jumping = False

    def update(self, *args):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.jumping:
            self.jumping = True
            self.vel.y = -JUMP_STRENGTH

        if self.jumping:
            self.vel.y += GRAVITY
            self.pos.y += self.vel.y
            if self.pos.y >= SCREEN_HEIGHT - 70:
                self.pos.y = SCREEN_HEIGHT - 70
                self.jumping = False

        self.rect.topleft = self.pos

    def reset(self):
        self.pos = pygame.math.Vector2(100, SCREEN_HEIGHT - 70)
        self.vel = pygame.math.Vector2(0, 0)
        self.jumping = False

# Classe dos obstáculos terrestres
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = obstacle_image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()

# Classe dos obstáculos aéreos
class AirObstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = obstacle_air_image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()

# Classe das moedas
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_image
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()

# Função para mostrar a tela de início
def show_start_screen():
    screen.fill(WHITE)
    draw_text_centered("Endless Runner", font, BLACK, screen, SCREEN_HEIGHT // 4)
    draw_text_centered("Pressione qualquer tecla para começar", font, BLACK, screen, SCREEN_HEIGHT // 2)
    draw_text_centered(f"Highscore: {highscore}", font, BLACK, screen, 3 * SCREEN_HEIGHT // 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Função para mostrar a tela de game over
def show_game_over_screen(score):
    screen.fill(WHITE)
    draw_text_centered("Game Over", font, BLACK, screen, SCREEN_HEIGHT // 4)
    draw_text_centered(f"Score: {score}", font, BLACK, screen, SCREEN_HEIGHT // 2)
    draw_text_centered(f"Highscore: {highscore}", font, BLACK, screen, 3 * SCREEN_HEIGHT // 4)
    draw_text_centered("Pressione qualquer tecla para reiniciar", font, BLACK, screen, 5 * SCREEN_HEIGHT // 8)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Carregar highscore
if os.path.exists("highscore.txt"):
    with open("highscore.txt", "r") as file:
        highscore = int(file.read())
else:
    highscore = 0

# Configurações do jogo
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
obstacles = pygame.sprite.Group()
air_obstacles = pygame.sprite.Group()
coins = pygame.sprite.Group()

clock = pygame.time.Clock()
score = 0
speed = 5
distance = 0
last_obstacle_x = SCREEN_WIDTH

# Loop do jogo
running = True
game_active = False
while running:
    if not game_active:
        show_start_screen()
        game_active = True
        score = 0
        distance = 0
        speed = 5
        player.reset()
        obstacles.empty()
        air_obstacles.empty()
        coins.empty()
        all_sprites.empty()
        all_sprites.add(player)
        last_obstacle_x = SCREEN_WIDTH

        # Gera o primeiro obstáculo imediatamente
        if random.choice([True, False]):
            obstacle = Obstacle(SCREEN_WIDTH, SCREEN_HEIGHT - 70)
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
        else:
            air_obstacle = AirObstacle(SCREEN_WIDTH, SCREEN_HEIGHT - random.randint(120, 180))
            all_sprites.add(air_obstacle)
            air_obstacles.add(air_obstacle)
        last_obstacle_x = SCREEN_WIDTH

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizar posição do último obstáculo
    if obstacles or air_obstacles:
        last_obstacle_x = min(
            [obstacle.rect.x for obstacle in obstacles] +
            [air_obstacle.rect.x for air_obstacle in air_obstacles]
        )

    # Adicionar obstáculos com distância mínima
    if (SCREEN_WIDTH - last_obstacle_x) > MIN_OBSTACLE_DISTANCE:
        if random.randint(1, 60) == 1:
            if random.choice([True, False]):
                obstacle = Obstacle(SCREEN_WIDTH, SCREEN_HEIGHT - 70)
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
            else:
                air_obstacle = AirObstacle(SCREEN_WIDTH, SCREEN_HEIGHT - random.randint(120, 180))
                all_sprites.add(air_obstacle)
                air_obstacles.add(air_obstacle)
            last_obstacle_x = SCREEN_WIDTH  # Atualiza a posição do último obstáculo gerado

    # Adicionar moedas
    if random.randint(1, 100) == 1:
        coin = Coin(SCREEN_WIDTH, random.randint(50, SCREEN_HEIGHT - 90))
        all_sprites.add(coin)
        coins.add(coin)

    # Atualizar
    all_sprites.update(speed)

    # Colisões
    if pygame.sprite.spritecollideany(player, obstacles) or pygame.sprite.spritecollideany(player, air_obstacles):
        game_active = False
        if score > highscore:
            highscore = score
            with open("highscore.txt", "w") as file:
                file.write(str(highscore))
        show_game_over_screen(score)

    # Coleta de moedas
    collected_coins = pygame.sprite.spritecollide(player, coins, True)
    score += len(collected_coins)

    # Atualizar distância e velocidade
    distance += speed / 60
    speed = min(speed + SPEED_INCREMENT, MAX_SPEED)

    # Desenhar
    screen.fill(WHITE)
    screen.blit(ground_image, (0, SCREEN_HEIGHT - 20))
    all_sprites.draw(screen)
    draw_text_centered(f"Score: {score}", font, BLACK, screen, 30)
    draw_text_centered(f"Distance: {int(distance)}", font, BLACK, screen, 70)
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
