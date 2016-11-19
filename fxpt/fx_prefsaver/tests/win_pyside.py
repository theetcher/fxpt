import sys

from fxpt.qt.pyside import QtWidgets

import qt_window_test


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = qt_window_test.TestQtWindow(qt_window_test.TestQtWindow.QtTypePySide, 'SerializerFileJson', parent=None)
    win.show()
    app.exec_()
    sys.exit()

