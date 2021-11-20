from MainWindow import MainWindow
from PySide6.QtWidgets import QApplication
import sys


def main():

    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = MainWindow()
    ex.show()
    print("here goes")
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
