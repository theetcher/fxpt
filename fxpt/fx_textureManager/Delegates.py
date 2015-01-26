from PySide import QtGui
from fxpt.fx_textureManager.LineEditPath import LineEditPath

from com import FONT_MONOSPACE_QFONT


class TexNodeDelegate(QtGui.QItemDelegate):

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
