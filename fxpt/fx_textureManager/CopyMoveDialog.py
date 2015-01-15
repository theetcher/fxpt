from PySide import QtCore, QtGui

from fxpt.fx_prefsaver import PrefSaver, Serializers
from fxpt.fx_textureManager.CopyMoveDialogUI import Ui_Dialog

from fxpt.fx_textureManager.CopyMoveInfo import CopyMoveInfo

OPT_VAR_NAME_COPY_MOVE_DLG = 'fx_textureManager_copMoveDlg_prefs'


class CopyMoveDialog(QtGui.QDialog):

    def __init__(self, parent):
        super(CopyMoveDialog, self).__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.lastBrowsedDirTarget = ''
        self.lastBrowsedDirSource = ''

        self.ui_initSettings()
        self.ui_loadSettings()

        self.validateUi()

    # noinspection PyAttributeOutsideInit
    def ui_initSettings(self):
        self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerOptVar(OPT_VAR_NAME_COPY_MOVE_DLG))

        self.prefSaver.addControl(self, PrefSaver.UIType.PYSIDEWindow, (200, 200, 800, 350))
        # self.prefSaver.addControl(self.ui.uiLED_retargetRoot, PrefSaver.UIType.PYSIDELineEdit, '')
        # self.prefSaver.addControl(self.ui.uiCHK_forceRetarget, PrefSaver.UIType.PYSIDECheckBox, False)

        # self.prefSaver.addVariable('retargetDlg_lastBrowsedDirTarget', self.getLastBrowsedDir, self.setLastBrowsedDir, '')

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    # def setLastBrowsedDir(self, path):
    #     self.lastBrowsedDir = path
    #
    # def getLastBrowsedDir(self):
    #     return self.lastBrowsedDir

    def getTargetRoot(self):
        return self.ui.uiLED_targetRoot.getPath()

    # def setTargetRoot(self, path):
    #     self.ui.uiLED_retargetRoot.setPath(path)

    def getDelSrc(self):
        return self.ui.uiCHK_deleteSources.checkState() == QtCore.Qt.Checked

    def getCopyFolderStruct(self):
        return self.ui.uiGRP_folderStructure.isChecked()

    def getSourceRoot(self):
        return self.ui.uiLED_sourceRoot.getPath()

    def getCopyAdd(self):
        return self.ui.uiGRP_addTextures.isChecked()

    def getAddSuffixes(self):
        return str(self.ui.uiLED_texSuffixes.text())

    def getRetarget(self):
        return self.ui.uiCHK_retarget.checkState() == QtCore.Qt.Checked

    def getForceRetarget(self):
        return self.ui.uiCHK_forceRetarget.checkState() == QtCore.Qt.Checked

    # def getForceRetarget(self):
    #     return self.ui.uiCHK_forceRetarget.checkState() == QtCore.Qt.Checked

    def validateUi(self):
        return True
        # retargetRootExists = self.ui.uiLED_retargetRoot.pathExists()
        # self.ui.uiBTN_ok.setEnabled(retargetRootExists)
        # if retargetRootExists:
        #     self.setStatusText('')
        # else:
        #     self.setStatusText('Retarget root directory does not exists.')

    def setStatusText(self, text):
        self.ui.uiLBL_status.setText(text)

    def getDialogResult(self):
        res = CopyMoveInfo(
            targetRoot=self.getTargetRoot(),
            delSrc=self.getDelSrc(),
            copyFolderStruct=self.getCopyFolderStruct(),
            sourceRoot=self.getSourceRoot(),
            copyAdd=self.getCopyAdd(),
            addSuffixes=self.getAddSuffixes(),
            retarget=self.getRetarget(),
            forceRetarget=self.getForceRetarget()
        )
        return res

    def onBrowseClicked(self):
        # noinspection PyCallByClass
        dialogResult = QtGui.QFileDialog.getExistingDirectory(
            self,
            'Retarget Root',
            self.getLastBrowsedDir()
        )
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