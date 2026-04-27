import pygame
import random

pygame.init()

WIDTH = 79
HEIGHT = 54
HEADER_HEIGHT = 50
PANEL_WIDTH = 150
NUM_MINES = 998
CELL_SIZE = 40
COLORS = {
    "GRAY": (128, 128, 128),
    "LIGHT_GRAY": (192,192,192),
    "WHITE": (255,255,255)
}

FIXED_WIDTH = 1200
FIXED_HEIGHT = 800
screen = pygame.display.set_mode((FIXED_WIDTH, FIXED_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)

scroll_x = 0
scroll_y = 0

def print_board(mines, numbers):
    for r in range(HEIGHT):
        for c in range(WIDTH):
            if mines[r][c]:
                print(" X ", end="")
            else:
                print(f" {numbers[r][c]} ", end="")
        print()

def check_if_mine(r,c, mines):
    if r<0 or c<0 or r>=len(mines) or c>=len(mines[0]):
        return False
    if mines[r][c]:
        return True
    else:
        return False
            
def set_cell_number(mines, numbers, r, c):
    if not(0 <= r < HEIGHT and 0 <= c < WIDTH):
        return

    if mines[r][c] == True:
        numbers[r][c] = -1
        return
    
    count = 0
    
    for row in range(r-1, r+2):
        for column in range(c-1, c+2):
            if row == r and column == c:
                continue

            if check_if_mine(row,column, mines):
                count += 1
    
    numbers[r][c] = count

def draw_board():
    screen.fill(COLORS["WHITE"])
    visible_width = (screen.get_width() - PANEL_WIDTH) // CELL_SIZE
    visible_height = (screen.get_height() - HEADER_HEIGHT) // CELL_SIZE

    for row_offset in range(visible_height):
        for col_offset in range(visible_width):
            row = scroll_y + row_offset
            col = scroll_x + col_offset

            if row >= HEIGHT or col >= WIDTH: continue

            x = col_offset * CELL_SIZE
            y = row_offset * CELL_SIZE + HEADER_HEIGHT

            if not revealed[row][col]:
                pygame.draw.rect(screen, COLORS["GRAY"], (x,y,CELL_SIZE,CELL_SIZE))
                if flagged[row][col]:
                    pygame.draw.circle(screen, (255, 0, 0), (x + CELL_SIZE//2, y + CELL_SIZE//2), CELL_SIZE//4)
                continue
            
            pygame.draw.rect(screen, COLORS["LIGHT_GRAY"], (x,y,CELL_SIZE,CELL_SIZE))

            if numbers[row][col]>0:
                text = font.render(str(numbers[row][col]), True, (0,0,0))
                text_rect = text.get_rect(center = (x+CELL_SIZE//2, y+CELL_SIZE//2))
                screen.blit(text, text_rect)
            
            if numbers[row][col]==-1:
                #mine (fix later)
                text = font.render("X", True, (0,0,0))
                text_rect = text.get_rect(center = (x+CELL_SIZE//2, y+CELL_SIZE//2))
                screen.blit(text, text_rect)

    mines_left = NUM_MINES-flags_placed
    counter_text = font.render(f"MINES {mines_left}", True, (0,0,0))
    screen.blit(counter_text, (10, 10))

    panel_rect = pygame.Rect(WIDTH*CELL_SIZE, 0, PANEL_WIDTH, HEIGHT*CELL_SIZE + HEADER_HEIGHT)
    pygame.draw.rect(screen, (220, 220, 220), panel_rect)
    pygame.draw.rect(screen, (0, 0, 0), panel_rect, 2)
    
    if not game_over and start_time is not None:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    else:
        elapsed_time = 0
    
    timer_text = font.render(f"Time: {elapsed_time}s", True, (0,0,0))
    screen.blit(timer_text, (WIDTH*CELL_SIZE + 10, HEADER_HEIGHT + 10))

def chord(row,col):
    flagged_count = 0

    for r in range(row-1, row+2):
        for c in range(col-1, col+2):
            if not (0<=r<HEIGHT and 0<=c<WIDTH):
                continue
            if flagged[r][c]:
                flagged_count += 1
    
    if flagged_count == numbers[row][col]:
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if not (0<=r<HEIGHT and 0<=c<WIDTH):
                    continue
                if revealed[r][c] or flagged[r][c]:
                    continue

                reveal_cell(r, c)
    
def reveal_cell(row, col):
    global game_over

    if not(0 <= row < HEIGHT and 0 <= col < WIDTH):
        return
    
    if flagged[row][col]:
        return
    
    if numbers[row][col] == 0:
        flood_fill(row,col)
    
    revealed[row][col] = True

    if numbers[row][col] == -1:
        print("Game over! L bozo")
        game_over = True

def handle_click(row,col):
    global game_over
    global start_time

    if game_over: return

    if start_time is None:
        start_time = pygame.time.get_ticks()

    if numbers[row][col]>0 and revealed[row][col]:
        chord(row, col)
        return
    
    if flagged[row][col]: return

    reveal_cell(row,col)

def flood_fill(row, col):
    #TODO: fix wrong logic

    if not(0 <= row < HEIGHT and 0 <= col < WIDTH):
        return

    if numbers[row][col] == -1 or revealed[row][col]:
        return
    
    revealed[row][col] = True
    
    if numbers[row][col] != 0:
        return
    
    for r in range(row-1, row+2):
        for c in range(col-1, col+2):
            if r==row and c==col: continue
            flood_fill(r,c)

def flag():
    global flags_placed
    x,y = pygame.mouse.get_pos()

    row = (y-HEADER_HEIGHT)//CELL_SIZE
    col = x//CELL_SIZE

    board_row = scroll_y + row
    board_col = scroll_x + col

    if not (0 <= board_row < HEIGHT and 0 <= board_col < WIDTH):
        return
    
    if revealed[board_row][board_col]:
        return
    
    flagged[board_row][board_col] = not flagged[board_row][board_col]

    if flagged[board_row][board_col]:
        flags_placed += 1
    else:
        flags_placed -= 1

def new_game():
    global flags_placed, game_over, mines, numbers, revealed, flagged, mine_positions, start_time, scroll_x, scroll_y

    positions = [(r,c) for r in range(HEIGHT) for c in range(WIDTH)]
    mines = [[False]*WIDTH for _ in range(HEIGHT)]
    numbers = [[0]*WIDTH for _ in range(HEIGHT)]
    revealed = [[False]*WIDTH for _ in range(HEIGHT)]
    flagged = [[False]*WIDTH for _ in range(HEIGHT)]

    scroll_x = 0
    scroll_y = 0

    start_time = None

    flags_placed = 0

    game_over = False

    mine_positions = random.sample(positions, NUM_MINES)

    for pos in mine_positions:
        mines[pos[0]][pos[1]] = True

    for r in range(HEIGHT):
        for c in range(WIDTH):
            set_cell_number(mines, numbers, r, c)

new_game()

print_board(mines, numbers)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()

            row = (y-HEADER_HEIGHT)//CELL_SIZE
            col = x//CELL_SIZE
            board_row = scroll_y + row
            board_col = scroll_x + col

            if 0 <= board_row < HEIGHT and 0 <= board_col < WIDTH:
                handle_click(board_row, board_col)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                flag()
            
            if event.key == pygame.K_q:
                x,y=pygame.mouse.get_pos()
                row=(y-HEADER_HEIGHT)//CELL_SIZE
                col = x//CELL_SIZE
                board_row = scroll_y + row
                board_col = scroll_x + col
                
                if 0 <= board_row < HEIGHT and 0 <= board_col < WIDTH:
                    handle_click(board_row, board_col)
            
            if event.key == pygame.K_r:
                new_game()

            visible_width = (screen.get_width() - PANEL_WIDTH) // CELL_SIZE
            visible_height = (screen.get_height() - HEADER_HEIGHT) // CELL_SIZE
            
            if event.key == pygame.K_UP:
                scroll_y = max(0, min(scroll_y - 1, HEIGHT - visible_height))
            elif event.key == pygame.K_DOWN:
                scroll_y = max(0, min(scroll_y + 1, HEIGHT - visible_height))
            elif event.key == pygame.K_LEFT:
                scroll_x = max(0, min(scroll_x - 1, WIDTH - visible_width))
            elif event.key == pygame.K_RIGHT:
                scroll_x = max(0, min(scroll_x + 1, WIDTH - visible_width))
    
    draw_board()
    pygame.display.update()

    clock.tick(60)

pygame.quit()