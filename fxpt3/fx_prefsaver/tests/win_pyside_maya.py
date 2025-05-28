# noinspection PyUnresolvedReferences
from maya import OpenMayaUI as omui

from fxpt3.qt.pyside import QtWidgets, shiboken
from fxpt3.fx_prefsaver.tests import qt_window_test


mainWin = None


def run(serializer):

    global mainWin
    if not mainWin:
        ptr = omui.MQtUtil.mainWindow()
        if ptr:
            mainWinQObject = shiboken.wrapInstance(int(ptr), QtWidgets.QMainWindow)
        else:
            raise Exception('Cannot find Maya main window.')
        mainWin = qt_window_test.TestQtWindow(serializer, parent=mainWinQObject)
        # mainWin = qt_window_test.TestQtWindow(qt_window_test.TestQtWindow.QtTypePySide2, serializer, parent=None)

    mainWin.show()
    mainWin.raise_()
