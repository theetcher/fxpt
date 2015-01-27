import os
import maya.cmds as m
from PySide import QtCore, QtGui

from fxpt.side_utils import pyperclip

from fxpt.fx_textureManager import com

from fxpt.fx_textureManager.MainWindowUI import Ui_MainWindow
from fxpt.fx_textureManager.Harvesters import MayaSceneHarvester
from fxpt.fx_textureManager.Coordinators import CoordinatorMayaUI
from fxpt.fx_textureManager.Delegates import TexNodeDelegate
from fxpt.fx_prefsaver import PrefSaver, Serializers

from fxpt.fx_textureManager.SearchReplaceDialog import SearchReplaceDialog
from fxpt.fx_textureManager.RetargetDialog import RetargetDialog
from fxpt.fx_textureManager.CopyMoveDialog import CopyMoveDialog
from fxpt.fx_textureManager.LogDialog import LogDialog

#TODO!: need to remember table scrolling when doing actions. critical for editing in table cause after editing finished PasteProcessor will be ran and table will be rebuild
#TODO!: in table editing: PasteProcessor vs model editing
#TODO!: test on huge data
#TODO!: test processor usage without maya and pyside
#TODO: change icon of search and replace
#TODO: app icon
#TODO: edit filename in table. get new filename from edit cell and then apply ProcPaste


