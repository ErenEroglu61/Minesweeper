from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt


class CellWidget(QPushButton):
    right_clicked = pyqtSignal(int, int)

    def __init__(self, row, col):
        super().__init__()

        self.row = row
        self.col = col

        self.setFixedSize(40, 40)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.right_clicked.emit(self.row, self.col)
        else:
            super().mousePressEvent(event)