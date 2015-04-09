from PySide import QtCore, QtGui

from fxpt.fx_utils.utils import cleanupPath
from fxpt.fx_prefsaver import PrefSaver, Serializers
from fxpt.fx_refSystem.options_dialog_ui import Ui_Dialog
from fxpt.fx_refSystem.roots_cfg_handler import RootsCfgHandler

OPT_VAR_NAME = 'fx_refSystem_optionsDlg_prefs'
NO_ROOT_STRING = '... use absolute paths ...'
ACTIVE_ROOT_COLOR = QtGui.QColor(255, 174, 0)


class OptionsDialog(QtGui.QDialog):

    def __init__(self, parent):
        super(OptionsDialog, self).__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.lastBrowsedDir = None

        self.rootsCfgHandler = RootsCfgHandler()

        self.fillRootsList()

        self.ui_initSettings()
        self.ui_loadSettings()

    # noinspection PyAttributeOutsideInit
    def ui_initSettings(self):
        self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerOptVar(OPT_VAR_NAME))
        self.prefSaver.addControl(self, PrefSaver.UIType.PYSIDEWindow, (200, 200, 600, 300))
        self.prefSaver.addVariable('lastBrowsedDir', self.getLastBrowsedDir, self.setLastBrowsedDir, '')

    def getLastBrowsedDir(self):
        return self.lastBrowsedDir

    def setLastBrowsedDir(self, value):
        self.lastBrowsedDir = value

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    def fillRootsList(self):
        activeIndex = self.rootsCfgHandler.getCurrentRootIndex()
        for i, root in enumerate(self.rootsCfgHandler.getRoots()):
            root = root if root else NO_ROOT_STRING
            item = QtGui.QListWidgetItem(root)
            if i == activeIndex:
                font = QtGui.QFont()
                font.setBold(True)
                item.setFont(font)
                item.setForeground(ACTIVE_ROOT_COLOR)
                item.active = True
            else:
                item.active = False

            self.ui.uiLST_roots.addItem(item)

    def onAddClicked(self):
        # noinspection PyCallByClass
        newRootDir = QtGui.QFileDialog.getExistingDirectory(
            self,
            'References Root Dir',
            self.getLastBrowsedDir()
        )
        if not newRootDir:
            return

        QtGui.QListWidgetItem(cleanupPath(newRootDir), self.ui.uiLST_roots)

    def onDialogFinished(self):
        self.ui_saveSettings()

    def onDialogAccepted(self):
        self.rootsCfgHandler.saveCfg()
        print 'current root: {0}'.format(self.rootsCfgHandler.getCurrentRoot())






def run():
    dlg = OptionsDialog(None)
    dlg.show()