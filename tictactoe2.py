import pygame
import sys

pygame.init()

# Config
WIDTH, HEIGHT = 900, 600  
GRID_SIZE = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe 2.0")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Font
FONT = pygame.font.SysFont("comicsans", 40)
SMALL_FONT = pygame.font.SysFont("comicsans", 30)

def draw_grid():
    WIN.fill(WHITE)
    for x in range(1, 3):
        pygame.draw.line(WIN, BLACK, (x * GRID_SIZE // 3, 0), (x * GRID_SIZE // 3, GRID_SIZE), 3)
        pygame.draw.line(WIN, BLACK, (0, x * GRID_SIZE // 3), (GRID_SIZE, x * GRID_SIZE // 3), 3)
    pygame.display.update()

def draw_piece(row, col, size, symbol, color):
    x = col * GRID_SIZE // 3 + GRID_SIZE // 6
    y = row * GRID_SIZE // 3 + GRID_SIZE // 6
    
    if size == "small":
        text = SMALL_FONT.render(symbol, True, color)
    elif size == "medium":
        text = FONT.render(symbol, True, color)
    elif size == "large":
        large_font = pygame.font.SysFont("comicsans", 80) 
        text = large_font.render(symbol, True, color)
        
    text_rect = text.get_rect(center=(x, y))
    pygame.draw.circle(WIN, WHITE, (x, y), 80)  
    WIN.blit(text, text_rect)
    pygame.display.update()


def draw_sidebar(current_player, selected_size):
    pygame.draw.rect(WIN, GREY, (GRID_SIZE, 0, WIDTH - GRID_SIZE, HEIGHT))
    turn_text = FONT.render(f"Vez de {current_player.symbol}", True, current_player.color)
    WIN.blit(turn_text, (GRID_SIZE + 20, 20))

    sizes = ["small", "medium", "large"]
    y_start = 100
    for size in sizes:
        piece_text = SMALL_FONT.render(f"{size.capitalize()} ({current_player.pieces[size]})", True, BLACK)
        WIN.blit(piece_text, (GRID_SIZE + 20, y_start))
        if selected_size == size:
            pygame.draw.rect(WIN, BLACK, (GRID_SIZE + 10, y_start - 10, 200, 60), 3)
        y_start += 80

    pygame.display.update()

class Player:
    def __init__(self, symbol, color):
        self.symbol = symbol
        self.color = color
        self.pieces = {"small": 3, "medium": 3, "large": 3}

class TicTacToe:
    size_order = {"small": 1, "medium": 2, "large": 3}

    def __init__(self):
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_turn = None
        self.players = []

    def add_player(self, player):
        self.players.append(player)
        if len(self.players) == 1:
            self.current_turn = player

    def switch_turn(self):
        self.current_turn = self.players[1] if self.current_turn == self.players[0] else self.players[0]

    def make_move(self, row, col, size):
        if self.board[row][col] is None or TicTacToe.size_order[self.board[row][col][1]] < TicTacToe.size_order[size]:
            self.board[row][col] = (self.current_turn.symbol, size)
            self.current_turn.pieces[size] -= 1
            draw_piece(row, col, size, self.current_turn.symbol, self.current_turn.color)
            return True
        return False

    def check_winner(self):
        lines = [
            [self.board[r][c] for c in range(3)] for r in range(3)
        ] + [
            [self.board[r][c] for r in range(3)] for c in range(3)
        ] + [
            [self.board[i][i] for i in range(3)],
            [self.board[i][2 - i] for i in range(3)]
        ]
        for line in lines:
            if all(cell is not None and cell[0] == line[0][0] for cell in line):
                return self.current_turn
        return None

    def is_full(self):
        return all(all(cell is not None for cell in row) for row in self.board)

    def has_possible_moves(self):
        for row in range(3):
            for col in range(3):
                for size in ["small", "medium", "large"]:
                    if self.board[row][col] is None or TicTacToe.size_order[self.board[row][col][1]] < TicTacToe.size_order[size]:
                        if self.current_turn.pieces[size] > 0:
                            return True
        return False

def display_end_message(message):
    WIN.fill(WHITE)
    end_text = FONT.render(message, True, BLACK)
    WIN.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height() // 2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

def main_menu():
    run = True
    player_choice = None
    while run:
        WIN.fill(WHITE)
        title = FONT.render("Choose your fighter", True, BLACK)
        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        x_button = pygame.Rect(WIDTH // 4 - 50, HEIGHT // 2 - 50, 100, 100)
        o_button = pygame.Rect(3 * WIDTH // 4 - 50, HEIGHT // 2 - 50, 100, 100)
        pygame.draw.rect(WIN, RED, x_button)
        pygame.draw.rect(WIN, BLUE, o_button)
        x_text = FONT.render("X", True, WHITE)
        o_text = FONT.render("O", True, WHITE)
        WIN.blit(x_text, (x_button.x + x_button.width // 2 - x_text.get_width() // 2, x_button.y + x_button.height // 2 - x_text.get_height() // 2))
        WIN.blit(o_text, (o_button.x + o_button.width // 2 - o_text.get_width() // 2, o_button.y + o_button.height // 2 - o_button.height // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if x_button.collidepoint(event.pos):
                    player_choice = ("X", RED)
                    run = False
                elif o_button.collidepoint(event.pos):
                    player_choice = ("O", BLUE)
                    run = False

        pygame.display.update()

    return player_choice

def game_loop(player1, player2):
    game = TicTacToe()
    game.add_player(player1)
    game.add_player(player2)
    draw_grid()
    selected_size = "small"
    draw_sidebar(game.current_turn, selected_size)
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x < GRID_SIZE:
                    row = y // (GRID_SIZE // 3)
                    col = x // (GRID_SIZE // 3)
                    if game.make_move(row, col, selected_size):
                        winner = game.check_winner()
                        if winner:
                            display_end_message(f"Player {winner.symbol} wins!")
                            run = False
                        elif not game.has_possible_moves():
                            display_end_message("Draw!")
                            run = False
                        else:
                            game.switch_turn()
                            draw_sidebar(game.current_turn, selected_size)
                else:
                    if 100 <= y <= 160:
                        selected_size = "small"
                    elif 180 <= y <= 240:
                        selected_size = "medium"
                    elif 260 <= y <= 320:
                        selected_size = "large"
                    draw_sidebar(game.current_turn, selected_size)

        pygame.display.update()

    main()

def main():
    player1_choice = main_menu()
    player2_choice = ("O", BLUE) if player1_choice[0] == "X" else ("X", RED)
    player1 = Player(*player1_choice)
    player2 = Player(*player2_choice)
    game_loop(player1, player2)

if __name__ == "__main__":
    main()
