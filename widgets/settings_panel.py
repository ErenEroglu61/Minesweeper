from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton


class SettingsPanel(QWidget):
    def __init__(self, apply_callback):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: #2a2a40;
                border-radius: 10px;
            }

            QLabel {
                color: white;
                font-size: 14px;
            }

            QSpinBox {
                background-color: #3a3a5a;
                color: white;
                border-radius: 5px;
                padding: 3px;
            }

            QPushButton {
                background-color: #4a4a6a;
                color: white;
                border-radius: 6px;
                padding: 5px;
            }

            QPushButton:hover {
                background-color: #5a5a7a;
            }
        """)

        self.apply_callback = apply_callback

        layout = QVBoxLayout()

        # ROWS
        layout.addWidget(QLabel("Rows"))
        self.rows_input = QSpinBox()
        self.rows_input.setRange(5, 30)
        layout.addWidget(self.rows_input)

        # COLS
        layout.addWidget(QLabel("Columns"))
        self.cols_input = QSpinBox()
        self.cols_input.setRange(5, 30)
        layout.addWidget(self.cols_input)

        # MINES
        layout.addWidget(QLabel("Mines"))
        self.mines_input = QSpinBox()
        self.mines_input.setRange(1, 200)
        layout.addWidget(self.mines_input)

        # APPLY BUTTON
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.apply_settings)
        layout.addWidget(apply_btn)

        self.setLayout(layout)

    def apply_settings(self):
        rows = self.rows_input.value()
        cols = self.cols_input.value()
        mines = self.mines_input.value()

        # limit mines dynamically
        max_mines = int(rows * cols * 0.2)
        mines = min(mines, max_mines)

        self.apply_callback(rows, cols, mines)