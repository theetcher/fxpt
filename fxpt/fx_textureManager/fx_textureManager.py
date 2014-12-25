import maya.OpenMayaUI as apiUI
import shiboken
from PySide import QtGui

from fxpt.fx_textureManager import MainWindow

mainWin = None


def getMayaMainWindowPtr():
    ptr = apiUI.MQtUtil.mainWindow()
    if not ptr:
        raise RuntimeError('Cannot find Maya main window.')
    else:
        return ptr


def getMayaQMainWindow(ptr):
    return shiboken.wrapInstance(long(ptr), QtGui.QMainWindow)


def run():
    global mainWin
    if not mainWin:
        mayaMainWin = getMayaQMainWindow(getMayaMainWindowPtr())
        mainWin = MainWindow.TexManagerUI(mayaMainWin)
    mainWin.show()
    mainWin.raise_()


