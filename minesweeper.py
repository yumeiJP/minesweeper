import pygame
import random

pygame.init()

screen = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()

WIDTH = 9
HEIGHT = 9
NUM_MINES = 10
CELL_SIZE = 40
COLORS = {
    "GRAY": (128, 128, 128),
    "LIGHT_GRAY": (192,192,192),
    "WHITE": (255,255,255)
}

positions = [(r,c) for r in range(HEIGHT) for c in range(WIDTH)]
mines = [[False]*WIDTH for _ in range(HEIGHT)]
numbers = [[0]*WIDTH for _ in range(HEIGHT)]
revealed = [[False]*WIDTH for _ in range(HEIGHT)]

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
    
def mouse_click(event):
    x,y = event.pos

    row = y//CELL_SIZE
    col = x//CELL_SIZE

    if not(0 <= row < HEIGHT and 0 <= col < WIDTH):
        return
    
    if revealed[row][col]:
        return
    
    revealed[row][col] = True

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
            mouse_click(event)

    
    draw_board()
    pygame.display.update()

    clock.tick(60)

pygame.quit()