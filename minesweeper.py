import pygame
import random

pygame.init()

WIDTH = 15
HEIGHT = 15
NUM_MINES = 60
CELL_SIZE = 40
COLORS = {
    "GRAY": (128, 128, 128),
    "LIGHT_GRAY": (192,192,192),
    "WHITE": (255,255,255)
}

screen = pygame.display.set_mode((WIDTH*CELL_SIZE, HEIGHT*CELL_SIZE))
clock = pygame.time.Clock()

positions = [(r,c) for r in range(HEIGHT) for c in range(WIDTH)]
mines = [[False]*WIDTH for _ in range(HEIGHT)]
numbers = [[0]*WIDTH for _ in range(HEIGHT)]
revealed = [[False]*WIDTH for _ in range(HEIGHT)]
flagged = [[False]*WIDTH for _ in range(HEIGHT)]

font = pygame.font.SysFont('Arial', 24)

mine_positions = random.sample(positions, NUM_MINES)

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

    for row in range(HEIGHT):
        for col in range(WIDTH):
            x = col * CELL_SIZE
            y = row * CELL_SIZE

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

    if not(0 <= row < HEIGHT and 0 <= col < WIDTH):
        return
    
    if flagged[row][col]:
        return
    
    if numbers[row][col] == 0:
        flood_fill(row,col)
    
    revealed[row][col] = True

    if numbers[row][col] == -1:
        print("Game over! L bozo")
        #game over

def handle_click(row,col):
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
    x,y = pygame.mouse.get_pos()

    row = y//CELL_SIZE
    col = x//CELL_SIZE

    if not(0 <= row < HEIGHT and 0 <= col < WIDTH):
        return
    
    if revealed[row][col]:
        return
    
    flagged[row][col] = not flagged[row][col]
    


for pos in mine_positions:
    mines[pos[0]][pos[1]] = True

for r in range(HEIGHT):
    for c in range(WIDTH):
        set_cell_number(mines, numbers, r, c)


print_board(mines, numbers)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()

            row = y//CELL_SIZE
            col = x//CELL_SIZE
            handle_click(row, col)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                flag()
            
            if event.key == pygame.K_q:
                x,y=pygame.mouse.get_pos()
                row=y//CELL_SIZE
                col = x//CELL_SIZE
                handle_click(row,col)
    
    draw_board()
    pygame.display.update()

    clock.tick(60)

pygame.quit()