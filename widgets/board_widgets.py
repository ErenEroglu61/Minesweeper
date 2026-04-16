from PyQt5.QtWidgets import QWidget, QGridLayout, QMessageBox
from core.board import Board
from widgets.cell_widget import CellWidget
from PyQt5.QtGui import QIcon
from services.sound_manager import SoundManager


class BoardWidget(QWidget):
    def __init__(self, rows=8, cols=8, mines=10):
        super().__init__()

        self.board = Board(rows, cols, mines)
        self.sound = SoundManager()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.cells = []

        self.init_ui()

    def init_ui(self):
        for r in range(self.board.rows):
            row_cells = []
            for c in range(self.board.cols):
                cell_btn = CellWidget(r, c)

                # LEFT CLICK
                cell_btn.clicked.connect(
                    lambda _, r=r, c=c: self.handle_click(r, c)
                )

                # RIGHT CLICK
                cell_btn.right_clicked.connect(self.handle_right_click)

                self.layout.addWidget(cell_btn, r, c)
                row_cells.append(cell_btn)

            self.cells.append(row_cells)

    # 🖱️ LEFT CLICK
    def handle_click(self, r, c):
        cell = self.board.grid[r][c]

        if cell.is_flagged:
            return

        result = self.board.reveal_cell(r, c)

        if result == "mine":
            self.sound.play_explosion()
            self.show_game_over()
        else:
            self.sound.play_click()

            # 🏆 WIN CHECK
            if self.board.check_win():
                self.show_win()

        self.update_ui()

    # 🖱️ RIGHT CLICK
    def handle_right_click(self, r, c):
        cell = self.board.grid[r][c]

        if cell.is_revealed:
            return

        cell.is_flagged = not cell.is_flagged
        self.update_ui()

    # 💥 LOSE
    def show_game_over(self):
        QMessageBox.information(self, "Game Over", "You hit a mine!")

    # 🏆 WIN
    def show_win(self):
        QMessageBox.information(self, "Victory", "You win! 🎉")

    # 🔄 UPDATE UI
    def update_ui(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                btn = self.cells[r][c]

                if cell.is_flagged:
                    btn.setIcon(QIcon("ui/resources/flag.png"))

                elif cell.is_revealed:
                    if cell.is_mine:
                        btn.setIcon(QIcon("ui/resources/mine.png"))
                    else:
                        if cell.neighbor_mines > 0:
                            btn.setIcon(QIcon(f"ui/resources/numbers/{cell.neighbor_mines}.png"))
                        btn.setEnabled(False)