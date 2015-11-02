import sys

from PySide import QtGui

import model_win_test


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = model_win_test.TestModelWin()
    win.show()
    app.exec_()
    sys.exit()

