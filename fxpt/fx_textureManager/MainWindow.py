from PySide import QtCore, QtGui

from fxpt.fx_utils.qtFontCreator import QtFontCreator
from fxpt.fx_utils.utils import getFxUtilsDir

from fxpt.fx_textureManager.MainWindowUI import Ui_MainWindow
from fxpt.fx_textureManager.Harvesters import MayaSceneHarvester

from fxpt.fx_prefsaver import PrefSaver, Serializers

qtFontCreator = QtFontCreator(getFxUtilsDir() + '/proggy_tiny_sz.ttf', 12)
FONT_MONOSPACE_QFONT = qtFontCreator.getQFont()
FONT_MONOSPACE_LETTER_SIZE = qtFontCreator.getLetterSize('i')

TABLE_COLUMN_NAMES = ('Attribute', 'Filename', 'Exists')
TABLE_MAX_COLUMN_SIZE = (50, 100, 10)
TABLE_COLUMN_RIGHT_OFFSET = 20
TABLE_HEADER_TITLE_OFFSET = 2

FILE_EXISTS_STRINGS = {
    False: ('No', QtGui.QColor(225, 75, 75)),
    True: ('Yes', QtGui.QColor(140, 220, 75))
}


OPT_VAR_NAME = 'fx_textureManager_prefs'


class TexManagerUI(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(TexManagerUI, self).__init__(parent=parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.harvester = MayaSceneHarvester()

        self.model = QtGui.QStandardItemModel()
        self.ui.uiTBL_textures.setModel(self.model)

        self.fillTable()

        self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerOptVar(OPT_VAR_NAME))
        self.ui_initSettings()
        self.ui_loadSettings()

    def ui_initSettings(self):
        self.prefSaver.addControl(self, PrefSaver.UIType.PYSIDEWindow, (100, 100, 900, 600))

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    def ui_resetSettings(self):
        self.prefSaver.resetPrefs()

    def fillTable(self):

        self.model.clear()
        self.model.setRowCount(0)
        self.model.setColumnCount(len(TABLE_COLUMN_NAMES))
        for i, col in enumerate(TABLE_COLUMN_NAMES):
            self.model.setHeaderData(i, QtCore.Qt.Horizontal, col, QtCore.Qt.DisplayRole)

        texNodes = self.harvester.getTexNodes()

        self.model.insertRows(0, len(texNodes))

        for i, tn in enumerate(texNodes):

            print tn

            modelIndex = self.model.index(i, 0)
            self.model.setData(modelIndex, tn.getFullAttrName())
            self.model.setData(modelIndex, tn, QtCore.Qt.UserRole)

            modelIndex = self.model.index(i, 1)
            self.model.setData(modelIndex, tn.getAttrValue())

            modelIndex = self.model.index(i, 2)
            fileExists = tn.fileExists()
            self.model.setData(modelIndex, FILE_EXISTS_STRINGS[fileExists][0])
            self.model.setData(modelIndex, FILE_EXISTS_STRINGS[fileExists][1], QtCore.Qt.ForegroundRole)

        self.setTableProps()

    def setTableProps(self):
        table = self.ui.uiTBL_textures
        table.setFont(FONT_MONOSPACE_QFONT)
        table.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)

        # custom "resize to fit" section, cause standard table.resizeColumnsToContents() may be very slow on huge data
        model = table.model()
        columnCount = model.columnCount()
        for col in range(columnCount):
            stringLengths = [len(model.index(row, col).data(QtCore.Qt.DisplayRole)) for row in range(model.rowCount())]
            stringLengths.append(len(str(model.headerData(col, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole))) + TABLE_HEADER_TITLE_OFFSET)
            columnMaxLength = min(max(stringLengths), TABLE_MAX_COLUMN_SIZE[col])
            table.horizontalHeader().resizeSection(col, columnMaxLength * FONT_MONOSPACE_LETTER_SIZE + TABLE_COLUMN_RIGHT_OFFSET)

    def closeEvent(self, event):
        self.ui_saveSettings()
        event.accept()
