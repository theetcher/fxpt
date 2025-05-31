from fxpt3.qt.pyside import QtCore, QtWidgets
from fxpt3.fx_texture_manager.line_edit_path import LineEditPath
from fxpt3.fx_texture_manager.com import FONT_MONOSPACE_QFONT


class TexNodeDelegate(QtWidgets.QItemDelegate):

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

