import os
import maya.cmds as m
from maya.mel import eval as meval

from fxpt3.qt.pyside import QtCore, QtGui, QtWidgets
from fxpt3.side_utils import pyperclip
from fxpt3.fx_texture_manager import com

try:
    from fxpt3.fx_texture_manager.main_window_ui6 import Ui_MainWindow
except ImportError:
    from fxpt3.fx_texture_manager.main_window_ui2 import Ui_MainWindow

from fxpt3.fx_texture_manager.harvesters import MayaSceneHarvester, MayaSelectionHarvester
from fxpt3.fx_texture_manager.coordinators import CoordinatorMayaUI
from fxpt3.fx_texture_manager.delegates import TexNodeDelegate
from fxpt3.fx_prefsaver import prefsaver, serializers

from fxpt3.fx_texture_manager.search_replace_dialog import SearchReplaceDialog
from fxpt3.fx_texture_manager.retarget_dialog import RetargetDialog
from fxpt3.fx_texture_manager.copy_move_dialog import CopyMoveDialog
from fxpt3.fx_texture_manager.log_dialog import LogDialog


class TexManagerUI(QtWidgets.QMainWindow):

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

        self.setTableDelegates()
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
        self.prefSaver = prefsaver.PrefSaver(serializers.SerializerOptVar(com.OPT_VAR_NAME))

        self.prefSaver.addControl(self, prefsaver.UIType.PYSIDEWindow, (100, 100, 900, 600))
        self.prefSaver.addControl(self.ui.uiTBL_textures, prefsaver.UIType.PYSIDETableView)
        self.prefSaver.addControl(self.ui.uiLED_filter, prefsaver.UIType.PYSIDELineEdit, '')
        self.prefSaver.addControl(self.ui.uiACT_collapseRepetitions, prefsaver.UIType.PYSIDECheckAction, False)

        self.prefSaver.addControl(self.ui.uiACT_selectNothing, prefsaver.UIType.PYSIDECheckAction, True)
        self.prefSaver.addControl(self.ui.uiACT_selectTextureNode, prefsaver.UIType.PYSIDECheckAction, False)
        self.prefSaver.addControl(self.ui.uiACT_selectAssigned, prefsaver.UIType.PYSIDECheckAction, False)

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

    def setFilterWildcard(self, wildcard):
        # noinspection PyArgumentList
        # self.filterModel.setFilterRegExp(QtCore.QRegExp(wildcard, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.Wildcard))
        self.filterModel.setFilterRegularExpression(QtCore.QRegularExpression(wildcard, QtCore.QRegularExpression.PatternOption.CaseInsensitiveOption))

    # noinspection PyAttributeOutsideInit
    def initModels(self):
        self.model = QtGui.QStandardItemModel()
        self.filterModel = QtCore.QSortFilterProxyModel()
        self.filterModel.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filterModel.setSourceModel(self.model)
        self.ui.uiTBL_textures.setModel(self.filterModel)
        self.filterModel.setFilterKeyColumn(1)

        self.model.setColumnCount(len(com.TABLE_COLUMN_NAMES))
        for i, col in enumerate(com.TABLE_COLUMN_NAMES):
            self.model.setHeaderData(i, QtCore.Qt.Horizontal, col, QtCore.Qt.DisplayRole)

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
            res.append((existsCache[filename], tn.isAssigned(), filename, tn.getFullAttrName(), [tn]))
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
        for filename, tns in d.items():
            if filename not in existsCache:
                existsCache[filename] = tns[0].fileExists()

            fullAttrName = tns[0].getFullAttrName() if len(tns) == 1 else com.MULTIPLE_STRING
            assigned = True if any([tn.isAssigned() for tn in tns]) else False
            res.append((existsCache[filename], assigned, filename, fullAttrName, tns))

        return res

    def fillTable(self):

        if self.getCollapseRepetitionsOption():
            data = self.prepareDataCollapsed(self.harvester.getTexNodes())
        else:
            data = self.prepareData(self.harvester.getTexNodes())

        self.model.setRowCount(len(data))

        for i, dataItem in enumerate(data):

            exists, assigned, filename, attr, tns = dataItem

            modelIndex = self.model.index(i, com.COL_IDX_EXIST)
            self.model.setData(modelIndex, com.FILE_EXISTS_STRINGS[exists][0])
            self.model.setData(modelIndex, com.FILE_EXISTS_STRINGS[exists][1], QtCore.Qt.ForegroundRole)
            self.model.setData(modelIndex, tns, QtCore.Qt.UserRole)

            modelIndex = self.model.index(i, com.COL_IDX_FILENAME)
            self.model.setData(modelIndex, filename)
            self.model.setData(modelIndex, com.ASSIGNED_COLORS[assigned], QtCore.Qt.ForegroundRole)
            self.model.setData(modelIndex, tns, QtCore.Qt.UserRole)

            modelIndex = self.model.index(i, com.COL_IDX_ATTR)
            self.model.setData(modelIndex, attr)
            self.model.setData(modelIndex, com.ASSIGNED_COLORS[assigned], QtCore.Qt.ForegroundRole)
            self.model.setData(modelIndex, tns, QtCore.Qt.UserRole)

        self.setTableProps()

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
        nodes = [tn.getNode() for tn in self.getSelectedTexNodes() if m.objExists(tn.getNode())]
        if nodes:
            m.select(nodes, r=True)
        else:
            m.select(cl=True)

    def selectAssigned(self):
        sgToSelect = set()
        for tn in self.getSelectedTexNodes():
            sgToSelect.update(tn.getSgs())
        if sgToSelect:
            selectionList = [sg for sg in sgToSelect if m.objExists(sg)]
            if selectionList:
                m.select(list(selectionList))
            else:
                m.select(cl=True)

    def uiRefresh(self):
        sortingInfo = self.getSortingInfo()

        self.fillTable()
        self.onFilterTextChanged()

        self.setSorting(sortingInfo)

        selectedIndexes = self.getSelectedIndexes(0)
        if selectedIndexes:
            self.ui.uiTBL_textures.scrollTo(selectedIndexes[0], QtWidgets.QAbstractItemView.EnsureVisible)

        self.updateUiStates()

    def clearSelection(self):
        self.ui.uiTBL_textures.selectionModel().clear()

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
        self.clearSelection()
        self.uiRefresh()

    def onCopyFullPathTriggered(self):
        paths = filter(bool, self.getSelectedFullPaths())
        self.putCopyListToClipboard(paths)

    def onCopyFilenameTriggered(self):
        filenames = filter(bool, self.getSelectedFilenames())
        self.putCopyListToClipboard(filenames)

    # noinspection PyMethodMayBeStatic
    def putCopyListToClipboard(self, l):
        pyperclip.copy('\n'.join(l))

    def onSelectAllTriggered(self):
        self.ui.uiTBL_textures.selectAll()

    def onSelectInvertTriggered(self):
        model = self.ui.uiTBL_textures.model()
        selectionModel = self.ui.uiTBL_textures.selectionModel()

        topLeftIndex = model.index(0, 0)
        bottomRightIndex = model.index(model.rowCount() - 1, model.columnCount() - 1)
        # noinspection PyArgumentList
        itemSelection = QtCore.QItemSelection(topLeftIndex, bottomRightIndex)
        selectionModel.select(itemSelection, QtCore.QItemSelectionModel.Toggle)

    def onSelectNoneTriggered(self):
        self.ui.uiTBL_textures.clearSelection()

    # noinspection PyUnusedLocal
    def onCollapseRepetitionsToggled(self, state):
        if self.getUpdatesAllowed():
            self.clearSelection()
            self.uiRefresh()
        # self.ui.uiTBL_textures.clearSelection()

    def onAnalyzeSelectionToggled(self, state):
        if state:
            self.harvester = MayaSelectionHarvester()
        else:
            self.harvester = MayaSceneHarvester()
        self.uiRefresh()
        self.clearSelection()

    def onChangeSelectionBehaviour(self, state):
        if state:
            self.onTableSelectionChanged()

    def onCopyTriggered(self):
        self.clipboard = self.getSelectedFullPaths()[0]
        self.updateUiStates()

    def onDeleteUnusedShadingNodesTriggered(self):
        meval('MLdeleteUnused')
        self.uiRefresh()

    # noinspection PyMethodMayBeStatic
    def checkTnsExists(self, tns):
        log = []
        res = True
        for tn in tns:
            if not tn.nodeAttrExists():
                log.append('Texture node/attribute {0} does not exists.'.format(tn.getFullAttrName()))
                res = False
        if not res:
            log.append('Processing aborted: UI is out if sync with actual scene data. Refresh Texture Manager and try again.')
        return res, log

    def onPasteTriggered(self):
        tns = self.getSelectedTexNodes()
        tnsExists, log = self.checkTnsExists(tns)
        if tnsExists:
            self.coordinator.processPaste(tns, self.clipboard)
            self.uiRefresh()
        else:
            self.logDlg.showLog(log)

    def onCopyMoveTriggered(self):
        tns = self.getSelectedTexNodes()
        tnsExists, log = self.checkTnsExists(tns)
        if tnsExists:
            if self.copyMoveDlg.exec_() == QtWidgets.QDialog.Accepted:
                dialogResult = self.copyMoveDlg.getDialogResult()
                procLog = self.coordinator.processCopyMove(
                    tns,
                    dialogResult
                )
                self.logDlg.showLog(procLog)
                self.uiRefresh()
        else:
            self.logDlg.showLog(log)

    def onRetargetTriggered(self):
        tns = self.getSelectedTexNodes()
        tnsExists, log = self.checkTnsExists(tns)
        if tnsExists:
            if self.retargetDlg.exec_() == QtWidgets.QDialog.Accepted:
                retargetRoot, forceRetarget, useSourceRoot, sourceRoot = self.retargetDlg.getDialogResult()
                procLog = self.coordinator.processRetarget(
                    tns,
                    retargetRoot,
                    forceRetarget,
                    useSourceRoot,
                    sourceRoot
                )
                self.logDlg.showLog(procLog)
                self.uiRefresh()
        else:
            self.logDlg.showLog(log)

    def onSearchReplaceTriggered(self):
        tns = self.getSelectedTexNodes()
        tnsExists, log = self.checkTnsExists(tns)
        if tnsExists:
            if self.searchReplaceDlg.exec_() == QtWidgets.QDialog.Accepted:
                searchStr, replaceStr, caseSensitive = self.searchReplaceDlg.getDialogData()
                procLog = self.coordinator.processSearchAndReplace(
                    tns,
                    searchStr,
                    replaceStr,
                    caseSensitive
                )
                self.logDlg.showLog(procLog)
                self.uiRefresh()
        else:
            self.logDlg.showLog(log)

    def closeEvent(self, event):
        self.ui_saveSettings()
        event.accept()
