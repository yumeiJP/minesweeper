import pygame
import random

pygame.init()

screen = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()

WIDTH = 9
HEIGHT = 9
NUM_MINES = 10

positions = [(r,c) for r in range(HEIGHT) for c in range(WIDTH)]
mines = [[False]*WIDTH for _ in range(HEIGHT)]
numbers = [[0]*WIDTH for _ in range(HEIGHT)]

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

for pos in mine_positions:
    mines[pos[0]][pos[1]] = True

for r in range(HEIGHT):
    for c in range(WIDTH):
        if mines[r][c] == True:
            numbers[r][c] = -1
            continue
        
        count = 0
        
        for row in range(r-1, r+2):
            for column in range(c-1, c+2):
                if row == r and column == c:
                    continue

                has_mine = check_if_mine(row,column,mines)
                if has_mine:
                    count += 1
        
        numbers[r][c] = count

print_board()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()

    clock.tick(60)

pygame.quit()