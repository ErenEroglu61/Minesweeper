from PyQt5.QtWidgets import QWidget, QGridLayout, QMessageBox
from core.board import Board
from widgets.cell_widgets import CellWidget
from services.sound_manager import SoundManager
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from widgets.settings_panel import SettingsPanel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout

class BoardWidget(QWidget):
    def __init__(self, rows=8, cols=8, mines=10):
        super().__init__()

        self.board = Board(rows, cols, mines)
        self.sound = SoundManager()

        # LAYOUTS
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # 🔝 TOP BAR
        self.top_bar = QHBoxLayout()
        self.main_layout.addLayout(self.top_bar)

        # 🔄 Restart Button
        self.restart_btn = QPushButton("🔄")
        self.restart_btn.clicked.connect(self.restart_game)
        self.top_bar.addWidget(self.restart_btn)

        # ⏱ Timer (center)
        self.timer_label = QLabel("Time: 0")
        self.top_bar.addWidget(self.timer_label)

        # spacer (push settings to right)
        self.top_bar.addStretch()

        # ⚙️ Settings Button (right)
        self.settings_btn = QPushButton("⚙")
        self.settings_btn.clicked.connect(self.toggle_settings)
        self.top_bar.addWidget(self.settings_btn)

        self.grid_layout = QGridLayout()
        self.main_layout.addLayout(self.grid_layout)


        # SETTINGS PANEL
        self.settings_panel = SettingsPanel(self.apply_settings)
        self.settings_panel.hide()
        self.main_layout.addWidget(self.settings_panel)

        self.cells = []

        # TIMER
        self.time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        self.init_ui()

    def restart_game(self):
        reply = QMessageBox.question(
            self,
            "Restart",
            "Are you sure you want to restart?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        rows = self.board.rows
        cols = self.board.cols
        mines = self.board.mines

        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.cells = []

        self.board = Board(rows, cols, mines)

        self.time = 0
        self.timer_label.setText("Time: 0")

        self.init_ui()


    def init_ui(self):
        for r in range(self.board.rows):
            row_cells = []
            for c in range(self.board.cols):
                cell_btn = CellWidget(r, c)

                cell_btn.clicked.connect(
                    lambda _, r=r, c=c: self.handle_click(r, c)
                )

                cell_btn.right_clicked.connect(self.handle_right_click)

                self.grid_layout.addWidget(cell_btn, r, c)
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
            self.disable_board()

        else:
            self.sound.play_click()

            if self.board.check_win():
                self.show_win()
                self.disable_board()

        self.update_ui()

    def apply_settings(self, rows, cols, mines):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.cells = []

        # new board
        self.board = Board(rows, cols, mines)

        self.time = 0
        self.timer_label.setText("Time: 0")

        self.init_ui()

        self.settings_panel.hide()

    def toggle_settings(self):
        if self.settings_panel.isVisible():
            self.settings_panel.hide()
        else:
            self.settings_panel.show()

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

    # 🔒 Disable board
    def disable_board(self):
        for row in self.cells:
            for btn in row:
                btn.setEnabled(False)

    def update_timer(self):
        self.time += 1
        self.timer_label.setText(f"Time: {self.time}")

    def update_ui(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]
                btn = self.cells[r][c]

                btn.setIcon(QIcon())  # reset

                if cell.is_flagged:
                    btn.setIcon(QIcon("ui/resources/flag.png"))

                elif cell.is_revealed:
                    if cell.is_mine:
                        btn.setIcon(QIcon("ui/resources/mine.png"))
                    else:
                        if cell.neighbor_mines > 0:
                            btn.setIcon(QIcon(f"ui/resources/numbers/{cell.neighbor_mines}.png"))

                    btn.setEnabled(False)

                else:
                    # 👇 default hidden cell
                    btn.setIcon(QIcon("ui/resources/my_icon.jpg"))