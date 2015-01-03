from PySide import QtCore, QtGui

from fxpt.fx_utils.qtFontCreator import QtFontCreator
from fxpt.fx_utils.utils import getFxUtilsDir

from fxpt.fx_textureManager.MainWindowUI import Ui_MainWindow
from fxpt.fx_textureManager.Harvesters import MayaSceneHarvester

from fxpt.fx_prefsaver import PrefSaver, Serializers

qtFontCreator = QtFontCreator(getFxUtilsDir() + '/proggy_tiny_sz.ttf', 12)
FONT_MONOSPACE_QFONT = qtFontCreator.getQFont()
FONT_MONOSPACE_LETTER_SIZE = qtFontCreator.getLetterSize('i')

COL_IDX_EXIST = 0
COL_IDX_FILENAME = 1
COL_IDX_ATTR = 2

TABLE_COLUMN_NAMES = ('Exists', 'Filename', 'Attribute')

TABLE_MAX_COLUMN_SIZE = [0] * 3
TABLE_MAX_COLUMN_SIZE[COL_IDX_EXIST] = 5
TABLE_MAX_COLUMN_SIZE[COL_IDX_FILENAME] = 100
TABLE_MAX_COLUMN_SIZE[COL_IDX_ATTR] = 50

TABLE_COLUMN_RIGHT_OFFSET = 20
TABLE_HEADER_TITLE_OFFSET = 2

FILE_EXISTS_STRINGS = {
    False: (' No', QtGui.QColor(225, 75, 75)),
    True: (' Yes', QtGui.QColor(140, 220, 75))
}


OPT_VAR_NAME = 'fx_textureManager_prefs'


class TexManagerUI(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(TexManagerUI, self).__init__(parent=parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.harvester = MayaSceneHarvester()

        self.initModels()
        self.fillTable()

        self.createContextMenu()

        self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerOptVar(OPT_VAR_NAME))
        self.ui_initSettings()
        self.ui_loadSettings()

    def ui_initSettings(self):
        self.prefSaver.addControl(self, PrefSaver.UIType.PYSIDEWindow, (100, 100, 900, 600))
        self.prefSaver.addControl(self.ui.uiTBL_textures, PrefSaver.UIType.PYSIDETableView)
        self.prefSaver.addControl(self.ui.uiLED_filter, PrefSaver.UIType.PYSIDELineEdit, '')

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    def ui_resetSettings(self):
        self.prefSaver.resetPrefs()

    def createContextMenu(self):
        self.ui.uiTBL_textures.addAction(self.ui.uiACT_copyFullPath)
        self.ui.uiTBL_textures.addAction(self.ui.uiACT_copyFilename)

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

    def fillTable(self):

        self.model.clear()
        self.model.setRowCount(0)
        self.model.setColumnCount(len(TABLE_COLUMN_NAMES))
        for i, col in enumerate(TABLE_COLUMN_NAMES):
            self.model.setHeaderData(i, QtCore.Qt.Horizontal, col, QtCore.Qt.DisplayRole)

        texNodes = self.harvester.getTexNodes()

        self.model.insertRows(0, len(texNodes))

        for i, tn in enumerate(texNodes):

            modelIndex = self.model.index(i, COL_IDX_EXIST)
            fileExists = tn.fileExists()
            self.model.setData(modelIndex, FILE_EXISTS_STRINGS[fileExists][0])
            self.model.setData(modelIndex, FILE_EXISTS_STRINGS[fileExists][1], QtCore.Qt.ForegroundRole)

            modelIndex = self.model.index(i, COL_IDX_FILENAME)
            self.model.setData(modelIndex, tn.getAttrValue())

            modelIndex = self.model.index(i, COL_IDX_ATTR)
            self.model.setData(modelIndex, tn.getFullAttrName())
            self.model.setData(modelIndex, tn, QtCore.Qt.UserRole)

        self.setTableProps()

    def setTableProps(self):
        table = self.ui.uiTBL_textures
        table.setFont(FONT_MONOSPACE_QFONT)
        table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        # custom "resize to fit" section, cause standard table.resizeColumnsToContents() may be very slow on huge data
        model = self.model
        columnCount = model.columnCount()
        for col in range(columnCount):
            stringLengths = [len(model.index(row, col).data(QtCore.Qt.DisplayRole)) for row in range(model.rowCount())]
            stringLengths.append(len(str(model.headerData(col, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))) + TABLE_HEADER_TITLE_OFFSET)
            columnMaxLength = min(max(stringLengths), TABLE_MAX_COLUMN_SIZE[col])
            table.horizontalHeader().resizeSection(col, columnMaxLength * FONT_MONOSPACE_LETTER_SIZE + TABLE_COLUMN_RIGHT_OFFSET)

    def onFilterTextChanged(self):
        header = self.ui.uiTBL_textures.horizontalHeader()
        sortedSection = header.sortIndicatorSection()
        sortingOrder = header.sortIndicatorOrder()

        wildcard = self.ui.uiLED_filter.text()
        self.setFilterWildcard(wildcard)
        state = bool(wildcard)
        self.ui.uiBTN_filter.setEnabled(state)
        self.ui.uiBTN_filter.setChecked(state)

        self.ui.uiTBL_textures.sortByColumn(sortedSection, sortingOrder)

    def onFilterButtonToggled(self, state):
        if not state:
            self.ui.uiLED_filter.clear()

    def onRefreshTriggered(self):
        self.prefSaver.savePrefs()
        self.fillTable()
        self.onFilterTextChanged()
        self.prefSaver.loadPrefs()

    def onCopyFullPathTriggered(self):
        print 'onCopyFullPathTriggered()'

    def onCopyFilenameTriggered(self):
        print 'onCopyFilenameTriggered()'

    def onCopyMoveTriggered(self):
        print 'onCopyMoveTriggered()'

    def onRetargetTriggered(self):
        print 'onRetargetTriggered()'

    def onSearchReplaceTriggered(self):
        print 'onSearchReplaceTriggered()'

    def closeEvent(self, event):
        self.ui_saveSettings()
        event.accept()
