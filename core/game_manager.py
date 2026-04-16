class GameManager:
    def __init__(self):
        self.board = None

    def start_new_game(self, rows, cols, mines):
        self.board = Board(rows, cols, mines)

    def reveal(self, r, c):
        return self.board.reveal_cell(r, c)