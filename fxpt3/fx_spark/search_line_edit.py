from fxpt3.qt.pyside import QtCore, QtWidgets


class SearchLineEdit(QtWidgets.QLineEdit):
    """
    :type searchResultsList: QtGui.QListWidget
    """
    def __init__(self):
        super(SearchLineEdit, self).__init__()
        self.searchResultsList = None

    def setPartner(self, widget):
        self.searchResultsList = widget

    # noinspection PyMethodOverriding
    def keyPressEvent(self, event):
        """
        :type event: QtGui.QKeyEvent
        """
        rList = self.searchResultsList
        rCount = rList.count()
        cRow = rList.currentRow()
        lastIndex = rCount - 1
        if event.key() == QtCore.Qt.Key.Key_Up:
            if rCount:
                if cRow == 0:
                    rList.setCurrentRow(lastIndex)
                else:
                    rList.setCurrentRow(cRow - 1)
        elif event.key() == QtCore.Qt.Key.Key_Down:
            if rCount:
                if cRow == lastIndex:
                    rList.setCurrentRow(0)
                else:
                    rList.setCurrentRow(cRow + 1)
        elif event.key() in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):
            item = rList.currentItem()
            if item is not None:
                rList.itemActivated.emit(item)
        else:
            super(SearchLineEdit, self).keyPressEvent(event)
