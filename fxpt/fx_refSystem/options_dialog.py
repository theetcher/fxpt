from PySide import QtGui

from fxpt.fx_utils.utils import cleanupPath
from fxpt.fx_prefsaver import PrefSaver, Serializers
from fxpt.fx_refSystem.options_dialog_ui import Ui_Dialog
from fxpt.fx_refSystem.roots_cfg_handler import RootsCfgHandler
from fxpt.fx_refSystem.com import getMayaQMainWindow

OPT_VAR_NAME = 'fx_refSystem_optionsDlg_prefs'
NO_ROOT_STRING = '... use absolute paths ...'
ACTIVE_ROOT_COLOR = QtGui.QColor(255, 174, 0)
ACTIVE_ROOT_SUFFIX = ' [active]'


dlg = None


class OptionsDialog(QtGui.QDialog):

    def __init__(self, parent):
        super(OptionsDialog, self).__init__(parent=parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.lastBrowsedDir = None

        self.rootsCfgHandler = RootsCfgHandler()
        self.roots = self.rootsCfgHandler.getRoots()

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

        self.ui.uiLST_roots.sortItems()
        self.validateUI()

    def getSelectedItem(self):
        items = self.ui.uiLST_roots.selectedItems()
        if items:
            return items[0]

    def onAddClicked(self):
        # noinspection PyCallByClass
        newRootDir = cleanupPath(QtGui.QFileDialog.getExistingDirectory(
            self,
            'References Root Dir',
            self.getLastBrowsedDir()
        ))
        if not newRootDir:
            return

        if newRootDir not in self.roots:
            self.roots[newRootDir] = False
            self.fillRootsList()

    def onRemoveClicked(self):
        rootToRemove = self.getSelectedItem().root
        if self.roots[rootToRemove]:
            self.setActive('')
        del self.roots[rootToRemove]
        self.fillRootsList()

    def onSetActiveClicked(self):
        selectedItem = self.getSelectedItem()
        if selectedItem:
            self.setActive(selectedItem.root)
            self.fillRootsList()

    def setActive(self, activeRoot):
        for root in self.roots:
            if root == activeRoot:
                self.roots[root] = True
            else:
                self.roots[root] = False

    def validateUI(self):
        selectedItem = self.getSelectedItem()
        somethingSelected = selectedItem is not None
        useAbsSelected = somethingSelected and (not selectedItem.root)

        self.ui.uiBTN_remove.setEnabled(somethingSelected and (not useAbsSelected))
        self.ui.uiBTN_setActive.setEnabled(somethingSelected)

    def onSelectionChanged(self):
        self.validateUI()

    def onDialogFinished(self):
        self.ui_saveSettings()

    def onDialogAccepted(self):
        self.rootsCfgHandler.setterRoots(self.roots)
        self.rootsCfgHandler.saveCfg()


def run():
    if not dlg:
        global dlg
        mayaMainWin = getMayaQMainWindow()
        dlg = OptionsDialog(mayaMainWin)
    dlg.show()
    dlg.raise_()


