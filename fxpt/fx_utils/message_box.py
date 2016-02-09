import traceback

from PySide import QtGui

DEFAULT_WIDTH = 600


def messageDialog(
        parent=None,
        title=None,
        text=None,
        textInformative=None,
        textDetailed=None,
        icon=QtGui.QMessageBox.NoIcon,
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
    dlg.setIcon(icon)

    # hack for making predefined width message box
    if width:
        # noinspection PyArgumentList
        spacer = QtGui.QSpacerItem(width, 0, QtGui.QSizePolicy.Minimum, QtGui. QSizePolicy.Expanding)
        gridLayout = dlg.layout()
        gridLayout.addItem(spacer, gridLayout.rowCount(), 0, 1, gridLayout.columnCount())

    dlg.exec_()


def info(
        text,
        parent=None,
        title='Information',
        textInformative=None,
        textDetailed=None,
        width=DEFAULT_WIDTH
):

    messageDialog(
        text=text,
        parent=parent,
        title=title,
        textInformative=textInformative,
        textDetailed=textDetailed,
        icon=QtGui.QMessageBox.Information,
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
    messageDialog(
        text=text,
        parent=parent,
        title=title,
        textInformative=textInformative,
        textDetailed=textDetailed,
        icon=QtGui.QMessageBox.Warning,
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

    messageDialog(
        text=text,
        parent=parent,
        title=title,
        textInformative=textInformative,
        textDetailed=textDetailed,
        icon=QtGui.QMessageBox.Critical,
        width=width
    )


def exception(
        text,
        parent=None,
        title='Critical Error',
        textInformative='Press "Show Details" for more information',
        width=DEFAULT_WIDTH
):
    messageDialog(
        text=text,
        parent=parent,
        title=title,
        textInformative=textInformative,
        textDetailed=traceback.format_exc(),
        icon=QtGui.QMessageBox.Critical,
        width=width
    )
