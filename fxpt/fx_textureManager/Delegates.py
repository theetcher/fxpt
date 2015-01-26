from PySide import QtCore, QtGui
from fxpt.fx_textureManager.LineEditPath import LineEditPath

from com import FONT_MONOSPACE_QFONT


class TexNodeDelegate(QtGui.QItemDelegate):

    cellChanged = QtCore.Signal()

    def __init__(self, mainWin, *args, **kwargs):
        self.mainWin = mainWin
        super(TexNodeDelegate, self).__init__(*args, **kwargs)

    def createEditor(self, parent, option, index):
        if index.column() == 1:
            editor = LineEditPath(parent)
            editor.setFont(FONT_MONOSPACE_QFONT)
            return editor
        else:
            return None

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def setModelData(self, editor, model, index):
        super(TexNodeDelegate, self).setModelData(editor, model, index)
        path = editor.getPath()
        tns = model.data(index, QtCore.Qt.UserRole)
        self.mainWin.coordinator.processPaste(tns, path)
        self.cellChanged.emit()
        # self.mainWin.uiRefresh()

