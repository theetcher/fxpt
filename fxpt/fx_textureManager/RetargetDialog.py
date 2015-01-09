import os
from PySide import QtGui

from fxpt.fx_prefsaver import PrefSaver, Serializers

from fxpt.fx_textureManager.RetargetDialogUI import Ui_Dialog
from fxpt.fx_textureManager.com import cleanupPath


OPT_VAR_NAME_RETARGET_DLG = 'fx_textureManager_retargetDlg_prefs'

#TODO: make LineEditPath and put all cleanup and .exists in it


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
        return str(self.ui.uiLED_retargetRoot.text())

    def setRetargetRoot(self, path):
        self.ui.uiLED_retargetRoot.setText(path)

    def validateUi(self):
        retargetRootExists = os.path.exists(self.getRetargetRoot())
        self.ui.uiBTN_ok.setEnabled(retargetRootExists)
        if not retargetRootExists:
            self.setStatusText('Retarget root does not exists.')
        else:
            self.setStatusText('')

    def setStatusText(self, text):
        self.ui.uiLBL_status.setText(text)

    def onBrowseClicked(self):
        # noinspection PyCallByClass
        dialogResult = QtGui.QFileDialog.getExistingDirectory(
            self,
            'Retarget Root',
            self.getLastBrowsedDir()
        )
        cleanPath = cleanupPath(dialogResult)
        self.setLastBrowsedDir(cleanPath)
        self.setRetargetRoot(cleanPath)
        self.validateUi()

    def onRetargetRootEditingFinished(self):
        self.setRetargetRoot(cleanupPath(self.getRetargetRoot()))
        self.validateUi()

    # noinspection PyUnusedLocal
    def onDialogFinished(self, status):
        self.ui_saveSettings()