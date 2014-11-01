# noinspection PyUnresolvedReferences
# import fxptToSysPath

import sys
from PySide import QtGui

import TestQtWindow


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = TestQtWindow.TestQtWindow(TestQtWindow.TestQtWindow.QtTypePySide, 'SerializerFilePickle', parent=None)
    win.show()
    app.exec_()
    sys.exit()

