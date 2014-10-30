from PyQt4 import QtCore
import sip
import maya.OpenMayaUI as apiUI

import TestQtWindow

mainWin = None


def run(serializer):

    global mainWin
    if not mainWin:
        ptr = apiUI.MQtUtil.mainWindow()
        if ptr:
            mainWinQObject = sip.wrapinstance(long(ptr), QtCore.QObject)
        else:
            raise Exception('Cannot find Maya main window.')
        mainWin = TestQtWindow.TestQtWindow(TestQtWindow.TestQtWindow.QtTypePyQt, serializer, parent=mainWinQObject)

    mainWin.show()
    mainWin.raise_()


