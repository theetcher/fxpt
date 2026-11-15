# region imports

import re

import maya.cmds as m
import maya.OpenMayaUI as omui

from fxpt3.side_utils import pyperclip
from fxpt3.qt.pyside import shiboken, QtCore, QtGui, QtWidgets

from fxpt3.fx_prefsaver import prefsaver, serializers
from fxpt3.fx_search import searchers
from fxpt3.fx_search.com import (
    FONT_MONOSPACE_QFONT,
    FONT_MONOSPACE_LETTER_SIZE,
    OPT_VAR_CURRENT_TAB,
    SEARCH_STATE_WELCOME,
    SEARCH_STATE_SEARCHING,
    SEARCH_STATE_NOTHING_FOUND,
    SEARCH_STATE_RESULTS,
    SEARCH_STATE_ERROR,
    TABLE_MAX_COLUMN_SIZE,
    TABLE_COLUMN_RIGHT_OFFSET,
    TABLE_HEADER_TITLE_OFFSET,
)

try:
    from fxpt3.fx_search.main_window_ui6 import Ui_MainWindow
except ImportError:
    from fxpt3.fx_search.main_window_ui2 import Ui_MainWindow

# endregion imports


mainWin = None

# TODO: if string in table is too long, popup full string in some widget

OPT_VAR_NAME = 'fx_search_prefs'


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class SearchUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # noinspection PyArgumentList
        ptr = omui.MQtUtil.mainWindow()
        mainWinQObject = None
        if ptr is not None:
            mainWinQObject = shiboken.wrapInstance(int(ptr), QtWidgets.QWidget)  # or you can use QMainWindow
        else:
            m.error('cannot find main Maya window.')
        super(SearchUI, self).__init__(mainWinQObject)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)

        self.setupUi(self)

        self.ctxMenu = None
        self.generateCtxMenu()

        self.currentSearcherLink = None
        self.searchers = []
        self.initSearchersAndControls()

        self.ui_setState(SEARCH_STATE_WELCOME)

        self.prefSaver = prefsaver.PrefSaver(serializers.SerializerOptVar(OPT_VAR_NAME))
        self.ui_initSettings()
        self.ui_loadSettings()

    # noinspection PyMethodMayBeStatic
    def ui_initSettings(self):
        self.prefSaver.addControl(self, prefsaver.UIType.PYSIDEWindow, (100, 100, 900, 600))
        self.prefSaver.addControl(self.ui_LED_search, prefsaver.UIType.PYSIDELineEdit)
        self.prefSaver.addControl(self.ui_BTN_soCaseSensitive, prefsaver.UIType.PYSIDECheckButton, False)
        self.prefSaver.addControl(self.ui_BTN_soRegex, prefsaver.UIType.PYSIDECheckButton, False)
        self.prefSaver.addControl(self.ui_BTN_soSelectFound, prefsaver.UIType.PYSIDECheckButton, False)
        self.prefSaver.addControl(self.ui_BTN_soIncludeShapes, prefsaver.UIType.PYSIDECheckButton, False)
        self.prefSaver.addControl(self.ui_BTN_soSearchSelected, prefsaver.UIType.PYSIDECheckButton, False)
        self.prefSaver.addControl(self.ui_ACT_useAllTabs, prefsaver.UIType.PYSIDECheckAction, False)

        for btn in self.getCatButtons():
            self.prefSaver.addControl(btn, prefsaver.UIType.PYSIDECheckButton, True)

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    def ui_resetSettings(self):
        self.prefSaver.resetPrefs()

    def initSearchersAndControls(self):
        self.searchers = [
            SearcherLink(searchers.SearcherNodes('All Nodes'), QtWidgets.QPushButton('All Nodes'),
                         QtWidgets.QTableView(), QtWidgets.QWidget()),
            SearcherLink(searchers.SearcherDagNodes('DAG Nodes'), QtWidgets.QPushButton('DAG Nodes'),
                         QtWidgets.QTableView(), QtWidgets.QWidget()),
            SearcherLink(searchers.SearcherFxRefs('FX References'), QtWidgets.QPushButton('FX References'),
                         QtWidgets.QTableView(), QtWidgets.QWidget()),
            SearcherLink(searchers.SearcherTexturedBy('Textured By'), QtWidgets.QPushButton('Textured By'),
                         QtWidgets.QTableView(), QtWidgets.QWidget()),
            SearcherLink(searchers.SearcherTextures('Textures'), QtWidgets.QPushButton('Textures'),
                         QtWidgets.QTableView(), QtWidgets.QWidget()),
            SearcherLink(searchers.SearcherTransforms('Transforms'), QtWidgets.QPushButton('Transforms'),
                         QtWidgets.QTableView(), QtWidgets.QWidget()),
            SearcherLink(searchers.SearcherType('Type'), QtWidgets.QPushButton('Type'),
                         QtWidgets.QTableView(), QtWidgets.QWidget())
        ]

        for sl in self.searchers:
            layout = QtWidgets.QHBoxLayout()
            sl.tabWidget.setLayout(layout)
            layout.addWidget(sl.table)
            layout.setContentsMargins(4, 4, 4, 4)
            sl.table.setModel(sl.searcher.getModel())
            self.setTableProps(sl.table)

            sl.button.setCheckable(True)
            buttonLabel = sl.button.text()
            sl.button.setObjectName('uiBTN_' + buttonLabel[0].lower() + buttonLabel[1:].replace(' ', ''))
            # sl.button.setStyleSheet(CHECKED_BUTTON_STYLE)
            self.ui_LAY_catButtons.addWidget(sl.button)

            sl.table.selectionModel().selectionChanged.connect(self.ui_onTableSelectionChanged)

            sl.table.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
            sl.table.customContextMenuRequested.connect(self.ui_onCtxMenuPopupRequest)

        # noinspection PyArgumentList
        self.ui_LAY_catButtons.addItem(
            QtWidgets.QSpacerItem(
                20,
                40,
                QtWidgets.QSizePolicy.Policy.Minimum,
                QtWidgets.QSizePolicy.Policy.Expanding
            )
        )

        self.resetResultTablesAndTabs()

    def setTableProps(self, table):
        table.setShowGrid(False)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(15)
        table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        table.setFont(FONT_MONOSPACE_QFONT)
        table.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSortingEnabled(True)
        table.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)
        table.setAlternatingRowColors(True)
        table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel)

        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        # custom "resize to fit" section, cause standard table.resizeColumnsToContents() may be very slow on huge data
        displayRole = QtCore.Qt.ItemDataRole.DisplayRole
        model = table.model()
        columnCount = model.columnCount()
        for col in range(columnCount):
            stringLengths = [len(model.index(row, col).data(displayRole) or '') for row in range(model.rowCount())]
            stringLengths.append(len(str(model.headerData(col, QtCore.Qt.Orientation.Horizontal, displayRole))) + TABLE_HEADER_TITLE_OFFSET)
            columnMaxLength = min(max(stringLengths), TABLE_MAX_COLUMN_SIZE)
            table.horizontalHeader().resizeSection(col, columnMaxLength * FONT_MONOSPACE_LETTER_SIZE + TABLE_COLUMN_RIGHT_OFFSET)

    def generateCtxMenu(self):
        self.ctxMenu = QtWidgets.QMenu(self)
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
                tables = [currentSearcherLink.table]
            else:
                return None
        return tables

    def ui_onTableSelectionChanged(self, *args):
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
            try:
                sl.searcher.search(searchDesc)
            except re.error as e:
                self.resetResultTablesAndTabs()
                self.ui_setState(SEARCH_STATE_ERROR, 'invalid regular expression:\n{}'.format(e))
                return
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

    def ui_onResultTabChanged(self, *args):
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
                nodeInfo = index.data(QtCore.Qt.ItemDataRole.UserRole)
                nodeInfoList.append(nodeInfo)
        return nodeInfoList

    def ui_onCopyFullNameClicked(self):
        nameList = [ni.fullPathName for ni in self.getSelectedNodeInfos() if ni.fullPathName]
        nameString = ''
        for name in nameList:
            nameString += name + '\r\n'
        pyperclip.copy(nameString)

    def ui_onCopyShortNameClicked(self):
        nameList = [ni.shortName for ni in self.getSelectedNodeInfos() if ni.shortName]
        nameString = ''
        for name in nameList:
            nameString += name + '\r\n'
        pyperclip.copy(nameString)

    def resetResultTablesAndTabs(self):
        for sl in self.searchers:
            sl.searcher.reset()
            sl.attachedToTabWidget = False
        self.ui_TAB_results.clear()

    def ui_setState(self, state, message=''):
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
        elif state == SEARCH_STATE_ERROR:
            stack.setCurrentWidget(self.ui_STKPG_status)
            self.ui_TXT_status.setText(message)
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
        sd = searchers.SearchDesc()
        sd.searchString = str(self.ui_LED_search.text()).strip()
        sd.caseSensitive = self.ui_BTN_soCaseSensitive.isChecked()
        sd.regex = self.ui_BTN_soRegex.isChecked()
        sd.selectFound = self.ui_BTN_soSelectFound.isChecked()
        sd.includeShapes = self.ui_BTN_soIncludeShapes.isChecked()
        sd.searchSelected = self.ui_BTN_soSearchSelected.isChecked()
        return sd

    def ui_tryToSaveTabOptVar(self):
        currentSL = self.getCurrentSearcherLink()
        if currentSL:
            m.optionVar(stringValue=(OPT_VAR_CURRENT_TAB, currentSL.searcher.getName()))

    def ui_tryShowSavedTab(self):
        if not m.optionVar(exists=OPT_VAR_CURRENT_TAB):
            return
        savedTabName = m.optionVar(q=OPT_VAR_CURRENT_TAB)
        if not savedTabName:
            return
        for sl in self.searchers:
            if sl.attachedToTabWidget and sl.searcher.getName() == savedTabName:
                self.ui_TAB_results.setCurrentWidget(sl.tabWidget)
                return

    def getCurrentSearcherLink(self):
        currentWidget = self.ui_TAB_results.currentWidget()
        if currentWidget is None:
            return None
        for sl in self.searchers:
            if sl.tabWidget is currentWidget:
                return sl

    def ui_onShowHelpClicked(self):
        # noinspection PyArgumentList,PyCallByClass
        import webbrowser
        webbrowser.open('http://davydenko.info/searcher/', new=0, autoraise=True)

    def ui_onCloseClicked(self):
        self.close()

    # noinspection PyMethodOverriding
    def closeEvent(self, event):
        self.ui_saveSettings()
        self.ui_tryToSaveTabOptVar()
        global mainWin
        mainWin = None
        event.accept()


class SearcherLink(object):

    def __init__(self, searcher, button, table, tabWidget):
        self.searcher = searcher
        self.button = button
        self.table = table
        self.tabWidget = tabWidget
        self.attachedToTabWidget = False


def run():
    global mainWin
    if not mainWin:
        mainWin = SearchUI()
    mainWin.show()
    mainWin.raise_()
