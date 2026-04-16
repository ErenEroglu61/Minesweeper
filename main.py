import sys
from PyQt5.QtWidgets import QApplication
from widgets import BoardWidget

def main():
    app = QApplication(sys.argv)

    window = BoardWidget(8, 8, 10)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()