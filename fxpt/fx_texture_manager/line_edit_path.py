import os

from fxpt.qt.pyside import QtCore, QtWidgets

from fxpt.fx_texture_manager.com import cleanupPath


class LineEditPath(QtWidgets.QLineEdit):

    def __init__(self, *args, **kwargs):
        super(LineEditPath, self).__init__(*args, **kwargs)
        self.connect(self, QtCore.SIGNAL("editingFinished()"), self.onEditingFinished)

    def getPath(self):
        return str(self.text())

    def setPath(self, path):
        self.setText(path)

    def pathExists(self):
        return os.path.exists(self.getPath())

    def onEditingFinished(self):
        self.setPath(cleanupPath(self.getPath()))