class TexManagerUI(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(TexManagerUI, self).__init__(parent=parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.coordinator = CoordinatorMayaUI()
        self.clipboard = None

        uiAGR_selectionBehaviour = QtGui.QActionGroup(self)
        self.ui.uiACT_selectNothing.setActionGroup(uiAGR_selectionBehaviour)
        self.ui.uiACT_selectTextureNode.setActionGroup(uiAGR_selectionBehaviour)
        self.ui.uiACT_selectAssigned.setActionGroup(uiAGR_selectionBehaviour)

        self.searchReplaceDlg = SearchReplaceDialog(self)
        self.retargetDlg = RetargetDialog(self)
        self.copyMoveDlg = CopyMoveDialog(self)
        self.logDlg = LogDialog(self)

        self.createContextMenu()

        self.ui_initSettings()

        self.setUpdatesAllowed(False)
        self.ui_loadSettings(self.ui.uiACT_collapseRepetitions)
        self.setUpdatesAllowed(True)

        self.harvester = MayaSceneHarvester()

        self.initModels()
        self.fillTable()

        self.ui_loadSettings()

        self.connect(
            self.ui.uiTBL_textures.selectionModel(),
            QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'),
            self.onTableSelectionChanged
        )

        self.displayStatusBarInfo()
        self.updateUiStates()

    # noinspection PyAttributeOutsideInit
    def ui_initSettings(self):
        self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerOptVar(com.OPT_VAR_NAME))

        self.prefSaver.addControl(self, PrefSaver.UIType.PYSIDEWindow, (100, 100, 900, 600))
        self.prefSaver.addControl(self.ui.uiTBL_textures, PrefSaver.UIType.PYSIDETableView)
        self.prefSaver.addControl(self.ui.uiLED_filter, PrefSaver.UIType.PYSIDELineEdit, '')
        self.prefSaver.addControl(self.ui.uiACT_collapseRepetitions, PrefSaver.UIType.PYSIDECheckAction, False)

        self.prefSaver.addControl(self.ui.uiACT_selectNothing, PrefSaver.UIType.PYSIDECheckAction, True)
        self.prefSaver.addControl(self.ui.uiACT_selectTextureNode, PrefSaver.UIType.PYSIDECheckAction, False)
        self.prefSaver.addControl(self.ui.uiACT_selectAssigned, PrefSaver.UIType.PYSIDECheckAction, False)

    def ui_loadSettings(self, control=None):
        self.prefSaver.loadPrefs(control=control)

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    def ui_resetSettings(self):
        self.prefSaver.resetPrefs()

    # noinspection PyAttributeOutsideInit
    def setUpdatesAllowed(self, state):
        self.updatesAllowed = state

    def getUpdatesAllowed(self):
        return self.updatesAllowed

    def createContextMenu(self):
        self.ui.uiTBL_textures.addAction(self.ui.uiACT_copy)
        self.ui.uiTBL_textures.addAction(self.ui.uiACT_paste)

        separator = QtGui.QAction(self)
        separator.setSeparator(True)
        self.ui.uiTBL_textures.addAction(separator)

        self.ui.uiTBL_textures.addAction(self.ui.uiACT_copyFullPath)
        self.ui.uiTBL_textures.addAction(self.ui.uiACT_copyFilename)

        separator = QtGui.QAction(self)
        separator.setSeparator(True)
        self.ui.uiTBL_textures.addAction(separator)

        self.ui.uiTBL_textures.addAction(self.ui.uiACT_selectAll)
        self.ui.uiTBL_textures.addAction(self.ui.uiACT_selectInvert)
        self.ui.uiTBL_textures.addAction(self.ui.uiACT_selectNone)

        separator = QtGui.QAction(self)
        separator.setSeparator(True)
        self.ui.uiTBL_textures.addAction(separator)

        self.ui.uiTBL_textures.addAction(self.ui.uiACT_refresh)

    # noinspection PyAttributeOutsideInit
    def initModels(self):
        self.model = QtGui.QStandardItemModel()
        self.filterModel = QtGui.QSortFilterProxyModel()
        self.filterModel.setSourceModel(self.model)
        self.ui.uiTBL_textures.setModel(self.filterModel)
        self.filterModel.setFilterKeyColumn(1)

    def setFilterWildcard(self, wildcard):
        self.filterModel.setFilterRegExp(QtCore.QRegExp(wildcard, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.Wildcard))

    # noinspection PyMethodMayBeStatic
    def prepareData(self, texNodes):
        if not texNodes:
            return []

        res = []
        existsCache = {}
        for tn in texNodes:
            filename = tn.getAttrValue()
            if filename not in existsCache:
                existsCache[filename] = tn.fileExists()
            res.append((existsCache[filename], filename, tn.getFullAttrName(), [tn]))
        return res

    # noinspection PyMethodMayBeStatic
    def prepareDataCollapsed(self, texNodes):
        if not texNodes:
            return []

        d = {}
        for tn in texNodes:
            filename = tn.getAttrValue()
            if filename not in d:
                d[filename] = [tn]
            else:
                d[filename].append(tn)

        res = []
        existsCache = {}
        for filename, tns in d.iteritems():
            if filename not in existsCache:
                existsCache[filename] = tns[0].fileExists()

            fullAttrName = tns[0].getFullAttrName() if len(tns) == 1 else com.MULTIPLE_STRING
            res.append((existsCache[filename], filename, fullAttrName, tns))

        return res

    def fillTable(self):
        self.model.clear()
        self.model.setRowCount(0)
        self.model.setColumnCount(len(com.TABLE_COLUMN_NAMES))
        for i, col in enumerate(com.TABLE_COLUMN_NAMES):
            self.model.setHeaderData(i, QtCore.Qt.Horizontal, col, QtCore.Qt.DisplayRole)

        if self.getCollapseRepetitionsOption():
            data = self.prepareDataCollapsed(self.harvester.getTexNodes())
        else:
            data = self.prepareData(self.harvester.getTexNodes())

        self.model.insertRows(0, len(data))

        for i, dataItem in enumerate(data):

            exists, filename, attr, tns = dataItem

            modelIndex = self.model.index(i, com.COL_IDX_EXIST)
            self.model.setData(modelIndex, com.FILE_EXISTS_STRINGS[exists][0])
            self.model.setData(modelIndex, com.FILE_EXISTS_STRINGS[exists][1], QtCore.Qt.ForegroundRole)
            self.model.setData(modelIndex, tns, QtCore.Qt.UserRole)

            modelIndex = self.model.index(i, com.COL_IDX_FILENAME)
            self.model.setData(modelIndex, filename)
            self.model.setData(modelIndex, tns, QtCore.Qt.UserRole)

            modelIndex = self.model.index(i, com.COL_IDX_ATTR)
            self.model.setData(modelIndex, attr)
            self.model.setData(modelIndex, tns, QtCore.Qt.UserRole)

        self.setTableProps()
        self.setTableDelegates()

    def setTableDelegates(self):
        roDelegate = TexNodeDelegate(self)
        # noinspection PyUnresolvedReferences
        roDelegate.closeEditor.connect(self.onDelegateCloseEditor)
        self.ui.uiTBL_textures.setItemDelegate(roDelegate)

    @QtCore.Slot()
    def onDelegateCloseEditor(self):
        self.uiRefresh()

    def setTableProps(self):
        table = self.ui.uiTBL_textures
        table.setFont(com.FONT_MONOSPACE_QFONT)
        table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        # custom "resize to fit" section, cause standard table.resizeColumnsToContents() may be very slow on huge data
        model = self.model
        columnCount = model.columnCount()
        for col in range(columnCount):
            stringLengths = [len(model.index(row, col).data(QtCore.Qt.DisplayRole)) for row in range(model.rowCount())]
            stringLengths.append(len(str(model.headerData(col, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))) + com.TABLE_HEADER_TITLE_OFFSET)
            columnMaxLength = min(max(stringLengths), com.TABLE_MAX_COLUMN_SIZE[col])
            table.horizontalHeader().resizeSection(col, columnMaxLength * com.FONT_MONOSPACE_LETTER_SIZE + com.TABLE_COLUMN_RIGHT_OFFSET)

    def getCollapseRepetitionsOption(self):
        return self.ui.uiACT_collapseRepetitions.isChecked()

    def getSelectedTexNodes(self):
        tns = []
        for index in self.getSelectedIndexes(com.COL_IDX_ATTR):
            tns.extend(index.data(role=QtCore.Qt.UserRole))
        return sorted(tns)

    def getSelectedFullPaths(self):
        selectedIndexes = self.getSelectedIndexes(com.COL_IDX_FILENAME)
        return sorted([str(index.data()) for index in selectedIndexes])

    def getSelectedFilenames(self):
        return sorted([os.path.basename(fp) for fp in self.getSelectedFullPaths()])

    def getSelectTextureNodeOption(self):
        return self.ui.uiACT_selectTextureNode.isChecked()

    def getSelectAssignedOption(self):
        return self.ui.uiACT_selectAssigned.isChecked()

    # noinspection PyUnusedLocal
    def onTableSelectionChanged(self, *args):
        if self.getSelectAssignedOption():
            self.selectAssigned()
        elif self.getSelectTextureNodeOption():
            self.selectTextureNodes()

        self.updateUiStates()
        self.displayStatusBarInfo()

    def getSelectedIndexes(self, column):
        return self.ui.uiTBL_textures.selectionModel().selectedRows(column)

    def updateUiStates(self):
        somethingSelected = bool(self.getSelectedIndexes(com.COL_IDX_FILENAME))
        onlyOneItemSelected = bool(len(self.getSelectedIndexes(com.COL_IDX_FILENAME)) == 1)
        clipboardIsNotEmpty = self.clipboard is not None

        self.ui.uiACT_copy.setEnabled(onlyOneItemSelected)
        self.ui.uiACT_paste.setEnabled(clipboardIsNotEmpty and somethingSelected)

        self.ui.uiACT_copyFullPath.setEnabled(somethingSelected)
        self.ui.uiACT_copyFilename.setEnabled(somethingSelected)

        self.ui.uiACT_copyMove.setEnabled(somethingSelected)
        self.ui.uiACT_retarget.setEnabled(somethingSelected)
        self.ui.uiACT_searchReplace.setEnabled(somethingSelected)

    def displayStatusBarInfo(self):
        selectedItemsCount = len(self.getSelectedIndexes(com.COL_IDX_FILENAME))
        if selectedItemsCount:
            self.ui.statusbar.showMessage('{} item(s) selected.'.format(selectedItemsCount))
        else:
            self.ui.statusbar.clearMessage()

    def selectTextureNodes(self):
        nodes = [tn.getNode() for tn in self.getSelectedTexNodes()]
        if nodes:
            m.select(nodes, r=True)
        else:
            m.select(cl=True)

    def selectAssigned(self):
        sgToSelect = []
        for node in [tn.getNode() for tn in self.getSelectedTexNodes()]:
            sgToSelect.extend(com.getShadingGroups(node, set()))
        if sgToSelect:
            m.select(sgToSelect)
        else:
            m.select(cl=True)

    def uiRefresh(self):
        sortingInfo = self.getSortingInfo()

        self.fillTable()
        self.onFilterTextChanged()

        self.setSorting(sortingInfo)
        self.updateUiStates()

    def getSortingInfo(self):
        header = self.ui.uiTBL_textures.horizontalHeader()
        return header.sortIndicatorSection(), header.sortIndicatorOrder()

    def setSorting(self, sortingInfo):
        section, order = sortingInfo
        self.ui.uiTBL_textures.sortByColumn(section, order)

    def onFilterTextChanged(self):
        sortingInfo = self.getSortingInfo()

        wildcard = self.ui.uiLED_filter.text()
        self.setFilterWildcard(wildcard)
        state = bool(wildcard)
        self.ui.uiBTN_filter.setEnabled(state)
        self.ui.uiBTN_filter.setChecked(state)

        self.setSorting(sortingInfo)

    def onFilterButtonToggled(self, state):
        if not state:
            self.ui.uiLED_filter.clear()

    def onRefreshTriggered(self):
        self.uiRefresh()

    def onCopyFullPathTriggered(self):
        paths = filter(bool, self.getSelectedFullPaths())
        self.putCopyListToClipboard(paths)

    def onCopyFilenameTriggered(self):
        filenames = filter(bool, self.getSelectedFilenames())
        self.putCopyListToClipboard(filenames)

    # noinspection PyMethodMayBeStatic
    def putCopyListToClipboard(self, l):
        pyperclip.setcb('\n'.join(l))

    def onSelectAllTriggered(self):
        self.ui.uiTBL_textures.selectAll()

    def onSelectInvertTriggered(self):
        model = self.ui.uiTBL_textures.model()
        selectionModel = self.ui.uiTBL_textures.selectionModel()

        topLeftIndex = model.index(0, 0)
        bottomRightIndex = model.index(model.rowCount() - 1, model.columnCount() - 1)
        itemSelection = QtGui.QItemSelection(topLeftIndex, bottomRightIndex)
        selectionModel.select(itemSelection, QtGui.QItemSelectionModel.Toggle)

    def onSelectNoneTriggered(self):
        self.ui.uiTBL_textures.clearSelection()

    # noinspection PyUnusedLocal
    def onCollapseRepetitionsToggled(self, state):
        if self.getUpdatesAllowed():
            self.uiRefresh()
        # self.ui.uiTBL_textures.clearSelection()

    def onChangeSelectionBehaviour(self, state):
        if state:
            self.onTableSelectionChanged()

    def onCopyTriggered(self):
        self.clipboard = self.getSelectedFullPaths()[0]
        self.updateUiStates()

    def onPasteTriggered(self):
        self.coordinator.processPaste(self.getSelectedTexNodes(), self.clipboard)
        self.uiRefresh()

    def onCopyMoveTriggered(self):
        if self.copyMoveDlg.exec_() == QtGui.QDialog.Accepted:
            dialogResult = self.copyMoveDlg.getDialogResult()
            procLog = self.coordinator.processCopyMove(
                self.getSelectedTexNodes(),
                dialogResult
            )
            self.logDlg.showLog(procLog)
            self.uiRefresh()

    def onRetargetTriggered(self):
        if self.retargetDlg.exec_() == QtGui.QDialog.Accepted:
            retargetRoot, forceRetarget, useSourceRoot, sourceRoot = self.retargetDlg.getDialogResult()
            procLog = self.coordinator.processRetarget(
                self.getSelectedTexNodes(),
                retargetRoot,
                forceRetarget,
                useSourceRoot,
                sourceRoot
            )
            self.logDlg.showLog(procLog)
            self.uiRefresh()

    def onSearchReplaceTriggered(self):
        if self.searchReplaceDlg.exec_() == QtGui.QDialog.Accepted:
            searchStr, replaceStr, caseSensitive = self.searchReplaceDlg.getDialogData()
            procLog = self.coordinator.processSearchAndReplace(
                self.getSelectedTexNodes(),
                searchStr,
                replaceStr,
                caseSensitive
            )
            self.logDlg.showLog(procLog)
            self.uiRefresh()

    def closeEvent(self, event):
        self.ui_saveSettings()
        event.accept()
