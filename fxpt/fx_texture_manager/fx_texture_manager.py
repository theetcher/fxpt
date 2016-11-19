import maya.OpenMayaUI as apiUI

from fxpt.qt.pyside import QtWidgets, shiboken2

from fxpt.fx_texture_manager import main_window

mainWin = None


def getMayaMainWindowPtr():
    ptr = apiUI.MQtUtil.mainWindow()
    if not ptr:
        raise RuntimeError('Cannot find Maya main window.')
    else:
        return ptr


def getMayaQMainWindow(ptr):
    return shiboken2.wrapInstance(long(ptr), QtWidgets.QMainWindow)


def run():
    global mainWin
    if not mainWin:
        mayaMainWin = getMayaQMainWindow(getMayaMainWindowPtr())
        mainWin = main_window.TexManagerUI(mayaMainWin)
    mainWin.show()
    mainWin.raise_()


