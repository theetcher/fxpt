import os

from PySide import QtGui
import shiboken

import maya.cmds as m
import maya.OpenMayaUI as omui

from fxpt.fx_utils.utils import cleanupPath

from global_prefs_handler import GlobalPrefsHandler

globalPrefsHandler = GlobalPrefsHandler()

REF_ROOT_VAR_NAME = 'FX_REF_ROOT'
REF_ROOT_VAR_NAME_P = '%{}%'.format(REF_ROOT_VAR_NAME)


# noinspection PyDefaultArgument
def messageBoxMaya(message, title='Error', icon='critical', button=['Close'], defaultButton='Close', cancelButton='Close', dismissString='Close'):
    return m.confirmDialog(
        title=title,
        message=message,
        button=button,
        defaultButton=defaultButton,
        cancelButton=cancelButton,
        dismissString=dismissString,
        icon=icon
    )


def getMayaQMainWindow():
    # noinspection PyArgumentList
    ptr = omui.MQtUtil.mainWindow()
    if not ptr:
        raise RuntimeError('Cannot find Maya main window.')
    return shiboken.wrapInstance(long(ptr), QtGui.QMainWindow)


def getRefRootValue():
    return cleanupPath(os.environ.get(REF_ROOT_VAR_NAME, ''))


def isPathRelative(path):
    return path.lower().startswith(REF_ROOT_VAR_NAME_P.lower())


def getRelativePath(path):
    pathWorking = cleanupPath(path)

    refRootValueLower = getRefRootValue().lower()
    if not refRootValueLower:
        return pathWorking

    if isPathRelative(pathWorking):
        return pathWorking

    pathLower = pathWorking.lower()
    if pathLower.startswith(refRootValueLower):
        return REF_ROOT_VAR_NAME_P + pathWorking[len(refRootValueLower):]

    return path
