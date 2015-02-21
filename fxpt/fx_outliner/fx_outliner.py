#region imports

import functools as ft
import os
import xml.etree.ElementTree

import maya.cmds as m
import maya.mel as mel
import maya.OpenMayaUI as omui
import maya.OpenMaya as om

import shiboken
from PySide import QtCore
from PySide import QtGui

from fxpt.fx_prefsaver import PrefSaver, Serializers

from fxpt.fx_utils.qtFontCreator import QtFontCreator
from fxpt.fx_utils.utils import getFxUtilsDir

#endregion

#region constants

OS_NAME = os.name

SCRIPT_VERSION = 'v1.5'
SCRIPT_NAME = 'FX Outliner'
UI_WIN_NAME = 'fx_outliner_win'
UI_WIN_TITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION
SCRIPT_DIR = os.path.dirname(__file__)
OPT_VAR_NAME = 'fx_outliner'
XML_OUTLINER_CFG_FILE = SCRIPT_DIR + '\\fx_outliner.xml'
XML_USER_MENU_FILE = SCRIPT_DIR + '\\fx_outliner_user_menu.xml'
README_FILE = SCRIPT_DIR + '\\readme.txt'
FILTER_DESC = 'fx_outliner_filter'
OUTLINER_PANEL = 'FX Outliner Panel'

IDX_NAME = 0
IDX_TYPE = 1
IDX_PATH = 2

ICON_SEARCH = 'zoom.png'
ICON_CASE_SENSITIVE = SCRIPT_DIR + '\\icons\\fx_outliner_case.png'
ICON_REGEX = SCRIPT_DIR + '\\icons\\fx_outliner_regex.png'
ICON_SELECT_FOUND = SCRIPT_DIR + '\\icons\\fx_outliner_select.png'
ICON_TYPE_SEARCH = SCRIPT_DIR + '\\icons\\fx_outliner_type.png'
ICON_SHAPE = SCRIPT_DIR + '\\icons\\fx_outliner_shape.png'
ICON_POPUP_MENU = 'popupMenuIcon.png'
ICON_SHOW_SHAPES = 'frameBranch.png'
ICON_SHOW_SET_MEMBERS = 'out_objectSet.png'
ICON_SELECT_SET_MEMBERS = 'setEdit.png'
ICON_SORT_NAME = 'sortName.png'
ICON_SORT_TYPE = 'sortType.png'
ICON_SORT_REVERSED = 'reverseOrder.png'

qtFontCreator = QtFontCreator(getFxUtilsDir() + '/proggy_tiny_sz.ttf', 12)
FONT_MONOSPACE_QFONT = qtFontCreator.getQFont()
FONT_MONOSPACE_LETTER_SIZE = qtFontCreator.getLetterSize('i')

WAIT_WND_TOP_OFFSET = 70
WAIT_WND_HEIGHT = 30
WAIT_WND_WIDTH_RATIO = 0.7

#endregion


def dummyFunc():
    pass


def getMayaMainWindowPtr():
    # noinspection PyArgumentList
    ptr = omui.MQtUtil.mainWindow()
    if not ptr:
        raise RuntimeError('Cannot find Maya main window.')
    else:
        return ptr


def getMayaQMainWindow(ptr):
    return shiboken.wrapInstance(long(ptr), QtGui.QMainWindow)


class SearchResultsDialog(QtGui.QDialog):
    
    def __init__(self):
        mayaMainWin = getMayaQMainWindow(getMayaMainWindowPtr())
        super(SearchResultsDialog, self).__init__(mayaMainWin)
        self.setupUI()

    # noinspection PyAttributeOutsideInit
    def setupUI(self):
        self.setObjectName('SearchResultsDialog')
        self.setWindowTitle('Search Results')
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        self.setLayout(layout)
        self.ui_TBL_results = QtGui.QTableView()
        layout.addWidget(self.ui_TBL_results)

    # noinspection PyMethodMayBeStatic
    def showDlg(self):
        self.show()
        self.raise_()

    def getResultsTable(self):
        return self.ui_TBL_results


# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic,PyUnresolvedReferences,PyUnusedLocal
class FXOutlinerUI:
    def __init__(self):
        self.searchResult = []
        self.state = OutlinerState()
        self.userMenu = []  # list of tuples (command_name, command_string)
        self.ui_WND_wait = None

        self.searchResultDlg = SearchResultsDialog()
        self.ui_createUI()

    def ui_createUI(self):

        if m.window(UI_WIN_NAME, exists=True):
            if m.window(UI_WIN_NAME, q=True, visible=True):
                return
            else:
                m.deleteUI(UI_WIN_NAME, window=True)

        self.window = m.window(
            UI_WIN_NAME,
            title=UI_WIN_TITLE,
            maximizeButton=False,
        )

        m.scriptJob(event=['deleteAll', self.scriptJobDeleteAll], parent=self.window, protected=True)
        self.delUIScriptJobID = m.scriptJob(uiDeleted=[self.window, self.ui_onDeleteMainWin], protected=True)

        self.ui_LAY_mainForm = m.formLayout()

        # - - - - - - - - - - - - - - - - -

        self.ui_LAY_searchRow = m.rowLayout(
            numberOfColumns=8,
            adjustableColumn=2
        )

        self.ui_BTN_miscOperations = m.symbolButton(
            image=ICON_POPUP_MENU,
            width=22, height=22
        )

        self.loadUserCommandsFromXML()
        self.ui_POP_miscOperations = m.popupMenu(button=1)
        for command in self.userMenu:
            m.menuItem(
                parent=self.ui_POP_miscOperations,
                label=command[0],
                command=ft.partial(self.evalMelCommand, command[1])
            )
        m.menuItem(divider=True)
        m.menuItem(
            parent=self.ui_POP_miscOperations,
            label='Open FX Outliner Configuration File',
            command=ft.partial(self.openFileInEditor, XML_OUTLINER_CFG_FILE)
        )
        m.menuItem(
            parent=self.ui_POP_miscOperations,
            label='Open FX Outliner User Menu Configuration File',
            command=ft.partial(self.openFileInEditor, XML_USER_MENU_FILE)
        )
        m.menuItem(divider=True)
        m.menuItem(
            parent=self.ui_POP_miscOperations,
            label='Help',
            command=ft.partial(self.openFileInEditor, README_FILE)
        )

        m.setParent(self.ui_LAY_searchRow)

        self.ui_TFD_search = m.textField(
            enterCommand=self.ui_BTN_searchClick,
            alwaysInvokeEnterCommandOnReturn=True
        )
        self.ui_BTN_search = m.symbolButton(
            image=ICON_SEARCH,
            width=22, height=22,
            annotation='Perform Search',
            command=self.ui_BTN_searchClick
        )
        self.ui_BTN_searchCase = m.symbolCheckBox(
            image=ICON_CASE_SENSITIVE,
            width=22, height=22,
            annotation='Search: Case Sensitive',
            changeCommand=self.ui_BTN_searchCaseChange
        )
        self.ui_BTN_searchRegEx = m.symbolCheckBox(
            image=ICON_REGEX,
            width=22, height=22,
            annotation='Search: Regular Expression',
            changeCommand=self.ui_BTN_searchRegExChange
        )
        self.ui_BTN_searchType = m.symbolCheckBox(
            image=ICON_TYPE_SEARCH,
            width=22, height=22,
            annotation='Search: Search for Type',
            changeCommand=self.ui_BTN_searchTypeChange
        )
        self.ui_BTN_searchSelect = m.symbolCheckBox(
            image=ICON_SELECT_FOUND,
            width=22, height=22,
            annotation='Search: Select Result',
            changeCommand=self.ui_BTN_searchSelectChange
        )
        self.ui_BTN_searchShape = m.symbolCheckBox(
            image=ICON_SHAPE,
            width=22, height=22,
            annotation='Search: Include Shapes in Search',
            changeCommand=self.ui_BTN_searchShapeChange
        )

        # - - - - - - - - - - - - - - - - -

        m.setParent(self.ui_LAY_mainForm)

        self.ui_SEP_searchSeparator = m.separator(style='in', height=6)

        # - - - - - - - - - - - - - - - - -

        self.ui_LAY_outlinerForm = m.formLayout()

        self.ui_BTN_modeDropDown = m.button(
            height=24
        )

        # - - - - - - - - - - - - - - - - -

        self.generateOutlinerViews()

        self.ui_POP_mode = m.popupMenu(button=1)
        for viewCfg in self.state.outlinerViews:
            m.menuItem(
                parent=self.ui_POP_mode,
                label=viewCfg.name,
                command=ft.partial(self.ui_POP_mode_onClick, viewCfg)
            )

        lastPrebuildViewIndex = len(self.state.outlinerViews)
        self.loadOutlinerViewsFromXML()
        m.menuItem(
            parent=self.ui_POP_mode,
            divider=True,
        )

        for i in range(lastPrebuildViewIndex, len(self.state.outlinerViews)):
            vc = self.state.outlinerViews[i]
            m.menuItem(
                parent=self.ui_POP_mode,
                label=vc.name,
                command=ft.partial(self.ui_POP_mode_onClick, vc)
            )

        # - - - - - - - - - - - - - - - - -

        m.setParent(self.ui_LAY_outlinerForm)

        fxOutlinerPanels = [x for x in
                            m.getPanel(type='outlinerPanel')
                            if m.outlinerPanel(x, q=True, label=True) == OUTLINER_PANEL
                            ]
        if fxOutlinerPanels:
            self.ui_PNL_outliner = fxOutlinerPanels[0]
            m.outlinerPanel(self.ui_PNL_outliner, e=True, unParent=True)
            m.outlinerPanel(self.ui_PNL_outliner, e=True, parent=self.ui_LAY_outlinerForm)
        else:
            self.ui_PNL_outliner = m.outlinerPanel(
                menuBarVisible=False,
                label=OUTLINER_PANEL
            )

        self.ui_EDT_outliner = m.outlinerPanel(
            self.ui_PNL_outliner,
            query=True,
            outlinerEditor=True,
        )

        # - - - - - - - - - - - - - - - - -

        m.setParent(self.ui_LAY_outlinerForm)

        self.ui_LAY_outlinerToolbar = m.columnLayout()

        self.ui_BTN_showShapes = m.symbolCheckBox(
            image=ICON_SHOW_SHAPES,
            height=35, width=35,
            changeCommand=self.ui_BTN_showShapesChange,
            annotation='Show Shapes'
        )
        self.ui_BTN_showSetMembers = m.symbolCheckBox(
            image=ICON_SHOW_SET_MEMBERS,
            height=35, width=35,
            changeCommand=self.ui_BTN_showSetMembersChange,
            annotation='Show Set Members'
        )
        self.ui_BTN_selectSetMembers = m.symbolCheckBox(
            image=ICON_SELECT_SET_MEMBERS,
            height=35, width=35,
            changeCommand=self.ui_BTN_selectSetMembersChange,
            annotation='Select Set Members \ Assigned Objects'
        )

        # - - - - - - - - - - - - - - - - -

        m.formLayout(self.ui_LAY_outlinerForm, e=True, attachForm=(self.ui_BTN_modeDropDown, 'top', 2))
        m.formLayout(self.ui_LAY_outlinerForm, e=True,
                     attachControl=(self.ui_BTN_modeDropDown, 'right', 2, self.ui_LAY_outlinerToolbar))
        m.formLayout(self.ui_LAY_outlinerForm, e=True, attachNone=(self.ui_BTN_modeDropDown, 'bottom'))
        m.formLayout(self.ui_LAY_outlinerForm, e=True, attachForm=(self.ui_BTN_modeDropDown, 'left', 2))

        m.formLayout(self.ui_LAY_outlinerForm, e=True,
                     attachControl=(self.ui_PNL_outliner, 'top', 2, self.ui_BTN_modeDropDown))
        m.formLayout(self.ui_LAY_outlinerForm, e=True,
                     attachControl=(self.ui_PNL_outliner, 'right', 2, self.ui_LAY_outlinerToolbar))
        m.formLayout(self.ui_LAY_outlinerForm, e=True, attachForm=(self.ui_PNL_outliner, 'bottom', 2))
        m.formLayout(self.ui_LAY_outlinerForm, e=True, attachForm=(self.ui_PNL_outliner, 'left', 2))

        m.formLayout(self.ui_LAY_outlinerForm, e=True, attachForm=(self.ui_LAY_outlinerToolbar, 'top', 2))
        m.formLayout(self.ui_LAY_outlinerForm, e=True, attachForm=(self.ui_LAY_outlinerToolbar, 'right', 2))
        m.formLayout(self.ui_LAY_outlinerForm, e=True, attachForm=(self.ui_LAY_outlinerToolbar, 'bottom', 2))
        m.formLayout(self.ui_LAY_outlinerForm, e=True, attachNone=(self.ui_LAY_outlinerToolbar, 'left'))

        # - - - - - - - - - - - - - - - - -

        self.ui_LAY_attachFrame = m.frameLayout(
            marginHeight=2, marginWidth=2,
            borderVisible=False,
            labelVisible=False
        )

        self.ui_QT_TBL_searchResult = self.searchResultDlg.getResultsTable()

        self.searchResultModel = SearchResultModel()
        self.ui_searchResultTableSetProps()
        self.ui_QT_TBL_searchResult.setModel(self.searchResultModel)
        # double ui_searchResultTableSetProps cause some props need to be set # double ui_searchResultTableSetProps cause some props need to be set
        self.ui_searchResultTableSetProps()

        self.ui_QT_TBL_searchResult.connect(
            self.ui_QT_TBL_searchResult.selectionModel(),
            QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'),
            self.ui_QT_TBL_searchResult_selectionChanges
        )

        # - - - - - - - - - - - - - - - - -

        m.formLayout(self.ui_LAY_mainForm, e=True, attachForm=(self.ui_LAY_searchRow, 'top', 2))
        m.formLayout(self.ui_LAY_mainForm, e=True, attachForm=(self.ui_LAY_searchRow, 'right', 2))
        m.formLayout(self.ui_LAY_mainForm, e=True, attachNone=(self.ui_LAY_searchRow, 'bottom'))
        m.formLayout(self.ui_LAY_mainForm, e=True, attachForm=(self.ui_LAY_searchRow, 'left', 2))

        m.formLayout(self.ui_LAY_mainForm, e=True,
                     attachControl=(self.ui_SEP_searchSeparator, 'top', 2, self.ui_LAY_searchRow))
        m.formLayout(self.ui_LAY_mainForm, e=True, attachForm=(self.ui_SEP_searchSeparator, 'right', 2))
        m.formLayout(self.ui_LAY_mainForm, e=True, attachNone=(self.ui_SEP_searchSeparator, 'bottom'))
        m.formLayout(self.ui_LAY_mainForm, e=True, attachForm=(self.ui_SEP_searchSeparator, 'left', 2))

        m.formLayout(self.ui_LAY_mainForm, e=True,
                     attachControl=(self.ui_LAY_outlinerForm, 'top', 2, self.ui_SEP_searchSeparator))
        m.formLayout(self.ui_LAY_mainForm, e=True, attachForm=(self.ui_LAY_outlinerForm, 'right', 2))
        m.formLayout(self.ui_LAY_mainForm, e=True, attachForm=(self.ui_LAY_outlinerForm, 'bottom', 2))
        m.formLayout(self.ui_LAY_mainForm, e=True, attachForm=(self.ui_LAY_outlinerForm, 'left', 2))

        # - - - - - - - - - - - - - - - - -

        m.showWindow(self.window)

        # - - - - - - - - - - - - - - - - -

        self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerOptVar(OPT_VAR_NAME))
        self.prefSaver.addControl(self.searchResultDlg, PrefSaver.UIType.PYSIDEWindow, (200, 200, 500, 700))
        self.prefSaver.addVariable('fx_outliner_state', self.prefsPack, self.prefsUnPack, None)
        self.prefsLoad()
        self.ui_update()

        m.setFocus(self.ui_LAY_outlinerForm)

    def ui_searchResultTableSetProps(self, columnMaxLengthName=10, columnMaxLengthType=10, columnMaxLengthPath=10):
        table = self.ui_QT_TBL_searchResult
        table.setShowGrid(False)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(15)
        table.setSelectionBehavior(QtGui.QTableView.SelectRows)
        table.setSelectionMode(QtGui.QTableView.ExtendedSelection)
        table.setFont(FONT_MONOSPACE_QFONT)
        table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        #        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.setSortingEnabled(True)
        table.sortByColumn(0, QtCore.Qt.AscendingOrder)
        table.setAlternatingRowColors(True)
        table.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)

        table.horizontalHeader().resizeSection(IDX_NAME, columnMaxLengthName * FONT_MONOSPACE_LETTER_SIZE + 20)
        table.horizontalHeader().resizeSection(IDX_TYPE, columnMaxLengthType * FONT_MONOSPACE_LETTER_SIZE + 20)
        table.horizontalHeader().resizeSection(IDX_PATH, columnMaxLengthPath * FONT_MONOSPACE_LETTER_SIZE + 20)

        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

    def ui_showResultsDlg(self):
        self.searchResultDlg.showDlg()
        self.ui_update()

    def ui_POP_mode_onClick(self, ov, *arg):
        self.state.currentView = ov
        self.ui_update()

    def ui_BTN_showShapesChange(self, state):
        self.state.currentView.showShapes = state
        self.ui_update()

    def ui_BTN_searchCaseChange(self, state):
        self.state.searchCase = state
        self.ui_update()

    def ui_BTN_searchRegExChange(self, state):
        self.state.searchRegex = state
        self.ui_update()

    def ui_BTN_searchTypeChange(self, state):
        self.state.searchType = state
        self.ui_update()

    def ui_BTN_searchSelectChange(self, state):
        self.state.searchSelect = state
        self.ui_update()

    def ui_BTN_searchShapeChange(self, state):
        self.state.searchShape = state
        self.ui_update()

    def ui_BTN_showSetMembersChange(self, state):
        self.state.currentView.showSetMembers = state
        self.ui_update()

    def ui_BTN_selectSetMembersChange(self, state):
        self.state.currentView.selectSetMembers = state
        self.ui_update()

    def ui_QT_TBL_searchResult_selectionChanges(self):
        selectedIndexes = self.ui_QT_TBL_searchResult.selectionModel().selectedRows()  # column = 0 by default
        selectionList = []
        for index in selectedIndexes:
            selectionList.append(index.data(role=QtCore.Qt.UserRole))
        if selectedIndexes:
            m.select(selectionList, noExpand=True)
        else:
            m.select(clear=True)

    def ui_BTN_searchClick(self, arg):

        # self.ui_waitWindowShow()

        caseSensitivity = QtCore.Qt.CaseSensitive if self.state.searchCase else QtCore.Qt.CaseInsensitive
        patternType = QtCore.QRegExp.RegExp if self.state.searchRegex else QtCore.QRegExp.Wildcard
        searchType = self.state.searchType
        searchString = self.ui_getSearchString()

        lsResult = m.ls(long=True, showType=True)

        sceneNodes = {}
        for i in range(0, len(lsResult), 2):
            fullPathname = lsResult[i]
            splittedName = lsResult[i].split('|')
            nodeName = splittedName.pop()
            nodePath = '|'.join(splittedName)
            nodeType = lsResult[i + 1]
            sceneNodes[fullPathname] = (nodeName, nodeType, nodePath)

        if not self.state.searchShape:
            sceneNodesFiltered = {}
            selectionList = om.MSelectionList()
            mObject = om.MObject()

            for key in sceneNodes.iterkeys():
                nodeName, nodeType, nodePath = sceneNodes[key]
                selectionList.clear()
                selectionList.add(key)
                selectionList.getDependNode(0, mObject)
                if mObject.hasFn(om.MFn.kShape):
                    if not nodeType in [x.strip() for x in sceneNodes[nodePath][IDX_TYPE].split(',')]:
                        sceneNodes[nodePath] = (
                            sceneNodes[nodePath][IDX_NAME], sceneNodes[nodePath][IDX_TYPE] + ', ' + nodeType,
                            sceneNodes[nodePath][IDX_PATH]
                        )  # add shape type to its' transform type string
                    sceneNodes[key] = None
            for key in sceneNodes.iterkeys():
                if sceneNodes[key]:
                    sceneNodesFiltered[key] = sceneNodes[key]
        else:
            sceneNodesFiltered = sceneNodes

        self.searchResultModel.search(sceneNodesFiltered, searchString, caseSensitivity, patternType, searchType)

        nodeNames = [len(self.searchResultModel.index(row, IDX_NAME).data(QtCore.Qt.DisplayRole)) for row in
                     range(self.searchResultModel.rowCount())]
        nodeTypes = [len(self.searchResultModel.index(row, IDX_TYPE).data(QtCore.Qt.DisplayRole)) for row in
                     range(self.searchResultModel.rowCount())]
        nodePaths = [len(self.searchResultModel.index(row, IDX_PATH).data(QtCore.Qt.DisplayRole)) for row in
                     range(self.searchResultModel.rowCount())]
        columnMaxLengthName = max(nodeNames) if nodeNames else 10
        columnMaxLengthType = max(nodeTypes) if nodeTypes else 10
        columnMaxLengthPath = max(nodePaths) if nodePaths else 10

        self.ui_searchResultTableSetProps(columnMaxLengthName, columnMaxLengthType, columnMaxLengthPath)

        if self.state.searchSelect:
            if self.searchResultModel.rowCount():
                self.ui_QT_TBL_searchResult.selectAll()
            else:
                m.select(clear=True)
        else:
            self.ui_showResultsDlg()

        # self.ui_waitWindowHide()

    def ui_getSearchString(self):
        textFieldString = m.textField(self.ui_TFD_search, q=True, text=True)
        textFieldString = textFieldString.strip().split()
        if textFieldString:
            return textFieldString[0]
        else:
            return ''

    def ui_update(self):
        self.prefsSave()

        m.symbolCheckBox(self.ui_BTN_searchCase, e=True, value=self.state.searchCase)
        m.symbolCheckBox(self.ui_BTN_searchRegEx, e=True, value=self.state.searchRegex)
        m.symbolCheckBox(self.ui_BTN_searchType, e=True, value=self.state.searchType)
        m.symbolCheckBox(self.ui_BTN_searchSelect, e=True, value=self.state.searchSelect)
        m.symbolCheckBox(self.ui_BTN_searchShape, e=True, value=self.state.searchShape)

        ov = self.state.currentView

        m.button(self.ui_BTN_modeDropDown, edit=True, label=ov.name)

        m.outlinerEditor(self.ui_EDT_outliner, edit=True, mainListConnection=ov.mainListConnection)
        m.outlinerEditor(self.ui_EDT_outliner, edit=True, selectionConnection=ov.selectionConnection)
        m.outlinerEditor(self.ui_EDT_outliner, edit=True, filter=ov.filter)
        m.outlinerEditor(self.ui_EDT_outliner, edit=True, setFilter=ov.setFilter)
        m.outlinerEditor(self.ui_EDT_outliner, edit=True, showShapes=ov.showShapes)
        m.outlinerEditor(self.ui_EDT_outliner, edit=True, showSetMembers=ov.showSetMembers)
        m.outlinerEditor(self.ui_EDT_outliner, edit=True, showDagOnly=ov.showDagOnly)
        m.outlinerEditor(self.ui_EDT_outliner, edit=True, expandObjects=ov.expandObjects)

        m.outlinerEditor(self.ui_EDT_outliner, edit=True,
                         selectCommand=(ov.selectCommand if ov.selectCommand else dummyFunc))

        m.symbolCheckBox(self.ui_BTN_showShapes, e=True, enable=ov.showShapesEnable, value=ov.showShapes)
        m.symbolCheckBox(self.ui_BTN_showSetMembers, e=True, enable=ov.showSetMembersEnable, value=ov.showSetMembers)
        m.symbolCheckBox(self.ui_BTN_selectSetMembers, e=True, enable=ov.selectSetMembersEnable,
                         value=ov.selectSetMembers)

    def ui_waitWindowShow(self):
        if not self.ui_WND_wait:
            self.ui_WND_wait = QtGui.QWidget()
            layout = QtGui.QHBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            self.ui_WND_wait.setLayout(layout)
            label = QtGui.QLabel('Searching...')
            label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            label.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
            layout.addWidget(label)
            self.ui_WND_wait.setWindowFlags(QtCore.Qt.Popup)

        parentTopLeft = self.ui_QT_TBL_searchResult.mapToGlobal(self.ui_QT_TBL_searchResult.rect().topLeft())
        parentX = parentTopLeft.x()
        parentY = parentTopLeft.y()
        parentWidth = self.ui_QT_TBL_searchResult.rect().width()

        waitWndWidth = parentWidth * WAIT_WND_WIDTH_RATIO
        waitWndX = parentX + (parentWidth - waitWndWidth) / 2

        self.ui_WND_wait.move(waitWndX, parentY + WAIT_WND_TOP_OFFSET)
        self.ui_WND_wait.resize(waitWndWidth, WAIT_WND_HEIGHT)

        self.ui_WND_wait.show()
        self.ui_WND_wait.raise_()
        self.ui_WND_wait.repaint()

    def ui_waitWindowHide(self):
        if self.ui_WND_wait:
            self.ui_WND_wait.hide()

    def scriptJobDeleteAll(self):
        m.scriptJob(kill=self.delUIScriptJobID, force=True)
        m.deleteUI(UI_WIN_NAME, window=True)
        run()

    def ui_onDeleteMainWin(self):
        self.prefsSave()
        self.searchResultDlg.close()

        # clean up filters
        for ov in self.state.outlinerViews:
            if ov.filter and m.objExists(ov.filter):
                m.delete(ov.filter)
            if (ov.setFilter != 'defaultSetFilter') and m.objExists(ov.setFilter):
                m.delete(ov.setFilter)

    def ui_onOutlinerSelectSG(self, sc):
        if self.state.currentView.selectSetMembers:
            SGs = m.selectionConnection(sc, q=True, object=True)
            if not SGs:
                return
            assignedTo = m.sets(SGs, q=True)
            if assignedTo:
                m.select(assignedTo)

    def ui_onOutlinerSelectMatTex(self, sc):
        if self.state.currentView.selectSetMembers:
            selected = m.selectionConnection(sc, q=True, object=True)
            if not selected:
                return
            SGs = self.getSGs(selected)
            if not SGs:
                return
            assignedTo = m.sets(SGs, q=True)
            if assignedTo:
                m.select(assignedTo)

    def getSGs(self, src):
        SGs = []
        for s in src:
            connectedSGs = m.listConnections(s, d=True, s=False, type='shadingEngine', exactType=True)
            if connectedSGs:
                SGs.extend(connectedSGs)
            nextLevel = []

            for c in m.listConnections(s, d=True, s=False):
                if (m.getClassification(m.nodeType(c), satisfies='shader') or
                        m.getClassification(m.nodeType(c), satisfies='texture') or
                        m.getClassification(m.nodeType(c), satisfies='utility')):
                    nextLevel.append(c)

            for nl in nextLevel:
                SGs.extend(self.getSGs([nl]))
        return SGs

    def ui_errorDialog(self, errorMsg):
        m.confirmDialog(
            title='Error',
            message=errorMsg,
            button='Ok',
            defaultButton='Ok',
            cancelButton='Ok',
            icon='critical'
        )
        m.error(errorMsg)

    def generateOutlinerViews(self):

        self.state.outlinerViews = []

        # --- DAG Nodes Only ---

        ov = OutlinerView(
            name='DAG Nodes',
        )
        self.state.outlinerViews.append(ov)

        # --- All Objects ---

        ov = OutlinerView(
            name='All Nodes',
            showDagOnly=False
        )
        self.state.outlinerViews.append(ov)

        # --- Shading Groups ---

        ov = OutlinerView(
            name='Shading Groups',
            showSetMembers=False,
            expandObjects=True,
            showShapesEnable=False,
            selectSetMembersEnable=True
        )
        ov.filter = m.itemFilter(byType='shadingEngine', text=FILTER_DESC)
        ov.setFilter = m.itemFilter(text=FILTER_DESC)
        ov.selectCommand = ft.partial(self.ui_onOutlinerSelectSG, ov.selectionConnection)
        self.state.outlinerViews.append(ov)

        # --- Materials ---

        ov = OutlinerView(
            name='Materials',
            showDagOnly=False,
            showShapesEnable=False,
            showSetMembersEnable=False,
            selectSetMembersEnable=True
        )
        ov.filter = m.itemFilter(
            byType=['lambert', 'particleCloud', 'anisotropic', 'blinn', 'hairTubeShader', 'layeredShader',
                    'oceanShader', 'phong', 'phongE', 'rampShader', 'shadingMap', 'surfaceShader', 'useBackground',
                    'envFog', 'fluidShape', 'lightFog', 'volumeFog', 'volumeShader'], text=FILTER_DESC)
        ov.selectCommand = ft.partial(self.ui_onOutlinerSelectMatTex, ov.selectionConnection)
        self.state.outlinerViews.append(ov)

        # --- Textures ---

        ov = OutlinerView(
            name='Textures',
            showDagOnly=False,
            showShapesEnable=False,
            showSetMembersEnable=False,
            selectSetMembersEnable=True
        )
        ov.filter = m.itemFilter(
            byType=['file', 'mountain', 'cloth', 'water', 'psdFileTex', 'fractal', 'fluidTexture2D', 'grid', 'ramp',
                    'movie', 'ocean', 'bulge', 'checker', 'noise', 'fluidTexture3D', 'stucco', 'wood', 'snow',
                    'solidFractal', 'crater', 'volumeNoise', 'brownian', 'granite', 'marble', 'leather', 'cloud',
                    'rock'], text=FILTER_DESC)
        ov.selectCommand = ft.partial(self.ui_onOutlinerSelectMatTex, ov.selectionConnection)
        self.state.outlinerViews.append(ov)

        # ------------------------------------

        self.state.currentView = self.state.outlinerViews[0]

    def loadOutlinerViewsFromXML(self):
        if not os.path.exists(XML_OUTLINER_CFG_FILE):
            return

        tree = None
        try:
            tree = xml.etree.ElementTree.parse(XML_OUTLINER_CFG_FILE)
        except Exception as e:
            self.ui_errorDialog(
                'Error loading user views from file.\nFilename: ' + XML_OUTLINER_CFG_FILE + '\n\n' +
                'Additional exception info:\n' + str(e))

        def xmlParseBool(s):
            if s.lower() in ['true', '1', 't', 'y', 'yes']:
                return True
            elif s.lower() in ['false', '0', 'f', 'n', 'no']:
                return False
            else:
                self.ui_errorDialog('Error parsing boolean attribute "' + s + '" from file\n' + XML_OUTLINER_CFG_FILE)

        for view in tree.findall('view'):
            ov = OutlinerView()

            if 'name' in view.attrib:
                ov.name = view.attrib['name']
            if 'showShapes' in view.attrib:
                ov.showShapes = xmlParseBool(view.attrib['showShapes'])
            if 'showShapesEnable' in view.attrib:
                ov.showShapesEnable = xmlParseBool(view.attrib['showShapesEnable'])
            if 'showDagOnly' in view.attrib:
                ov.showDagOnly = xmlParseBool(view.attrib['showDagOnly'])
            if 'showSetMembers' in view.attrib:
                ov.showSetMembers = xmlParseBool(view.attrib['showSetMembers'])
            if 'showSetMembersEnable' in view.attrib:
                ov.showSetMembersEnable = xmlParseBool(view.attrib['showSetMembersEnable'])
            if 'expandObjects' in view.attrib:
                ov.expandObjects = xmlParseBool(view.attrib['expandObjects'])
            if 'selectSetMembersEnable' in view.attrib:
                ov.selectSetMembersEnable = xmlParseBool(view.attrib['selectSetMembersEnable'])

            filterList = [x.strip(' ,;') for x in view.text.strip().split()]
            if filterList:
                ov.filter = m.itemFilter(byType=filterList, text=FILTER_DESC)

            self.state.outlinerViews.append(ov)

    def prefsSave(self):
        self.prefSaver.savePrefs()

    def prefsLoad(self):
        self.prefSaver.loadPrefs()

    def prefsPack(self):

        prefDict = {}

        for attrName in (
            'searchCase',
            'searchRegex',
            'searchType',
            'searchSelect',
            'searchShape'
        ):
            prefDict[attrName] = getattr(self.state, attrName)

        prefDict['currentViewName'] = self.state.currentView.name

        ovDict = {}
        prefDict['outlinerViews'] = ovDict

        for ov in self.state.outlinerViews:
            ovDict[ov.name] = {
                'showShapes': ov.showShapes,
                'showSetMembers': ov.showSetMembers,
                'selectSetMembers': ov.selectSetMembers,
            }

        return prefDict

    def prefsUnPack(self, prefDict):
        if not prefDict:
            return

        for attrName in (
            'searchCase',
            'searchRegex',
            'searchType',
            'searchSelect',
            'searchShape'
        ):
            setattr(self.state, attrName, prefDict.get(attrName, False))

        currentViewItem = [x for x in self.state.outlinerViews if x.name == prefDict.get('currentViewName', '')]
        if currentViewItem:
            self.state.currentView = currentViewItem[0]

        for ov in self.state.outlinerViews:
            if 'outlinerViews' in prefDict:
                if ov.name in prefDict['outlinerViews']:
                    viewDict = prefDict['outlinerViews'][ov.name]
                    ov.showShapes = viewDict.get('showShapes', False)
                    ov.showSetMembers = viewDict.get('showSetMembers', False)
                    ov.selectSetMembers = viewDict.get('selectSetMembers', False)

    def loadUserCommandsFromXML(self):

        if not os.path.exists(XML_USER_MENU_FILE):
            return

        tree = None
        try:
            tree = xml.etree.ElementTree.parse(XML_USER_MENU_FILE)
        except Exception as e:
            self.ui_errorDialog(
                'Error loading user commands from file.\nFilename: ' + XML_USER_MENU_FILE + '\n\n' +
                'Additional exception info:\n' + str(e))

        for command in tree.findall('command'):

            if 'name' in command.attrib:
                commandName = command.attrib['name']
            else:
                commandName = 'Unnamed User Command'
            commandString = command.text.strip()
            self.userMenu.append((commandName, commandString))

    def evalMelCommand(self, cmd, *arg):
        mel.eval(cmd)

    def openFileInEditor(self, filename, *arg):
        # this works only on Windows
        # don't have MacOS or Linux system to test other cases
        # so if anybody knows how to write this procedure to handle mac or linux please tell me
        if OS_NAME == 'nt':
        #            os.startfile(filename)
            os.system('start notepad.exe ' + filename)
        else:
            m.confirmDialog(
                title='Error',
                message='Config file you are looking for:\n' + filename +
                        "\nSorry, but i don't know how to open this file in editor in your system.",
                button='Ok',
                defaultButton='Ok',
                cancelButton='Ok',
                icon='critical'
            )


