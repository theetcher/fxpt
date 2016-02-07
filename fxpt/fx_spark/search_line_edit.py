from PySide import QtGui, QtCore


class SearchLineEdit(QtGui.QLineEdit):
    """
    :type searchResultsList: QtGui.QListWidget
    """
    def __init__(self):
        super(SearchLineEdit, self).__init__()
        self.searchResultsList = None

    def setPartner(self, widget):
        self.searchResultsList = widget

    def keyPressEvent(self, event):
        """
        :type event: QtGui.QKeyEvent
        """
        resultsCount = self.searchResultsList.count()
        if event.key() == QtCore.Qt.Key_Up:
            if resultsCount:
                self.searchResultsList.setCurrentRow(resultsCount - 1)
                self.searchResultsList.setFocus()
        elif event.key() == QtCore.Qt.Key_Down:
            if resultsCount:
                self.searchResultsList.setCurrentRow(0)
                self.searchResultsList.setFocus()
        elif event.key() == QtCore.Qt.Key_Enter:
            pass
        else:
            super(SearchLineEdit, self).keyPressEvent(event)
