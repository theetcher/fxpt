import sys
import traceback

from fxpt.qt.pyside import QtWidgets

DEFAULT_WIDTH = 500

BTN_OK = QtWidgets.QMessageBox.Ok
BTN_OPEN = QtWidgets.QMessageBox.Open
BTN_SAVE = QtWidgets.QMessageBox.Save
BTN_CANCEL = QtWidgets.QMessageBox.Cancel
BTN_CLOSE = QtWidgets.QMessageBox.Close
BTN_DISCARD = QtWidgets.QMessageBox.Discard
BTN_APPLY = QtWidgets.QMessageBox.Apply
BTN_RESET = QtWidgets.QMessageBox.Reset
BTN_RESTORE_DEFAULTS = QtWidgets.QMessageBox.RestoreDefaults
BTN_HELP = QtWidgets.QMessageBox.Help
BTN_SAVE_ALL = QtWidgets.QMessageBox.SaveAll
BTN_YES = QtWidgets.QMessageBox.Yes
BTN_YES_TO_ALL = QtWidgets.QMessageBox.YesToAll
BTN_NO = QtWidgets.QMessageBox.No
BTN_NO_TO_ALL = QtWidgets.QMessageBox.NoToAll
BTN_ABORT = QtWidgets.QMessageBox.Abort
BTN_RETRY = QtWidgets.QMessageBox.Retry
BTN_IGNORE = QtWidgets.QMessageBox.Ignore
BTN_NO_BUTTON = QtWidgets.QMessageBox.NoButton

ICON_NONE = QtWidgets.QMessageBox.NoIcon
ICON_QUESTION = QtWidgets.QMessageBox.Question
ICON_INFORMATION = QtWidgets.QMessageBox.Information
ICON_WARNING = QtWidgets.QMessageBox.Warning
ICON_CRITICAL = QtWidgets.QMessageBox.Critical


def messageBox(
        text,
        parent=None,
        title=None,
        textInformative=None,
        textDetailed=None,
        icon=ICON_NONE,
        buttons=BTN_OK,
        defaultButton=BTN_OK,
        escapeButton=BTN_OK,
        width=DEFAULT_WIDTH
):

    dlg = QtWidgets.QMessageBox(parent)
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
        spacer = QtWidgets.QSpacerItem(width, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
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
        width=DEFAULT_WIDTH
):
    return messageBox(
        text,
        parent=parent,
        title=title,
        textInformative=str(sys.exc_info()[1]),
        textDetailed=traceback.format_exc(),
        icon=ICON_CRITICAL,
        width=width
    )