class SearchResultModel(QtGui.QSortFilterProxyModel):
    def __init__(self):
        QtGui.QSortFilterProxyModel.__init__(self)
        self.model = QtGui.QStandardItemModel()
        self.initModel()
        self.setSourceModel(self.model)

    def initModel(self):
        self.model.clear()
        self.model.setRowCount(0)
        self.model.setColumnCount(3)
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, 'Name', QtCore.Qt.DisplayRole)
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, 'Type', QtCore.Qt.DisplayRole)
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, 'Path', QtCore.Qt.DisplayRole)

    def search(self, sceneNodes, searchString, caseSensitivity, patternType, searchType):

        self.initModel()

        self.model.insertRows(0, len(sceneNodes))

        i = 0
        for fullPathname in sceneNodes.iterkeys():
            cell1 = self.model.index(i, 0)
            cell2 = self.model.index(i, 1)
            cell3 = self.model.index(i, 2)

            self.model.setData(cell1, sceneNodes[fullPathname][0])  # nodeName
            self.model.setData(cell2, sceneNodes[fullPathname][1])  # nodeType
            self.model.setData(cell3, sceneNodes[fullPathname][2])  # nodePath
            self.model.setData(cell1, fullPathname, QtCore.Qt.UserRole)

            i += 1

        if searchType:
            self.setFilterKeyColumn(1)
        else:
            self.setFilterKeyColumn(0)

        self.setFilterRegExp(QtCore.QRegExp(searchString, caseSensitivity, patternType))


