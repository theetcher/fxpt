#region imports

from fxpt.side_utils import pyperclip

from PySide import QtCore, QtGui
import shiboken

import maya.OpenMayaUI as omui
import pymel.core as pm

from fxpt.fx_prefsaver import PrefSaver, Serializers
import MainWindowUI
import Searchers
from Com import *

#endregion imports

mainWin = None

#TODO: if string in table is too long, popup full string in some widget

OPT_VAR_NAME = 'fx_search_prefs'


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class SearchUI(QtGui.QMainWindow, MainWindowUI.Ui_MainWindow):
    def __init__(self):
        ptr = omui.MQtUtil.mainWindow()
        mainWinQObject = None
        if ptr is not None:
            mainWinQObject = shiboken.wrapInstance(long(ptr), QtGui.QWidget)  # or you can use QMainWindow
        else:
            m.error('cannot find main Maya window.')
        super(SearchUI, self).__init__(mainWinQObject)

        self.setupUi(self)

        self.ctxMenu = None
        self.generateCtxMenu()

        self.currentSearcherLink = None
        self.searchers = []
        self.initSearchersAndControls()

        self.ui_setState(SEARCH_STATE_WELCOME)

        self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerOptVar(OPT_VAR_NAME))
        self.ui_initSettings()
        self.ui_loadSettings()

    # noinspection PyMethodMayBeStatic
    def ui_initSettings(self):
        self.prefSaver.addControl(self, PrefSaver.UIType.PYSIDEWindow, (100, 100, 900, 600))
        self.prefSaver.addControl(self.ui_LED_search, PrefSaver.UIType.PYSIDELineEdit)
        self.prefSaver.addControl(self.ui_BTN_soCaseSensitive, PrefSaver.UIType.PYSIDECheckButton, False)
        self.prefSaver.addControl(self.ui_BTN_soRegex, PrefSaver.UIType.PYSIDECheckButton, False)
        self.prefSaver.addControl(self.ui_BTN_soSelectFound, PrefSaver.UIType.PYSIDECheckButton, False)
        self.prefSaver.addControl(self.ui_BTN_soIncludeShapes, PrefSaver.UIType.PYSIDECheckButton, False)
        self.prefSaver.addControl(self.ui_BTN_soSearchSelected, PrefSaver.UIType.PYSIDECheckButton, False)
        self.prefSaver.addControl(self.ui_ACT_useAllTabs, PrefSaver.UIType.PYSIDECheckAction, False)

        for btn in self.getCatButtons():
            self.prefSaver.addControl(btn, PrefSaver.UIType.PYSIDECheckButton, True)

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    def ui_resetSettings(self):
        self.prefSaver.resetPrefs()

    def initSearchersAndControls(self):
        self.searchers = [
            SearcherLink(Searchers.SearcherNodes('All Nodes'), QtGui.QPushButton('All Nodes'),
                         QtGui.QTableView(), QtGui.QWidget()),
            SearcherLink(Searchers.SearcherDagNodes('DAG Nodes'), QtGui.QPushButton('DAG Nodes'),
                         QtGui.QTableView(), QtGui.QWidget()),
            SearcherLink(Searchers.SearcherTexturedBy('Textured By'), QtGui.QPushButton('Textured By'),
                         QtGui.QTableView(), QtGui.QWidget()),
            SearcherLink(Searchers.SearcherTextures('Textures'), QtGui.QPushButton('Textures'),
                         QtGui.QTableView(), QtGui.QWidget()),
            SearcherLink(Searchers.SearcherTransforms('Transforms'), QtGui.QPushButton('Transforms'),
                         QtGui.QTableView(), QtGui.QWidget()),
            SearcherLink(Searchers.SearcherType('Type'), QtGui.QPushButton('Type'),
                         QtGui.QTableView(), QtGui.QWidget())
        ]

        for sl in self.searchers:
            layout = QtGui.QHBoxLayout()
            sl.tabWidget.setLayout(layout)
            layout.addWidget(sl.table)
            layout.setContentsMargins(4, 4, 4, 4)
            sl.table.setModel(sl.searcher.getModel())
            self.setTableProps(sl.table)

            sl.button.setCheckable(True)
            buttonLabel = sl.button.text()
            sl.button.setObjectName('uiBTN_' + buttonLabel[0].lower() + buttonLabel[1:].replace(' ', ''))
            sl.button.setStyleSheet(CHECKED_BUTTON_STYLE)
            self.ui_LAY_catButtons.addWidget(sl.button)

            sl.table.connect(
                sl.table.selectionModel(),
                QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'),
                self.ui_onTableSelectionChanged
            )

            sl.table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            sl.table.connect(sl.table, QtCore.SIGNAL('customContextMenuRequested(QPoint)'),
                             self.ui_onCtxMenuPopupRequest)

        self.ui_LAY_catButtons.addItem(QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))

        self.resetResultTablesAndTabs()

    def setTableProps(self, table):
        table.setShowGrid(False)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(15)
        table.setSelectionBehavior(QtGui.QTableView.SelectRows)
        table.setSelectionMode(QtGui.QTableView.ExtendedSelection)
        table.setFont(FONT_MONOSPACE_QFONT)
        table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        table.setSortingEnabled(True)
        table.sortByColumn(0, QtCore.Qt.AscendingOrder)
        table.setAlternatingRowColors(True)
        table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)

        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        # custom "resize to fit" section, cause standard table.resizeColumnsToContents() may be very slow on huge data
        model = table.model()
        columnCount = model.columnCount()
        for col in range(columnCount):
            stringLengths = [len(model.index(row, col).data(QtCore.Qt.DisplayRole)) for row in range(model.rowCount())]
            stringLengths.append(len(str(model.headerData(col, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))) + TABLE_HEADER_TITLE_OFFSET)
            columnMaxLength = min(max(stringLengths), TABLE_MAX_COLUMN_SIZE)
            table.horizontalHeader().resizeSection(col, columnMaxLength * FONT_MONOSPACE_LETTER_SIZE + TABLE_COLUMN_RIGHT_OFFSET)

    def generateCtxMenu(self):
        self.ctxMenu = QtGui.QMenu()
        self.ctxMenu.addAction(self.ui_ACT_selectAll)
        self.ctxMenu.addAction(self.ui_ACT_deselectAll)
        self.ctxMenu.addSeparator()
        self.ctxMenu.addAction(self.ui_ACT_copyFullNamesToClipboard)
        self.ctxMenu.addAction(self.ui_ACT_copyShortNamesToClipboard)
        self.ctxMenu.addSeparator()
        self.ctxMenu.addAction(self.ui_ACT_useAllTabs)

    # noinspection PyArgumentList
    def ui_onCtxMenuPopupRequest(self, *arg, **kwarg):
        self.ctxMenu.popup(QtGui.QCursor.pos())

    def ui_onCatOnOffClicked(self):
        checkState = True if self.sender() == self.ui_BTN_catAllOn else False
        for btn in self.getCatButtons():
            btn.setChecked(checkState)

    def getCurrentOrAllTables(self):
        if self.ui_isUseAllTabs():
            tables = self.getTables()
        else:
            currentSearcherLink = self.getCurrentSearcherLink()
            if currentSearcherLink:
                tables = [self.getCurrentSearcherLink().table]
            else:
                return None
        return tables

    def ui_onTableSelectionChanged(self):
        selectionList = []

        getSelectedNodeInfos = self.getSelectedNodeInfos()
        if not getSelectedNodeInfos:
            return

        for ni in getSelectedNodeInfos:
            if ni.selectionString:
                selectionList.extend(ni.selectionString)

        if selectionList:
            m.select(selectionList)
        else:
            m.select(clear=True)

    def ui_onSearchClicked(self):
        self.ui_tryToSaveTabOptVar()
        self.ui_setState(SEARCH_STATE_SEARCHING)
        self.repaint()

        self.resetResultTablesAndTabs()

        searchDesc = self.getSearchDesc()
        self.setActiveSearchers()

        somethingFound = False
        for sl in self.searchers:
            sl.searcher.search(searchDesc)
            if sl.searcher.hasResult():
                somethingFound = True
                self.ui_TAB_results.addTab(sl.tabWidget, sl.searcher.getName())
                self.setTableProps(sl.table)
                sl.attachedToTabWidget = True

        if somethingFound:
            self.ui_setState(SEARCH_STATE_RESULTS)
            if searchDesc.selectFound:
                for table in self.getTables():
                    table.selectAll()
            self.ui_tryShowSavedTab()
        else:
            self.ui_setState(SEARCH_STATE_NOTHING_FOUND)

    def ui_onResultTabChanged(self):
        self.ui_onTableSelectionChanged()

    # noinspection PyTypeChecker
    def ui_onSelectAllClicked(self):
        tables = self.getCurrentOrAllTables()
        if not tables:
            return
        for table in tables:
            table.selectAll()

    # noinspection PyTypeChecker
    def ui_onDeselectAllClicked(self):
        tables = self.getCurrentOrAllTables()
        if not tables:
            return
        for table in tables:
            table.clearSelection()

    # noinspection PyTypeChecker
    def getSelectedNodeInfos(self):
        nodeInfoList = []
        tables = self.getCurrentOrAllTables()
        if not tables:
            return nodeInfoList
        for table in tables:
            selectedIndexes = table.selectionModel().selectedRows()  # column = 0 by default
            for index in selectedIndexes:
                nodeInfo = index.data(role=QtCore.Qt.UserRole)
                nodeInfoList.append(nodeInfo)
        return nodeInfoList

    def ui_onCopyFullNameClicked(self):
        nameList = [ni.fullPathName for ni in self.getSelectedNodeInfos() if ni.fullPathName]
        nameString = ''
        for name in nameList:
            nameString += name + '\r\n'
        pyperclip.setcb(nameString)

    def ui_onCopyShortNameClicked(self):
        nameList = [ni.shortName for ni in self.getSelectedNodeInfos() if ni.shortName]
        nameString = ''
        for name in nameList:
            nameString += name + '\r\n'
        pyperclip.setcb(nameString)

    def resetResultTablesAndTabs(self):
        for sl in self.searchers:
            sl.searcher.reset()
            sl.attachedToTabWidget = False
            self.ui_TAB_results.clear()

    def ui_setState(self, state):
        stack = self.ui_STK_results
        if state == SEARCH_STATE_WELCOME:
            stack.setCurrentWidget(self.ui_STKPG_status)
            self.ui_TXT_status.setText('type something to search\n and press "enter"')
        elif state == SEARCH_STATE_SEARCHING:
            stack.setCurrentWidget(self.ui_STKPG_status)
            self.ui_TXT_status.setText('searching...')
        elif state == SEARCH_STATE_NOTHING_FOUND:
            stack.setCurrentWidget(self.ui_STKPG_status)
            self.ui_TXT_status.setText('nothing found')
        elif state == SEARCH_STATE_RESULTS:
            stack.setCurrentWidget(self.ui_STKPG_results)

    def setActiveSearchers(self):
        for sl in self.searchers:
            sl.searcher.setActive(sl.button.isChecked())

    def getSearchers(self):
        return [sl.searcher for sl in self.searchers]

    def getCatButtons(self):
        return [sl.button for sl in self.searchers]

    def getTables(self):
        return [sl.table for sl in self.searchers]

    def ui_isUseAllTabs(self):
        return self.ui_ACT_useAllTabs.isChecked()

    def getSearchDesc(self):
        sd = Searchers.SearchDesc()
        sd.searchString = str(self.ui_LED_search.text()).strip()
        sd.caseSensitive = self.ui_BTN_soCaseSensitive.isChecked()
        sd.regex = self.ui_BTN_soRegex.isChecked()
        sd.selectFound = self.ui_BTN_soSelectFound.isChecked()
        sd.includeShapes = self.ui_BTN_soIncludeShapes.isChecked()
        sd.searchSelected = self.ui_BTN_soSearchSelected.isChecked()
        return sd

    def ui_tryToSaveTabOptVar(self):
        optVars = pm.env.optionVars
        currentWidget = self.ui_TAB_results.currentWidget()
        currentSL = None
        for sl in self.searchers:
            if currentWidget is sl.tabWidget:
                currentSL = sl
                break
        if currentSL:
            optVars[OPT_VAR_CURRENT_TAB] = currentSL.searcher.getName()

    def ui_tryShowSavedTab(self):
        optVars = pm.env.optionVars
        savedTabName = optVars[OPT_VAR_CURRENT_TAB]
        if not savedTabName:
            return
        for sl in self.searchers:
            if sl.attachedToTabWidget and sl.searcher.getName() == savedTabName:
                self.ui_TAB_results.setCurrentWidget(sl.tabWidget)
                return

    def getCurrentSearcherLink(self):
        currentWidget = self.ui_TAB_results.currentWidget()
        for sl in self.searchers:
            if sl.tabWidget is currentWidget:
                return sl

    def ui_onShowHelpClicked(self):
        return
        # QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://www.site.com/somehelp', QtCore.QUrl.TolerantMode))

    def ui_onCloseClicked(self):
        self.close()

    def closeEvent(self, event):
        self.ui_saveSettings()
        self.ui_tryToSaveTabOptVar()
        global mainWin
        mainWin = None
        event.accept()


