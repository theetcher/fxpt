from fxpt.qt.pyside import QtCore, QtWidgets


class ResultsListWidget(QtWidgets.QListWidget):
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
        rCount = self.count()
        cRow = self.currentRow()
        lastIndex = rCount - 1

        if event.key() == QtCore.Qt.Key_Up:
            if rCount:
                if cRow == 0:
                    self.setCurrentRow(lastIndex)
                else:
                    parentClass.keyPressEvent(event)
        elif event.key() == QtCore.Qt.Key_Down:
            if rCount:
                if cRow == lastIndex:
                    self.setCurrentRow(0)
                else:
                    parentClass.keyPressEvent(event)
        else:
            parentClass.keyPressEvent(event)
