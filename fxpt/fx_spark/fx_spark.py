from fxpt.qt.pyside import shiboken2, QtWidgets

import maya.OpenMayaUI as omui

from . import spark_ui


def getMayaWin():
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)  # or you can use QMainWindow
    else:
        raise RuntimeError('Cannot find main Maya window.')


def run():
    ui = spark_ui.SparkUI(getMayaWin())
    ui.show()
    ui.raise_()