class OutlinerState():
    def __init__(self):
        self.currentView = None
        self.currentViewName = ''
        self.searchCase = False
        self.searchRegex = False
        self.searchType = False
        self.searchSelect = False
        self.searchShape = False

        self.outlinerViews = None


class OutlinerView():
    def __init__(self,
                 name='Untitled',
                 mainListConnection='worldList',
                 selectionConnection='modelList',
                 flt='',
                 setFilter='defaultSetFilter',
                 showShapes=False,
                 showShapesEnable=True,
                 showDagOnly=True,
                 selectCommand=None,
                 showSetMembers=True,
                 showSetMembersEnable=True,
                 expandObjects=False,
                 selectSetMembers=False,
                 selectSetMembersEnable=False
                 ):
        self.name = name
        self.mainListConnection = mainListConnection
        self.selectionConnection = selectionConnection
        self.filter = flt
        self.setFilter = setFilter
        self.showShapes = showShapes
        self.showShapesEnable = showShapesEnable
        self.showDagOnly = showDagOnly
        self.selectCommand = selectCommand
        self.showSetMembers = showSetMembers
        self.showSetMembersEnable = showSetMembersEnable
        self.expandObjects = expandObjects
        self.selectSetMembers = selectSetMembers
        self.selectSetMembersEnable = selectSetMembersEnable


def run():
    FXOutlinerUI()
