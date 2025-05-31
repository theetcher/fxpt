# TODO: tests are not ported from Python 2

# noinspection PyUnresolvedReferences
from maya import OpenMayaUI as omui

from fxpt3.qt.pyside import QtWidgets, shiboken
from fxpt3.fx_texture_manager import main_window


toolMainWin = None


def run():

    global toolMainWin
    if not toolMainWin:
        ptr = omui.MQtUtil.mainWindow()
        if ptr:
            mainWinQObject = shiboken.wrapInstance(int(ptr), QtWidgets.QMainWindow)
        else:
            raise Exception('Cannot find Maya main window.')
        toolMainWin = main_window.TexManagerUI(mainWinQObject)

    toolMainWin.show()
    toolMainWin.raise_()