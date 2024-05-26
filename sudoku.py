import pygame
import random

# Config
pygame.init()
WIDTH, HEIGHT = 600, 700
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
FONT = pygame.font.SysFont("comicsans", 40)
SMALL_FONT = pygame.font.SysFont("comicsans", 20)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0 , 255)
GRAY = (200, 200, 200)
HIGHLIGHT = (144, 238, 144)  

# Dimensions
CELL_SIZE = 60
GRID_POS = (20, 20)
GRID_SIZE = CELL_SIZE * 9

def draw_grid():
    for x in range(10):
        if x % 3 == 0:
            pygame.draw.line(SCREEN, BLACK, (GRID_POS[0] + x * CELL_SIZE, GRID_POS[1]),
                             (GRID_POS[0] + x * CELL_SIZE, GRID_POS[1] + GRID_SIZE), 4)
            pygame.draw.line(SCREEN, BLACK, (GRID_POS[0], GRID_POS[1] + x * CELL_SIZE),
                             (GRID_POS[0] + GRID_SIZE, GRID_POS[1] + x * CELL_SIZE), 4)
        else:
            pygame.draw.line(SCREEN, GRAY, (GRID_POS[0] + x * CELL_SIZE, GRID_POS[1]),
                             (GRID_POS[0] + x * CELL_SIZE, GRID_POS[1] + GRID_SIZE), 2)
            pygame.draw.line(SCREEN, GRAY, (GRID_POS[0], GRID_POS[1] + x * CELL_SIZE),
                             (GRID_POS[0] + GRID_SIZE, GRID_POS[1] + x * CELL_SIZE), 2)

def draw_numbers(board, initial_board):
    for row in range(9):
        for col in range(9):
            if board[row][col] != 0:
                if initial_board[row][col] != 0:
                    color = BLACK
                else:
                    temp = board[row][col]
                    board[row][col] = 0
                    if is_valid(board, row, col, temp):
                        color = BLUE
                    else:
                        color = RED
                    board[row][col] = temp
                text = FONT.render(str(board[row][col]), True, color)
                SCREEN.blit(text, (GRID_POS[0] + col * CELL_SIZE + 20, GRID_POS[1] + row * CELL_SIZE + 10))

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_row, box_col = row // 3 * 3, col // 3 * 3
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False
    return True

def solve_board(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def generate_full_board():
    board = [[0] * 9 for _ in range(9)]
    
    for _ in range(7):  
        row, col = random.randint(0, 8), random.randint(0, 8)
        num = random.randint(1, 9)
        if is_valid(board, row, col, num):  
            board[row][col] = num
    
    temp_board = [row[:] for row in board]
    if solve_board(temp_board):
        return temp_board
    else:
        return generate_full_board()

def remove_numbers(board, difficulty):
    removal_count = 0
    if difficulty == "easy":
        removal_count = 30
    elif difficulty == "medium":
        removal_count = 40
    elif difficulty == "hard":
        removal_count = 50
    
    removed_positions = set()
    while removal_count > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if (row, col) not in removed_positions:
            removed_positions.add((row, col))
            board[row][col] = 0
            removal_count -= 1

def generate_board(difficulty="easy"):
    board = generate_full_board()
    remove_numbers(board, difficulty)
    return board

def reset_board(difficulty):
    global initial_board, board
    initial_board = generate_board(difficulty)
    board = [row[:] for row in initial_board]

def draw_buttons():
    solve_text = SMALL_FONT.render("Solve", True, BLACK)
    solve_rect = pygame.Rect(500, 620, 100, 50)
    pygame.draw.rect(SCREEN, GREEN, solve_rect)
    SCREEN.blit(solve_text, (solve_rect.x + 20, solve_rect.y + 15))

    reset_text = SMALL_FONT.render("Reset", True, BLACK)
    reset_rect = pygame.Rect(380, 620, 100, 50)
    pygame.draw.rect(SCREEN, RED, reset_rect)
    SCREEN.blit(reset_text, (reset_rect.x + 20, reset_rect.y + 15))

    easy_text = SMALL_FONT.render("Easy", True, BLACK)
    easy_rect = pygame.Rect(20, 620, 100, 50)
    pygame.draw.rect(SCREEN, GRAY, easy_rect)
    SCREEN.blit(easy_text, (easy_rect.x + 20, easy_rect.y + 15))

    medium_text = SMALL_FONT.render("Medium", True, BLACK)
    medium_rect = pygame.Rect(140, 620, 100, 50)
    pygame.draw.rect(SCREEN, GRAY, medium_rect)
    SCREEN.blit(medium_text, (medium_rect.x + 20, medium_rect.y + 15))

    hard_text = SMALL_FONT.render("Hard", True, BLACK)
    hard_rect = pygame.Rect(260, 620, 100, 50)
    pygame.draw.rect(SCREEN, GRAY, hard_rect)
    SCREEN.blit(hard_text, (hard_rect.x + 20, hard_rect.y + 15))

    return solve_rect, reset_rect, easy_rect, medium_rect, hard_rect

def highlight_cell(cell):
    if cell and initial_board[cell[0]][cell[1]] == 0:  
        row, col = cell
        pygame.draw.rect(SCREEN, HIGHLIGHT, (GRID_POS[0] + col * CELL_SIZE, GRID_POS[1] + row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def main():
    global initial_board, board
    initial_board = generate_board("easy")
    board = [row[:] for row in initial_board]

    selected_cell = None
    running = True
    while running:
        SCREEN.fill(WHITE)
        draw_grid()
        highlight_cell(selected_cell)
        draw_numbers(board, initial_board)
        solve_button, reset_button, easy_button, medium_button, hard_button = draw_buttons()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if solve_button.collidepoint(mouse_pos):
                    solve_board(board)
                elif reset_button.collidepoint(mouse_pos):
                    board = [row[:] for row in initial_board]
                elif easy_button.collidepoint(mouse_pos):
                    reset_board("easy")
                elif medium_button.collidepoint(mouse_pos):
                    reset_board("medium")
                elif hard_button.collidepoint(mouse_pos):
                    reset_board("hard")
                else:
                    x, y = mouse_pos
                    if GRID_POS[0] <= x < GRID_POS[0] + GRID_SIZE and GRID_POS[1] <= y < GRID_POS[1] + GRID_SIZE:
                        selected_cell = ((y - GRID_POS[1]) // CELL_SIZE, (x - GRID_POS[0]) // CELL_SIZE)

            if event.type == pygame.KEYDOWN and selected_cell:
                row, col = selected_cell
                if initial_board[row][col] == 0:  
                    if event.key == pygame.K_1:
                        num = 1
                    elif event.key == pygame.K_2:
                        num = 2
                    elif event.key == pygame.K_3:
                        num = 3
                    elif event.key == pygame.K_4:
                        num = 4
                    elif event.key == pygame.K_5:
                        num = 5
                    elif event.key == pygame.K_6:
                        num = 6
                    elif event.key == pygame.K_7:
                        num = 7
                    elif event.key == pygame.K_8:
                        num = 8
                    elif event.key == pygame.K_9:
                        num = 9
                    elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        num = 0
                    else:
                        num = None

                    if num is not None:
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                        else:
                            board[row][col] = num  

        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
