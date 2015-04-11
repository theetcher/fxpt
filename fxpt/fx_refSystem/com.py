from PySide import QtGui
import shiboken

import maya.cmds as m
import maya.OpenMayaUI as omui

import log_dialog

from global_prefs_handler import GlobalPrefsHandler

globalPrefsHandler = GlobalPrefsHandler()

REF_ROOT_VAR_NAME = 'FX_REF_ROOT'
REF_ROOT_VAR_NAME_P = '%{}%'.format(REF_ROOT_VAR_NAME)

log = log_dialog.LogDialog()


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
