import sip

from PyQt4 import QtGui
import maya.OpenMayaUI as apiUI

import qt_window_test


mainWin = None


def run(serializer):

    global mainWin
    if not mainWin:
        ptr = apiUI.MQtUtil.mainWindow()
        if ptr:
            mainWinQObject = sip.wrapinstance(long(ptr), QtGui.QMainWindow)
        else:
            raise Exception('Cannot find Maya main window.')
        mainWin = qt_window_test.TestQtWindow(qt_window_test.TestQtWindow.QtTypePyQt, serializer, parent=mainWinQObject)

    mainWin.show()
    mainWin.raise_()


