import os

from fxpt3.qt.pyside import QtCore, QtWidgets
from fxpt3.fx_texture_manager.com import cleanupPath

# TODO: this class is not found by generated ui python files. Manually patched files with "from . import"

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
