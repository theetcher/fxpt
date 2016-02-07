from PySide import QtGui, QtCore


class ResultsListWidget(QtGui.QListWidget):
    """
    :type searchLineEdit: QtGui.QLineEdit
    """
    def __init__(self):
        super(ResultsListWidget, self).__init__()
        self.searchLineEdit = None

    def setPartner(self, widget):
        self.searchLineEdit = widget

    # noinspection PyMethodOverriding
    def keyPressEvent(self, event):
        """
        :type event: QtGui.QKeyEvent
        """
        parentClass = super(ResultsListWidget, self)
        resultsCount = self.count()
        currentRow = self.currentRow()

        if event.key() == QtCore.Qt.Key_Up:
            if resultsCount and currentRow == 0:
                self.searchLineEdit.setFocus()
                self.clearSelection()
            else:
                parentClass.keyPressEvent(event)
        elif event.key() == QtCore.Qt.Key_Down:
            if resultsCount and currentRow == resultsCount - 1:
                self.searchLineEdit.setFocus()
                self.clearSelection()
            else:
                parentClass.keyPressEvent(event)
        else:
            parentClass.keyPressEvent(event)
