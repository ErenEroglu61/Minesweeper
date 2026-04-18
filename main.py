import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from widgets.board_widgets import BoardWidget

def main():
    app = QApplication(sys.argv)

    window = BoardWidget(8, 8, 10)
    window.setWindowTitle("Minesweeper")
    window.setWindowIcon(QIcon('UI/resources/flag.png'))
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()