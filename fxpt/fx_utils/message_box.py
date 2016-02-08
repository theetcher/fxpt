import traceback

from PySide import QtGui


def messageBox(
        parent=None,
        title='Error',
        text='',
        textInformative='Press "Show Details" for more information',
        textDetailed=None,
        icon=QtGui.QMessageBox.Critical,
        width=600
):

    dlg = QtGui.QMessageBox(parent)
    dlg.setWindowTitle(title)
    dlg.setText(text)
    dlg.setInformativeText(textInformative)
    dlg.setDetailedText(textDetailed if textDetailed is not None else traceback.format_exc())
    dlg.setIcon(icon)

    # hack for making predefined width message box
    if width:
        spacer = QtGui.QSpacerItem(width, 0, QtGui.QSizePolicy.Minimum, QtGui. QSizePolicy.Expanding)
        gridLayout = dlg.layout()
        gridLayout.addItem(spacer, gridLayout.rowCount(), 0, 1, gridLayout.columnCount())

    dlg.exec_()
