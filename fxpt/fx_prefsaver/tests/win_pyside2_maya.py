from fxpt.qt.pyside import QtWidgets, shiboken2

import maya.OpenMayaUI as apiUI

import qt_window_test


mainWin = None


def run(serializer):

    global mainWin
    if not mainWin:
        ptr = apiUI.MQtUtil.mainWindow()
        if ptr:
            mainWinQObject = shiboken2.wrapInstance(long(ptr), QtWidgets.QMainWindow)
        else:
            raise Exception('Cannot find Maya main window.')
        mainWin = qt_window_test.TestQtWindow(qt_window_test.TestQtWindow.QtTypePySide2, serializer, parent=mainWinQObject)

    mainWin.show()
    mainWin.raise_()


