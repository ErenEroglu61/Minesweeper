import sys
import ctypes
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from widgets.board_widget import BoardWidget
from utils.path import resource_path

myappid = 'mycompany.minesweeper.app.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def main():
    app = QApplication(sys.argv)
    app.setApplicationDisplayName("Minesweeper")
    app.setWindowIcon(QIcon(resource_path("ui/resources/flag.ico")))

    window = BoardWidget(8, 8, 10)
    window.setWindowTitle("Minesweeper")
    window.setWindowIcon(QIcon(resource_path('UI/resources/flag.ico')))
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()