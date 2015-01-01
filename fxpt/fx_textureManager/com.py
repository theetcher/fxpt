import os
from PySide import QtGui

SCRIPT_DIR = os.path.dirname(__file__)

FONT_MONOSPACE_FILENAME = SCRIPT_DIR + '\\proggy_tiny_sz.ttf'
FONT_MONOSPACE_SIZE = 12


def fontFromFile(filename):
    fontID = QtGui.QFontDatabase.addApplicationFont(filename)
    fontFamily = QtGui.QFontDatabase.applicationFontFamilies(fontID)[0]
    return QtGui.QFont(fontFamily, FONT_MONOSPACE_SIZE)


FONT_MONOSPACE_QFONT = fontFromFile(FONT_MONOSPACE_FILENAME)
FONT_MONOSPACE_LETTER_SIZE = QtGui.QFontMetrics(FONT_MONOSPACE_QFONT).width('i')