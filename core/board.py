import random
from .cell import Cell


class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.first_click = True

    # 💣 Place mines (optimized)
    def place_mines(self):
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        mine_positions = random.sample(positions, self.mines)

        for r, c in mine_positions:
            self.grid[r][c].is_mine = True

    # 🔢 Calculate neighbor mine counts
    def calculate_neighbors(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].is_mine:
                    continue

                count = 0

                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:

                        # skip itself
                        if dr == 0 and dc == 0:
                            continue

                        nr, nc = r + dr, c + dc

                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.grid[nr][nc].is_mine:
                                count += 1

                self.grid[r][c].neighbor_mines = count

    # 🖱️ Reveal a cell
    def reveal_cell(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return "invalid"

        cell = self.grid[r][c]

        if cell.is_revealed or cell.is_flagged:
            return "ignored"

        # 🎯 FIRST CLICK LOGIC
        if self.first_click:
            self.first_click = False
            self.place_mines_safe(r, c)
            self.calculate_neighbors()

        cell.is_revealed = True

        if cell.is_mine:
            return "mine"

        if cell.neighbor_mines == 0:
            self.flood_fill(r, c)

        return "safe"

    def place_mines_safe(self, safe_r, safe_c):
        positions = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if not (r == safe_r and c == safe_c)  # ❗ SAFE CELL
        ]

        mine_positions = random.sample(positions, self.mines)

        for r, c in mine_positions:
            self.grid[r][c].is_mine = True

    # 🌊 Flood fill (recursive reveal)
    def flood_fill(self, r, c):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:

                nr, nc = r + dr, c + dc

                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbor = self.grid[nr][nc]

                    if neighbor.is_revealed or neighbor.is_mine:
                        continue

                    neighbor.is_revealed = True

                    if neighbor.neighbor_mines == 0:
                        self.flood_fill(nr, nc)

    # 🏆 Check win condition
    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]

                if not cell.is_mine and not cell.is_revealed:
                    return False

        return True