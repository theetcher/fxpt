from fxpt3.qt.pyside import QtCore, QtWidgets
from fxpt3.fx_prefsaver import prefsaver, serializers

try:
    from fxpt3.fx_texture_manager.retarget_dialog_ui6 import Ui_Dialog
except ImportError:
    from fxpt3.fx_texture_manager.retarget_dialog_ui2 import Ui_Dialog

OPT_VAR_NAME_RETARGET_DLG = 'fx_textureManager_retargetDlg_prefs'


class RetargetDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super(RetargetDialog, self).__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.lastBrowsedDir = ''
        self.lastBrowsedDirSrc = ''

        self.ui_initSettings()
        self.ui_loadSettings()

        self.validateUi()

    # noinspection PyAttributeOutsideInit
    def ui_initSettings(self):
        self.prefSaver = prefsaver.PrefSaver(serializers.SerializerOptVar(OPT_VAR_NAME_RETARGET_DLG))

        self.prefSaver.addControl(self, prefsaver.UIType.PYSIDEWindow, (200, 200, 600, 100))
        self.prefSaver.addControl(self.ui.uiLED_retargetRoot, prefsaver.UIType.PYSIDELineEdit, '')
        self.prefSaver.addControl(self.ui.uiCHK_forceRetarget, prefsaver.UIType.PYSIDECheckBox, False)
        self.prefSaver.addControl(self.ui.uiGRP_useSourceRoot, prefsaver.UIType.PYSIDEGroupBox, False)
        self.prefSaver.addControl(self.ui.uiLED_sourceRoot, prefsaver.UIType.PYSIDELineEdit, '')

        self.prefSaver.addVariable('retargetDlg_lastBrowsedDir', self.getLastBrowsedDir, self.setLastBrowsedDir, '')
        self.prefSaver.addVariable('retargetDlg_lastBrowsedSrcDir', self.getLastBrowsedSrcDir, self.setLastBrowsedSrcDir, '')

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    def setLastBrowsedDir(self, path):
        self.lastBrowsedDir = path

    def getLastBrowsedDir(self):
        return self.lastBrowsedDir

    def setLastBrowsedSrcDir(self, path):
        self.lastBrowsedDirSrc = path

    def getLastBrowsedSrcDir(self):
        return self.lastBrowsedDirSrc

    def getRetargetRoot(self):
        return self.ui.uiLED_retargetRoot.getPath()

    def setRetargetRoot(self, path):
        self.ui.uiLED_retargetRoot.setPath(path)

    def getSourceRoot(self):
        return self.ui.uiLED_sourceRoot.getPath()

    def setSourceRoot(self, path):
        self.ui.uiLED_sourceRoot.setPath(path)

    def getForceRetarget(self):
        return self.ui.uiCHK_forceRetarget.checkState() == QtCore.Qt.Checked

    def getUseSourceRoot(self):
        return self.ui.uiGRP_useSourceRoot.isChecked()

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
        return self.getRetargetRoot(), self.getForceRetarget(), self.getUseSourceRoot(), self.getSourceRoot()

    def onBrowseClicked(self):
        # noinspection PyCallByClass
        dialogResult = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            'Retarget Root',
            self.getLastBrowsedDir()
        )
        if dialogResult:
            self.setRetargetRoot(dialogResult)
            self.ui.uiLED_retargetRoot.onEditingFinished()
            self.setLastBrowsedDir(self.getRetargetRoot())
            self.validateUi()

    def onBrowseSourceClicked(self):
        # noinspection PyCallByClass
        dialogResult = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            'Source Root',
            self.getLastBrowsedSrcDir()
        )
        if dialogResult:
            self.setSourceRoot(dialogResult)
            self.ui.uiLED_sourceRoot.onEditingFinished()
            self.setLastBrowsedSrcDir(self.getSourceRoot())
            self.validateUi()

    def onValidateUiNeeded(self):
        self.validateUi()

    def onOkClicked(self):
        self.validateUi()
        if self.ui.uiBTN_ok.isEnabled():
            self.accept()

    # noinspection PyUnusedLocal
    def onDialogFinished(self, status):
        self.ui_saveSettings()
