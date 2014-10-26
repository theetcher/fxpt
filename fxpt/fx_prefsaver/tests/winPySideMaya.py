from PySide import QtGui
import shiboken
import maya.OpenMayaUI as apiUI

import TestQtWindow

mainWin = None


def run():

    global mainWin
    if not mainWin:
        ptr = apiUI.MQtUtil.mainWindow()
        if ptr:
            mainWinQObject = shiboken.wrapInstance(long(ptr), QtGui.QMainWindow)  # or you can use QMainWindow
        else:
            raise Exception('Cannot find Maya main window.')
        mainWin = TestQtWindow.TestQtWindow(TestQtWindow.TestQtWindow.QtTypePySide, parent=mainWinQObject)

    mainWin.show()
    mainWin.raise_()


