import sys

from PyQt4 import QtGui

import TestQtWindow


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = TestQtWindow.TestQtWindow(TestQtWindow.TestQtWindow.QtTypePyQt, 'SerializerFileJson', parent=None)
    win.show()
    app.exec_()
    sys.exit()

