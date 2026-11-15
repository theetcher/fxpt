import sys
import traceback

from fxpt3.qt.pyside import QtWidgets

DEFAULT_WIDTH = 500

BTN_OK = QtWidgets.QMessageBox.StandardButton.Ok
BTN_OPEN = QtWidgets.QMessageBox.StandardButton.Open
BTN_SAVE = QtWidgets.QMessageBox.StandardButton.Save
BTN_CANCEL = QtWidgets.QMessageBox.StandardButton.Cancel
BTN_CLOSE = QtWidgets.QMessageBox.StandardButton.Close
BTN_DISCARD = QtWidgets.QMessageBox.StandardButton.Discard
BTN_APPLY = QtWidgets.QMessageBox.StandardButton.Apply
BTN_RESET = QtWidgets.QMessageBox.StandardButton.Reset
BTN_RESTORE_DEFAULTS = QtWidgets.QMessageBox.StandardButton.RestoreDefaults
BTN_HELP = QtWidgets.QMessageBox.StandardButton.Help
BTN_SAVE_ALL = QtWidgets.QMessageBox.StandardButton.SaveAll
BTN_YES = QtWidgets.QMessageBox.StandardButton.Yes
BTN_YES_TO_ALL = QtWidgets.QMessageBox.StandardButton.YesToAll
BTN_NO = QtWidgets.QMessageBox.StandardButton.No
BTN_NO_TO_ALL = QtWidgets.QMessageBox.StandardButton.NoToAll
BTN_ABORT = QtWidgets.QMessageBox.StandardButton.Abort
BTN_RETRY = QtWidgets.QMessageBox.StandardButton.Retry
BTN_IGNORE = QtWidgets.QMessageBox.StandardButton.Ignore
BTN_NO_BUTTON = QtWidgets.QMessageBox.StandardButton.NoButton

ICON_NONE = QtWidgets.QMessageBox.Icon.NoIcon
ICON_QUESTION = QtWidgets.QMessageBox.Icon.Question
ICON_INFORMATION = QtWidgets.QMessageBox.Icon.Information
ICON_WARNING = QtWidgets.QMessageBox.Icon.Warning
ICON_CRITICAL = QtWidgets.QMessageBox.Icon.Critical


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
        spacer = QtWidgets.QSpacerItem(width, 0, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        gridLayout = dlg.layout()
        gridLayout.addItem(spacer, gridLayout.rowCount(), 0, 1, gridLayout.columnCount())

    # PySide6 has exec(), PySide2 only exec_()
    execFn = getattr(dlg, 'exec', None) or dlg.exec_
    # exec() returns a plain int; convert it so callers can compare with BTN_* (PySide6 enums don't compare with int)
    return QtWidgets.QMessageBox.StandardButton(execFn())


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
