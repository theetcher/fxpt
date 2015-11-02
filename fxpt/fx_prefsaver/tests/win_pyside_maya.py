import shiboken

from PySide import QtGui
import maya.OpenMayaUI as apiUI

import qt_window_test


mainWin = None


def run(serializer):

    global mainWin
    if not mainWin:
        ptr = apiUI.MQtUtil.mainWindow()
        if ptr:
            mainWinQObject = shiboken.wrapInstance(long(ptr), QtGui.QMainWindow)
        else:
            raise Exception('Cannot find Maya main window.')
        mainWin = qt_window_test.TestQtWindow(qt_window_test.TestQtWindow.QtTypePySide, serializer, parent=mainWinQObject)

    mainWin.show()
    mainWin.raise_()


