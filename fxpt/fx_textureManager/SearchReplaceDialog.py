from PySide import QtGui
from fxpt.fx_textureManager.SearchReplaceDialogUI import Ui_Dialog


class SearchReplaceDialog(QtGui.QDialog):

    def __init__(self, parent):
        super(SearchReplaceDialog, self).__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def getSearchReplaceStrings(self):
        return str(self.ui.uiLED_search.text()), str(self.ui.uiLED_replace.text())