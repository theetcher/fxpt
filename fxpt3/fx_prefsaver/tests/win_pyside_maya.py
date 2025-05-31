# noinspection PyUnresolvedReferences
from maya import OpenMayaUI as omui

from fxpt3.qt.pyside import QtWidgets, shiboken
from fxpt3.fx_prefsaver.tests import qt_window_test


toolMainWin = None


def run(serializer):

    global toolMainWin
    if not toolMainWin:
        ptr = omui.MQtUtil.mainWindow()
        if ptr:
            mainWinQObject = shiboken.wrapInstance(int(ptr), QtWidgets.QMainWindow)
        else:
            raise Exception('Cannot find Maya main window.')
        toolMainWin = qt_window_test.TestQtWindow(serializer, parent=mainWinQObject)
        # mainWin = qt_window_test.TestQtWindow(qt_window_test.TestQtWindow.QtTypePySide2, serializer, parent=None)

    toolMainWin.show()
    toolMainWin.raise_()
