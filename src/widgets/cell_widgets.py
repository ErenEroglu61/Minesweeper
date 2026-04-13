from PyQt5.QtWidgets import QPushButton

class CellWidget(QPushButton):
    def __init__(self, row, col):
        super().__init__()

        self.row = row
        self.col = col

        self.setFixedSize(40, 40)