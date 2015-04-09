from PySide import QtGui, QtCore


def removeInvalidClipboardData():
    oldMimeData = QtGui.qApp.clipboard().mimeData()
    newMimeData = QtCore.QMimeData()

    for fmt in oldMimeData.formats():
        if 'text/uri-list' in fmt:  # This breaks maya paste
            continue
        data = oldMimeData.data(fmt)
        newMimeData.setData(fmt, data)

    clipboard = QtGui.qApp.clipboard() 
    clipboard.blockSignals(True)
    clipboard.setMimeData(newMimeData)
    clipboard.blockSignals(False)


def fix():
    QtGui.qApp.clipboard().dataChanged.connect(removeInvalidClipboardData)