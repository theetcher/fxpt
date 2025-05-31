import maya.cmds as m

from fxpt3.fx_utils.utils import pathToSlash
from fxpt3.qt.pyside import QtGui

from fxpt3.fx_utils.qt_font_creator import QtFontCreator
from fxpt3.fx_utils.utils import getFxUtilsDir
fontFilename = getFxUtilsDir() + '/proggy_tiny_sz.ttf'
qtFontCreator = QtFontCreator(getFxUtilsDir() + '/proggy_tiny_sz.ttf', 12)
FONT_MONOSPACE_QFONT = qtFontCreator.getQFont()
FONT_MONOSPACE_LETTER_SIZE = qtFontCreator.getMaxLetterSize()

FILE_EXISTS_STRINGS = {
    False: (' No', QtGui.QColor(225, 75, 75)),
    True: (' Yes', QtGui.QColor(140, 220, 75))
}

ASSIGNED_COLORS = {
    False: QtGui.QPalette().color(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText),
    True: QtGui.QPalette().color(QtGui.QPalette.Active, QtGui.QPalette.WindowText)
}


# style not finished
TOOLBAR_BUTTON_STYLE = """
QToolButton:checked{
    color: #000000;
    background-color: #5c5c5c;

    border-radius: 3px;
    border-style: dotted;
    border-color: black;
    border-width: 1px;

    margin-top:1px;
    margin-right:1px;
    margin-bottom:1px;
    margin-left:1px;

    padding:3px
}
"""



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


OPT_VAR_NAME = 'fx_textureManager_prefs'
MULTIPLE_STRING = '...multiple...'


def cleanupPath(path):
    return pathToSlash(path.strip()).rstrip('/')
