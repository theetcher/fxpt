import sys

from PySide import QtGui

import TestModelWin


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = TestModelWin.TestModelWin()
    win.show()
    app.exec_()
    sys.exit()