class OptionVarLink():

    def __init__(self, ovName, defaultValue, getFromControlFunc, setToControlFunc):
        self.ovName = ovName
        self.defaultValue = defaultValue
        self.getFromControlFunc = getFromControlFunc
        self.setToControlFunc = setToControlFunc

    def init(self):
        optVars = pm.env.optionVars
        if self.ovName not in optVars:
            optVars[self.ovName] = self.defaultValue

    def applyToControl(self):
        optVars = pm.env.optionVars
        self.setToControlFunc(optVars[self.ovName])

    def getFromControl(self):
        optVars = pm.env.optionVars
        optVars[self.ovName] = self.getFromControlFunc()

    def reset(self):
        optVars = pm.env.optionVars
        optVars.pop(self.ovName)
        self.init()
        self.applyToControl()


class SearcherLink():

    def __init__(self, searcher, button, table, tabWidget):
        self.searcher = searcher
        self.button = button
        self.table = table
        self.tabWidget = tabWidget
        self.attachedToTabWidget = False


def run():

#    from pydev import pydevd
#    pydevd.settrace('localhost', port=62882, stdoutToServer=True, stderrToServer=True)

    global mainWin
    if not mainWin:
        mainWin = SearchUI()
    mainWin.show()
    mainWin.raise_()
