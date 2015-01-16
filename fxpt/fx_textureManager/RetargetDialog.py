from PySide import QtCore, QtGui

from fxpt.fx_prefsaver import PrefSaver, Serializers
from fxpt.fx_textureManager.RetargetDialogUI import Ui_Dialog


OPT_VAR_NAME_RETARGET_DLG = 'fx_textureManager_retargetDlg_prefs'


class RetargetDialog(QtGui.QDialog):

    def __init__(self, parent):
        super(RetargetDialog, self).__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.lastBrowsedDir = ''

        self.ui_initSettings()
        self.ui_loadSettings()

        self.validateUi()

    # noinspection PyAttributeOutsideInit
    def ui_initSettings(self):
        self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerOptVar(OPT_VAR_NAME_RETARGET_DLG))

        self.prefSaver.addControl(self, PrefSaver.UIType.PYSIDEWindow, (200, 200, 600, 100))
        self.prefSaver.addControl(self.ui.uiLED_retargetRoot, PrefSaver.UIType.PYSIDELineEdit, '')
        self.prefSaver.addControl(self.ui.uiCHK_forceRetarget, PrefSaver.UIType.PYSIDECheckBox, False)

        self.prefSaver.addVariable('retargetDlg_lastBrowsedDir', self.getLastBrowsedDir, self.setLastBrowsedDir, '')

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    def setLastBrowsedDir(self, path):
        self.lastBrowsedDir = path

    def getLastBrowsedDir(self):
        return self.lastBrowsedDir

    def getRetargetRoot(self):
        return self.ui.uiLED_retargetRoot.getPath()

    def setRetargetRoot(self, path):
        self.ui.uiLED_retargetRoot.setPath(path)

    def getForceRetarget(self):
        return self.ui.uiCHK_forceRetarget.checkState() == QtCore.Qt.Checked

    def validateUi(self):
        retargetRootExists = self.ui.uiLED_retargetRoot.pathExists()
        self.ui.uiBTN_ok.setEnabled(retargetRootExists)
        if retargetRootExists:
            self.setStatusText('')
        else:
            self.setStatusText('Retarget root directory does not exists.')

    def setStatusText(self, text):
        self.ui.uiLBL_status.setText(text)

    def getDialogResult(self):
        return self.getRetargetRoot(), self.getForceRetarget()

    def onBrowseClicked(self):
        # noinspection PyCallByClass
        dialogResult = QtGui.QFileDialog.getExistingDirectory(
            self,
            'Retarget Root',
            self.getLastBrowsedDir()
        )
        if dialogResult:
            self.setRetargetRoot(dialogResult)
            self.ui.uiLED_retargetRoot.onEditingFinished()
            self.setLastBrowsedDir(self.getRetargetRoot())
            self.validateUi()

    def onRetargetRootEditingFinished(self):
        self.validateUi()

    def onOkClicked(self):
        self.validateUi()
        if self.ui.uiBTN_ok.isEnabled():
            self.accept()

    # noinspection PyUnusedLocal
    def onDialogFinished(self, status):
        self.ui_saveSettings()