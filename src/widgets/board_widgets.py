from PyQt5.QtWidgets import QWidget, QGridLayout
from core.board import Board
from .cell_widget import CellWidget


class BoardWidget(QWidget):
    def __init__(self, rows=8, cols=8, mines=10):
        super().__init__()

        self.board = Board(rows, cols, mines)

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.cells = []

        self.init_ui()

    def init_ui(self):
        for r in range(self.board.rows):
            row_cells = []
            for c in range(self.board.cols):
                cell_btn = CellWidget(r, c)

                # 🔗 connect click
                cell_btn.clicked.connect(
                    lambda _, r=r, c=c: self.handle_click(r, c)
                )

                self.layout.addWidget(cell_btn, r, c)
                row_cells.append(cell_btn)

            self.cells.append(row_cells)

    def handle_click(self, r, c):
        result = self.board.reveal_cell(r, c)

        self.update_ui()

        if result == "mine":
            print("💥 Game Over")

    # Update ui
    def update_ui(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                btn = self.cells[r][c]

                if cell.is_revealed:
                    if cell.is_mine:
                        btn.setText("💣")
                    else:
                        btn.setText(str(cell.neighbor_mines) if cell.neighbor_mines > 0 else "")
                        btn.setEnabled(False)