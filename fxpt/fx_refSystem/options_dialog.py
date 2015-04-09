from PySide import QtCore, QtGui

from fxpt.fx_utils.utils import cleanupPath
from fxpt.fx_prefsaver import PrefSaver, Serializers
from fxpt.fx_refSystem.options_dialog_ui import Ui_Dialog
from fxpt.fx_refSystem.roots_cfg_handler import RootsCfgHandler

OPT_VAR_NAME = 'fx_refSystem_optionsDlg_prefs'
NO_ROOT_STRING = '... use absolute paths ...'
ACTIVE_ROOT_COLOR = QtGui.QColor(255, 174, 0)
ACTIVE_ROOT_SUFFIX = ' [active]'


# TODO: sorting in dialog

class OptionsDialog(QtGui.QDialog):

    def __init__(self, parent):
        super(OptionsDialog, self).__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.lastBrowsedDir = None

        self.rootsCfgHandler = RootsCfgHandler()
        self.roots = self.rootsCfgHandler.getRoots()
        self.checkForOneActiveRoot()

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
        self.ui.uiLST_roots.clear()
        for root, isActive in self.roots.items():
            rootDisplayText = root if root else NO_ROOT_STRING
            item = QtGui.QListWidgetItem()
            item.root = root
            if isActive:
                font = QtGui.QFont()
                font.setBold(True)
                item.setFont(font)
                item.setForeground(ACTIVE_ROOT_COLOR)
                item.setText(rootDisplayText + ACTIVE_ROOT_SUFFIX)
                item.active = True
            else:
                item.setText(rootDisplayText)
                item.active = False

            self.ui.uiLST_roots.addItem(item)

    def getSelectedItem(self):
        items = self.ui.uiLST_roots.selectedItems()
        if items:
            return items[0]

    def onAddClicked(self):
        # noinspection PyCallByClass
        newRootDir = QtGui.QFileDialog.getExistingDirectory(
            self,
            'References Root Dir',
            self.getLastBrowsedDir()
        )
        if not newRootDir:
            return

        self.roots[cleanupPath(newRootDir)] = False
        self.fillRootsList()

    def onSetActiveClicked(self):
        selectedItem = self.getSelectedItem()
        if selectedItem:
            assert selectedItem.root in self.roots, 'selected item root not in db.'
            self.setActive(selectedItem.root)
            self.fillRootsList()

    def setActive(self, activeRoot):
        for root in self.roots:
            if root == activeRoot:
                self.roots[root] = True
            else:
                self.roots[root] = False

    def onDialogFinished(self):
        self.ui_saveSettings()

    def onDialogAccepted(self):
        self.checkForOneActiveRoot()
        self.rootsCfgHandler.setterRoots(self.roots)
        self.rootsCfgHandler.saveCfg()

    def checkForOneActiveRoot(self):
        assert len([v for v in self.roots.values() if v]) == 1, 'number of active roots is not equal to 1'


def run():
    dlg = OptionsDialog(None)
    dlg.show()