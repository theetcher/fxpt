from PySide import QtGui

from fxpt.fx_textureManager.MainWindowUI import Ui_MainWindow


class TexManagerUI(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(TexManagerUI, self).__init__(parent=parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
