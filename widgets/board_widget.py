from PyQt5.QtWidgets import QWidget, QGridLayout, QMessageBox
from core.board import Board
from widgets.cell_widget import CellWidget
from services.sound_manager import SoundManager
from PyQt5.QtWidgets import QVBoxLayout, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from widgets.settings_panel import SettingsPanel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import QSize
from config import BUTTON_STYLE
from config import  WINDOW_STYLE
from utils.path import resource_path


class BoardWidget(QWidget):
    def __init__(self, rows=8, cols=8, mines=10):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e1e2f,
                    stop:1 #2a2a40
                );
            }
        """)

        self.board = Board(rows, cols, mines)
        self.sound = SoundManager()

        # LAYOUTS
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # TOP BAR
        self.top_bar = QHBoxLayout()
        self.main_layout.addLayout(self.top_bar)

        # Restart
        self.restart_btn = QPushButton("🔄")
        self.restart_btn.clicked.connect(self.restart_game)
        self.restart_btn.setStyleSheet(BUTTON_STYLE)

        self.mines_label = QLabel(f"Mines: {self.board.mines}")
        self.mines_label.setStyleSheet("color: white; font-weight: bold;")


        # Timer
        self.timer_label = QLabel("Time: 0")
        self.timer_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
        """)

        # ️ Settings
        self.settings_btn = QPushButton("⚙")
        self.settings_btn.clicked.connect(self.toggle_settings)

        # Layout order (centered)
        self.top_bar.addWidget(self.restart_btn)
        self.top_bar.addStretch()
        self.top_bar.addWidget(self.mines_label)
        self.top_bar.addWidget(self.timer_label)
        self.top_bar.addStretch()
        self.top_bar.addWidget(self.settings_btn)

        # GRID WRAPPER centered
        self.grid_wrapper = QHBoxLayout()
        self.main_layout.addLayout(self.grid_wrapper)

        self.grid_wrapper.addStretch()

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(2)
        self.grid_wrapper.addLayout(self.grid_layout)

        self.grid_wrapper.addStretch()


        # SETTINGS PANEL
        self.settings_panel = SettingsPanel(self.apply_settings)
        self.settings_panel.hide()
        self.main_layout.addWidget(self.settings_panel)
        self.main_layout.insertWidget(1, self.settings_panel)

        self.restart_btn.setFixedSize(40, 40)
        self.settings_btn.setFixedSize(40, 40)

        self.cells = []

        # TIMER
        self.time = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.remaining_mines = self.board.mines
        self.mines_label.setText(f"Mines: {self.remaining_mines}")

        self.init_ui()

    def restart_game(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Restart")
        msg.setText("Are you sure you want to restart?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # background css
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1e1e2f;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
        """)

        # button css
        yes_btn = msg.button(QMessageBox.Yes)
        no_btn = msg.button(QMessageBox.No)

        yes_btn.setStyleSheet("""
            background-color: #3a3a5a;
            color: white;
            border-radius: 6px;
            padding: 5px;
        """)

        no_btn.setStyleSheet("""
            background-color: #3a3a5a;
            color: white;
            border-radius: 6px;
            padding: 5px;
        """)

        reply = msg.exec_()

        if reply == QMessageBox.No:
            return

        self.remaining_mines = self.board.mines
        self.mines_label.setText(f"Mines: {self.remaining_mines}")

        # restart logic
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
        self.timer.start(1000)

        self.init_ui()

    def init_ui(self):
        for r in range(self.board.rows):
            row_cells = []

            for c in range(self.board.cols):
                cell_btn = CellWidget(r, c)

                cell_btn.setMinimumSize(40, 40)
                cell_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                cell_btn.setIconSize(QSize(32, 32))

                cell_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2a2a40;
                        border-radius: 8px;
                        border: 1px solid #3a3a5a;
                    }
                    QPushButton:hover {
                        background-color: #3a3a5a;
                    }
                    QPushButton:pressed {
                        background-color: #1a1a2a;
                    }
                """)
                cell_btn.clicked.connect(
                    lambda _, r=r, c=c: self.handle_click(r, c)
                )

                cell_btn.right_clicked.connect(self.handle_right_click)

                self.grid_layout.addWidget(cell_btn, r, c)

                row_cells.append(cell_btn)

            self.cells.append(row_cells)
    #  LEFT CLICK
    def handle_click(self, r, c):
        cell = self.board.grid[r][c]

        if cell.is_flagged:
            return

        # Smart Click if flags == num reveal all neighbors
        if cell.is_revealed:
            results = self.board.reveal_neighbors_if_flags_match(r, c)

            if results:
                if any(r == "mine" for r in results):
                    self.sound.play_explosion()
                    self.show_game_over()
                    self.disable_board()
                else:
                    self.sound.play_click()

                    if self.board.check_win():
                        self.show_win()
                        self.disable_board()

            self.update_ui()
            return

        result = self.board.reveal_cell(r, c)

        if result == "mine":
            self.sound.play_explosion()

            self.reveal_all_mines()
            self.update_ui()

            self.show_game_over()
            self.disable_board()
        else:
            self.sound.play_click()

            if self.board.check_win():
                self.show_win()
                self.disable_board()

        self.update_ui()

    def apply_settings(self, rows, cols, mines):
        self.timer.start(1000)
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.cells = []

        self.board = Board(rows, cols, mines)

        self.time = 0
        self.timer_label.setText("Time: 0")

        self.remaining_mines = self.board.mines
        self.mines_label.setText(f"Mines: {self.remaining_mines}")

        self.init_ui()

        self.settings_panel.hide()

    def toggle_settings(self):
        if self.settings_panel.isVisible():
            self.settings_panel.hide()
        else:
            self.settings_panel.show()

    #  place flag with right click
    def handle_right_click(self, r, c):
        cell = self.board.grid[r][c]

        if cell.is_revealed:
            return

        if not cell.is_flagged:
            cell.is_flagged = True
            self.remaining_mines -= 1
        else:
            cell.is_flagged = False
            self.remaining_mines += 1

        self.mines_label.setText(f"Mines: {self.remaining_mines}")

        self.update_ui()

    def reveal_all_mines(self):
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                cell = self.board.grid[r][c]

                if cell.is_mine:
                    cell.is_revealed = True

    # LOSE
    def show_game_over(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Game Over")
        msg.setText("You hit a mine!")

        msg.setStyleSheet(WINDOW_STYLE)

        msg.exec_()

    # WIN
    def show_win(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Victory")
        msg.setText("You win! 🎉")

        msg.setStyleSheet(WINDOW_STYLE)

        msg.exec_()

    # Disable board
    def disable_board(self):
        for row in self.cells:
            for btn in row:
                btn.setEnabled(False)

        self.timer.stop()

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
                    btn.setIcon(QIcon(resource_path("ui/resources/flag.png")))

                elif cell.is_revealed:
                    btn.setStyleSheet("""
                        QPushButton {
                            background-color: #1a1a2a;
                            border-radius: 8px;
                            color: white;
                        }
                    """)
                    if cell.is_mine:
                        btn.setIcon(QIcon(resource_path("ui/resources/mine.png")))
                    else:
                        if cell.neighbor_mines > 0:
                            btn.setIcon(QIcon(resource_path(f"ui/resources/numbers/{cell.neighbor_mines}.png")))


                else:
                    btn.setIcon(QIcon(resource_path("ui/resources/my_icon.jpg")))