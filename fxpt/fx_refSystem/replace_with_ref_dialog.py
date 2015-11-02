from PySide import QtGui

from fxpt.fx_utils.utils import cleanupPath
from fxpt.fx_prefsaver import prefsaver, serializers
from fxpt.fx_refSystem.replace_with_ref_dialog_ui import Ui_Dialog

OPT_VAR_NAME = 'fx_refSystem_replaceDlg_prefs'


class ReplaceDialog(QtGui.QDialog):

    RESULT_CANCEL = 0
    RESULT_SAVE_REPLACE = 1
    RESULT_REPLACE = 2

    def __init__(self, parent):
        super(ReplaceDialog, self).__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.lastBrowsedDir = None
        self.dialogResult = self.__class__.RESULT_CANCEL

        self.ui_initSettings()
        self.ui_loadSettings()

    # noinspection PyAttributeOutsideInit
    def ui_initSettings(self):
        self.prefSaver = prefsaver.PrefSaver(serializers.SerializerOptVar(OPT_VAR_NAME))
        self.prefSaver.addControl(self, prefsaver.UIType.PYSIDEWindow, (200, 200, 500, 200))
        self.prefSaver.addVariable('lastBrowsedDir', self.getLastBrowsedDir, self.setLastBrowsedDir, '')

    def getLastBrowsedDir(self):
        return self.lastBrowsedDir

    def setLastBrowsedDir(self, value):
        self.lastBrowsedDir = value

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    def setText(self, text):
        self.ui.uiLBL_text.setText(text)

    def getDialogResult(self):
        return self.dialogResult

    def onDialogFinished(self):
        self.ui_saveSettings()

    def onSaveReplaceClicked(self):
        self.dialogResult = self.__class__.RESULT_SAVE_REPLACE
        self.accept()

    def onReplaceClicked(self):
        self.dialogResult = self.__class__.RESULT_REPLACE
        self.accept()

    def onCancelClicked(self):
        self.dialogResult = self.__class__.RESULT_CANCEL
        self.reject()

