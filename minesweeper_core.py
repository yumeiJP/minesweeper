import random

class MinesweeperCore:
    def __init__(self, width=30, height=16, num_mines=99):
        self.WIDTH = width
        self.HEIGHT = height
        self.NUM_MINES = num_mines
        self.reset()

    def reset(self):
        self.mines = [[False]*self.WIDTH for _ in range(self.HEIGHT)]
        self.numbers = [[0]*self.WIDTH for _ in range(self.HEIGHT)]
        self.revealed = [[False]*self.WIDTH for _ in range(self.HEIGHT)]
        self.flagged = [[False]*self.WIDTH for _ in range(self.HEIGHT)]
        self.flags_placed = 0
        self.game_over = False
        self.win = False
        self.first_click = True
        self.mines_placed = False

    def check_if_mine(self, r, c, mines):
        if r<0 or c<0 or r>=len(mines) or c>=len(mines[0]):
            return False
        if mines[r][c]:
            return True
        else:
            return False

    def set_cell_number(self, mines, numbers, r, c):
        if not(0 <= r < self.HEIGHT and 0 <= c < self.WIDTH):
            return
        if mines[r][c] == True:
            numbers[r][c] = -1
            return
        count = 0
        for row in range(r-1, r+2):
            for column in range(c-1, c+2):
                if row == r and column == c:
                    continue
                if self.check_if_mine(row, column, mines):
                    count += 1
        numbers[r][c] = count

    def place_mines(self, first_row, first_col):
        all_positions = [(r, c) for r in range(self.HEIGHT) for c in range(self.WIDTH)]
        all_positions.remove((first_row, first_col))
        mine_positions = random.sample(all_positions, self.NUM_MINES)
        for (r, c) in mine_positions:
            self.mines[r][c] = True
        for r in range(self.HEIGHT):
            for c in range(self.WIDTH):
                self.set_cell_number(self.mines, self.numbers, r, c)
        self.mines_placed = True

    def flood_fill(self, row, col):
        stack = [(row, col)]
        while stack:
            r, c = stack.pop()
            if not (0 <= r < self.HEIGHT and 0 <= c < self.WIDTH):
                continue
            if self.numbers[r][c] == -1 or self.revealed[r][c]:
                continue
            self.revealed[r][c] = True
            if self.numbers[r][c] != 0:
                continue
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    stack.append((r + dr, c + dc))

    def chord(self, row, col):
        flagged_count = 0
        for r in range(row-1, row+2):
            for c in range(col-1, col+2):
                if not (0<=r<self.HEIGHT and 0<=c<self.WIDTH):
                    continue
                if self.flagged[r][c]:
                    flagged_count += 1
        if flagged_count == self.numbers[row][col]:
            for r in range(row-1, row+2):
                for c in range(col-1, col+2):
                    if not (0<=r<self.HEIGHT and 0<=c<self.WIDTH):
                        continue
                    if self.revealed[r][c] or self.flagged[r][c]:
                        continue
                    self.reveal_cell(r, c)

    def reveal_cell(self, row, col):
        if not(0 <= row < self.HEIGHT and 0 <= col < self.WIDTH):
            return
        if self.flagged[row][col]:
            return
        if not self.mines_placed:
            self.place_mines(row, col)
        if self.numbers[row][col] == 0:
            self.flood_fill(row, col)
        else:
            self.revealed[row][col] = True
        if self.numbers[row][col] == -1:
            self.revealed[row][col] = True
            self.game_over = True
            return
        revealed_non_mine = sum(not self.mines[r][c] and self.revealed[r][c] for r in range(self.HEIGHT) for c in range(self.WIDTH))
        if revealed_non_mine == self.WIDTH * self.HEIGHT - self.NUM_MINES:
            self.win = True
            self.game_over = True

    def handle_click(self, row, col):
        if self.game_over:
            return
        if self.first_click:
            self.first_click = False
            if not self.mines_placed:
                self.place_mines(row, col)
        if self.numbers[row][col] > 0 and self.revealed[row][col]:
            self.chord(row, col)
            return
        if self.flagged[row][col]:
            return
        self.reveal_cell(row, col)

    def toggle_flag(self, row, col):
        if self.game_over or self.revealed[row][col]:
            return
        if not self.flagged[row][col]:
            self.flagged[row][col] = True
            self.flags_placed += 1
        else:
            self.flagged[row][col] = False
            self.flags_placed -= 1

    def get_state(self):
        state = []
        for r in range(self.HEIGHT):
            for c in range(self.WIDTH):
                state.append(1 if self.revealed[r][c] else 0)
                if self.revealed[r][c] and self.numbers[r][c] >= 0:
                    val = self.numbers[r][c] / 8.0
                else:
                    val = 0.0
                state.append(val)
                state.append(1 if self.flagged[r][c] else 0)
        return state

    def get_legal_actions(self):
        legal = []
        for r in range(self.HEIGHT):
            for c in range(self.WIDTH):
                if not self.revealed[r][c] and not self.flagged[r][c]:
                    legal.append((r, c))
        return legal

    def cells_cleared(self):
        count = 0
        for r in range(self.HEIGHT):
            for c in range(self.WIDTH):
                if self.revealed[r][c] and not self.mines[r][c]:
                    count += 1
        return count