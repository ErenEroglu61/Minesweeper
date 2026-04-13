import random
from .cell import Cell


class Board:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]

        self.place_mines()
        self.calculate_neighbors()

    # Random mines
    def place_mines(self):
        placed = 0
        while placed < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)

            if not self.grid[r][c].is_mine:
                self.grid[r][c].is_mine = True
                placed += 1

    # numbers
    def calculate_neighbors(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].is_mine:
                    continue

                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc

                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.grid[nr][nc].is_mine:
                                count += 1

                self.grid[r][c].neighbor_mines = count

    # On-click
    def reveal_cell(self, r, c):
        cell = self.grid[r][c]

        if cell.is_revealed or cell.is_flagged:
            return

        cell.is_revealed = True

        #boom
        if cell.is_mine:
            return "mine"

        if cell.neighbor_mines == 0:
            self.flood_fill(r, c)

        return "safe"

    def flood_fill(self, r, c):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc

                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbor = self.grid[nr][nc]

                    if not neighbor.is_revealed and not neighbor.is_mine:
                        neighbor.is_revealed = True

                        if neighbor.neighbor_mines == 0:
                            self.flood_fill(nr, nc)