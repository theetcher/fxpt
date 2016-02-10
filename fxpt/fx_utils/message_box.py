import traceback

from PySide import QtGui

DEFAULT_WIDTH = 500

BTN_OK = QtGui.QMessageBox.Ok
BTN_OPEN = QtGui.QMessageBox.Open
BTN_SAVE = QtGui.QMessageBox.Save
BTN_CANCEL = QtGui.QMessageBox.Cancel
BTN_CLOSE = QtGui.QMessageBox.Close
BTN_DISCARD = QtGui.QMessageBox.Discard
BTN_APPLY = QtGui.QMessageBox.Apply
BTN_RESET = QtGui.QMessageBox.Reset
BTN_RESTORE_DEFAULTS = QtGui.QMessageBox.RestoreDefaults
BTN_HELP = QtGui.QMessageBox.Help
BTN_SAVE_ALL = QtGui.QMessageBox.SaveAll
BTN_YES = QtGui.QMessageBox.Yes
BTN_YES_TO_ALL = QtGui.QMessageBox.YesToAll
BTN_NO = QtGui.QMessageBox.No
BTN_NO_TO_ALL = QtGui.QMessageBox.NoToAll
BTN_ABORT = QtGui.QMessageBox.Abort
BTN_RETRY = QtGui.QMessageBox.Retry
BTN_IGNORE = QtGui.QMessageBox.Ignore
BTN_NO_BUTTON = QtGui.QMessageBox.NoButton

ICON_NONE = QtGui.QMessageBox.NoIcon
ICON_QUESTION = QtGui.QMessageBox.Question
ICON_INFORMATION = QtGui.QMessageBox.Information
ICON_WARNING = QtGui.QMessageBox.Warning
ICON_CRITICAL = QtGui.QMessageBox.Critical


def messageBox(
        text,
        parent=None,
        title=None,
        textInformative=None,
        textDetailed=None,
        icon=ICON_NONE,
        buttons=None,
        defaultButton=None,
        escapeButton=None,
        width=DEFAULT_WIDTH
):

    dlg = QtGui.QMessageBox(parent)
    if title:
        dlg.setWindowTitle(title)
    if text:
        dlg.setText(text)
    if textInformative:
        dlg.setInformativeText(textInformative)
    if textDetailed:
        dlg.setDetailedText(textDetailed)
    if buttons:
        dlg.setStandardButtons(buttons)
    if defaultButton:
        dlg.setDefaultButton(defaultButton)
    if escapeButton:
        dlg.setEscapeButton(escapeButton)
    dlg.setIcon(icon)

    # hack for making predefined width message box
    if width:
        # noinspection PyArgumentList
        spacer = QtGui.QSpacerItem(width, 0, QtGui.QSizePolicy.Minimum, QtGui. QSizePolicy.Expanding)
        gridLayout = dlg.layout()
        gridLayout.addItem(spacer, gridLayout.rowCount(), 0, 1, gridLayout.columnCount())

    return dlg.exec_()


def info(
        text,
        parent=None,
        title='Information',
        textInformative=None,
        textDetailed=None,
        width=DEFAULT_WIDTH
):

    return messageBox(
        text,
        parent=parent,
        title=title,
        textInformative=textInformative,
        textDetailed=textDetailed,
        icon=ICON_INFORMATION,
        width=width
    )


def warning(
        text,
        parent=None,
        title='Warning',
        textInformative=None,
        textDetailed=None,
        width=DEFAULT_WIDTH
):
    return messageBox(
        text,
        parent=parent,
        title=title,
        textInformative=textInformative,
        textDetailed=textDetailed,
        icon=ICON_WARNING,
        width=width
    )


def error(
        text,
        parent=None,
        title='Error',
        textInformative=None,
        textDetailed=None,
        width=DEFAULT_WIDTH
):

    return messageBox(
        text,
        parent=parent,
        title=title,
        textInformative=textInformative,
        textDetailed=textDetailed,
        icon=ICON_CRITICAL,
        width=width
    )


def exception(
        text,
        parent=None,
        title='Fatal Error',
        textInformative='Press "Show Details" for more information',
        width=DEFAULT_WIDTH
):
    return messageBox(
        text,
        parent=parent,
        title=title,
        textInformative=textInformative,
        textDetailed=traceback.format_exc(),
        icon=ICON_CRITICAL,
        width=width
    )
