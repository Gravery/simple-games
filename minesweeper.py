import pygame
import sys
import random
import time

pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Config
DIFFICULTIES = {
    'easy': {'size': 8, 'bombs': 10, 'cell_size': 50},
    'medium': {'size': 16, 'bombs': 40, 'cell_size': 30},
    'hard': {'size': 32, 'bombs': 160, 'cell_size': 20}
}

class Minesweeper:
    def __init__(self, difficulty):
        self.size = DIFFICULTIES[difficulty]['size']
        self.bombs = DIFFICULTIES[difficulty]['bombs']
        self.cell_size = DIFFICULTIES[difficulty]['cell_size']
        self.grid = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.revealed = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.flagged = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.game_over = False
        self.victory = False
        self.start_time = None
        self.place_bombs()
        self.calculate_numbers()
        self.screen_size = self.size * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size + 100))
        pygame.display.set_caption('Campo Minado')
        self.font = pygame.font.SysFont(None, 36)

    def place_bombs(self):
        count = 0
        while count < self.bombs:
            x = random.randint(0, self.size - 1)
            y = random.randint(0, self.size - 1)
            if self.grid[y][x] != -1:
                self.grid[y][x] = -1
                count += 1

    def calculate_numbers(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.grid[y][x] == -1:
                    continue
                bombs_count = sum(
                    (self.grid[ny][nx] == -1) 
                    for nx in range(max(0, x-1), min(self.size, x+2))
                    for ny in range(max(0, y-1), min(self.size, y+2))
                )
                self.grid[y][x] = bombs_count

    def reveal(self, x, y):
        if self.start_time is None:
            self.start_time = time.time()
        if self.grid[y][x] == -1:
            self.game_over = True
        self.revealed[y][x] = True
        if self.grid[y][x] == 0:
            for nx in range(max(0, x-1), min(self.size, x+2)):
                for ny in range(max(0, y-1), min(self.size, y+2)):
                    if not self.revealed[ny][nx]:
                        self.reveal(nx, ny)
        self.check_victory()

    def flag(self, x, y):
        self.flagged[y][x] = not self.flagged[y][x]
        self.check_victory()

    def check_victory(self):
        if all(
            (self.revealed[y][x] or self.flagged[y][x]) and
            (self.grid[y][x] != -1 or self.flagged[y][x])
            for y in range(self.size)
            for x in range(self.size)
        ):
            self.victory = True

    def draw(self):
        self.screen.fill(WHITE)
        for y in range(self.size):
            for x in range(self.size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if self.revealed[y][x]:
                    if self.grid[y][x] == -1:
                        pygame.draw.rect(self.screen, RED, rect)
                    else:
                        pygame.draw.rect(self.screen, GRAY, rect)
                        if self.grid[y][x] > 0:
                            font = pygame.font.SysFont(None, self.cell_size)
                            img = font.render(str(self.grid[y][x]), True, BLACK)
                            self.screen.blit(img, (x * self.cell_size + self.cell_size // 3, y * self.cell_size))
                else:
                    pygame.draw.rect(self.screen, WHITE, rect)
                    pygame.draw.rect(self.screen, BLACK, rect, 1)
                    if self.flagged[y][x]:
                        pygame.draw.line(self.screen, BLACK, (x * self.cell_size, y * self.cell_size),
                                         (x * self.cell_size + self.cell_size, y * self.cell_size + self.cell_size), 2)
                        pygame.draw.line(self.screen, BLACK, (x * self.cell_size + self.cell_size, y * self.cell_size),
                                         (x * self.cell_size, y * self.cell_size + self.cell_size), 2)
        
        # Draw info
        elapsed_time = int(time.time() - self.start_time) if self.start_time else 0
        time_text = self.font.render(f"Tempo: {elapsed_time} s", True, BLACK)
        self.screen.blit(time_text, (10, self.screen_size + 10))
        
        bombs_left = self.bombs - sum(sum(row) for row in self.flagged)
        bombs_text = self.font.render(f"Bombas restantes: {bombs_left}", True, BLACK)
        self.screen.blit(bombs_text, (10, self.screen_size + 50))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if y < self.screen_size:  # Click inside the grid
                        grid_x, grid_y = x // self.cell_size, y // self.cell_size
                        if event.button == 1:
                            self.reveal(grid_x, grid_y)
                        elif event.button == 3:
                            self.flag(grid_x, grid_y)
            self.draw()
            if self.game_over:
                self.show_end_screen("Game Over")
                running = False
            elif self.victory:
                self.show_end_screen("Victory!")
                running = False

        pygame.quit()
        sys.exit()

    def show_end_screen(self, message):
        self.screen.fill(WHITE)
        text = self.font.render(message, True, RED if message == "Game Over" else GREEN)
        self.screen.blit(text, (self.screen_size // 2 - text.get_width() // 2, self.screen_size // 2 - text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        main_menu()

def main_menu():
    screen = pygame.display.set_mode((400, 400))
    pygame.display.set_caption('Minesweeper - Menu')
    font = pygame.font.SysFont(None, 48)
    menu_items = ["Easy", "Medium", "Hard"]
    difficulties = ['easy', 'medium', 'hard']
    while True:
        screen.fill(WHITE)
        
        for i, item in enumerate(menu_items):
            text = font.render(item, True, BLACK)
            text_rect = text.get_rect(center=(200, 100 + i * 60))
            screen.blit(text, text_rect)
            if text_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, BLUE, text_rect, 2)
                if pygame.mouse.get_pressed()[0]:
                    game = Minesweeper(difficulties[i])
                    game.run()
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main_menu()
