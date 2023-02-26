from PyQt5 import QtWidgets as Qt
import sys
import traceback
from app import App


def main():
    app_ = Qt.QApplication(sys.argv)
    win = Qt.QMainWindow()
    app = App(win)
    app.run()
    sys.exit(app_.exec_())


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        traceback.print_exc()
