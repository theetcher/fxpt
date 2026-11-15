from fxpt3.qt.pyside import QtCore, QtWidgets, QtGui

from fxpt3.fx_utils.utils import cleanupPath
from fxpt3.fx_prefsaver import prefsaver, serializers
from fxpt3.fx_refsystem.roots_cfg_handler import RootsCfgHandler
from fxpt3.fx_refsystem.com import getMayaQMainWindow

try:
    from fxpt3.fx_refsystem.options_dialog_ui6 import Ui_Dialog
except ImportError:
    from fxpt3.fx_refsystem.options_dialog_ui2 import Ui_Dialog


OPT_VAR_NAME = 'fx_refsystem_optionsDlg_prefs'
NO_ROOT_STRING = '... use absolute paths ...'
# noinspection PyArgumentList
ACTIVE_ROOT_COLOR = QtGui.QColor(255, 174, 0)
ACTIVE_ROOT_SUFFIX = ' [active]'

ROLE_ROOT = QtCore.Qt.ItemDataRole.UserRole


dlg = None


class OptionsDialog(QtWidgets.QDialog):

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
        self.prefSaver = prefsaver.PrefSaver(serializers.SerializerOptVar(OPT_VAR_NAME))
        self.prefSaver.addControl(self, prefsaver.UIType.PYSIDEWindow, (200, 200, 600, 300))
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
            item = QtWidgets.QListWidgetItem()
            item.setData(ROLE_ROOT, root)
            if isActive:
                font = QtGui.QFont()
                font.setBold(True)
                item.setFont(font)
                item.setForeground(QtGui.QBrush(ACTIVE_ROOT_COLOR))
                item.setText(rootDisplayText + ACTIVE_ROOT_SUFFIX)
            else:
                item.setText(rootDisplayText)

            self.ui.uiLST_roots.addItem(item)

        self.ui.uiLST_roots.sortItems()
        self.validateUI()

    def getSelectedRoot(self):
        items = self.ui.uiLST_roots.selectedItems()
        if items:
            return items[0].data(ROLE_ROOT)
        return None

    def onAddClicked(self):
        # noinspection PyCallByClass
        newRootDir = cleanupPath(QtWidgets.QFileDialog.getExistingDirectory(
            self,
            'References Root Dir',
            self.getLastBrowsedDir()
        ))
        if not newRootDir:
            return

        self.setLastBrowsedDir(newRootDir)

        if newRootDir not in self.roots:
            self.roots[newRootDir] = False
            self.fillRootsList()

    def onRemoveClicked(self):
        rootToRemove = self.getSelectedRoot()
        if not rootToRemove:
            return
        if self.roots[rootToRemove]:
            self.setActive('')
        del self.roots[rootToRemove]
        self.fillRootsList()

    def onSetActiveClicked(self):
        selectedRoot = self.getSelectedRoot()
        if selectedRoot is not None:
            self.setActive(selectedRoot)
            self.fillRootsList()

    def setActive(self, activeRoot):
        for root in self.roots:
            if root == activeRoot:
                self.roots[root] = True
            else:
                self.roots[root] = False

    def validateUI(self):
        selectedRoot = self.getSelectedRoot()
        somethingSelected = selectedRoot is not None
        useAbsSelected = somethingSelected and (not selectedRoot)

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
    global dlg
    if not dlg:
        mayaMainWin = getMayaQMainWindow()
        dlg = OptionsDialog(mayaMainWin)
    else:
        # reload, so edits from a cancelled session don't linger
        dlg.roots = dlg.rootsCfgHandler.getRoots()
        dlg.fillRootsList()
    dlg.show()
    dlg.raise_()
