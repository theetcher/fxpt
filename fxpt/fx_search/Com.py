import os
from PySide import QtGui
import maya.OpenMaya as om
import maya.cmds as m

OPT_VAR_PREFIX = 'fx_search_'
OPT_VAR_CURRENT_TAB = OPT_VAR_PREFIX + 'currentTabName'

SCRIPT_DIR = os.path.dirname(__file__)

FONT_MONOSPACE_FILENAME = SCRIPT_DIR + '\\proggy_tiny_sz.ttf'
FONT_MONOSPACE_SIZE = 12


def fontFromFile(filename):
    fontID = QtGui.QFontDatabase.addApplicationFont(filename)
    fontFamily = QtGui.QFontDatabase.applicationFontFamilies(fontID)[0]
    return QtGui.QFont(fontFamily, FONT_MONOSPACE_SIZE)


FONT_MONOSPACE_QFONT = fontFromFile(FONT_MONOSPACE_FILENAME)
FONT_MONOSPACE_LETTER_SIZE = QtGui.QFontMetrics(FONT_MONOSPACE_QFONT).width('i')

CHECKED_BUTTON_STYLE = 'QPushButton:checked {color: #000000; background-color: #ffae00}'

SEARCH_STATE_WELCOME = 1
SEARCH_STATE_SEARCHING = 2
SEARCH_STATE_NOTHING_FOUND = 3
SEARCH_STATE_RESULTS = 4

TABLE_MAX_COLUMN_SIZE = 50
TABLE_COLUMN_RIGHT_OFFSET = 20
TABLE_HEADER_TITLE_OFFSET = 2


def isShape(fullPathName):
    selectionList = om.MSelectionList()
    mObject = om.MObject()
    selectionList.add(fullPathName)
    selectionList.getDependNode(0, mObject)
    return bool(mObject.hasFn(om.MFn.kShape))


def shapesOf(fullPathName):
    return m.listRelatives(fullPathName, shapes=True, fullPath=True, noIntermediate=True)


def parentsOf(fullPathName):
    return m.listRelatives(fullPathName, parent=True, fullPath=True)


def splitName(fullPathName):
    splittedName = fullPathName.split('|')
    shortName = splittedName.pop()
    path = '|'.join(splittedName)
    return shortName, path


def shortNameOf(fullPathName):
    return splitName(fullPathName)[0]


def pathOf(fullPathName):
    return splitName(fullPathName)[1]


def typeOf(fullPathName):
    return m.ls(fullPathName, showType=True)[1]


def attrExists(node, attr):
    return bool(m.attributeQuery(attr, node=node, exists=True))


def getNodeTypeString(fullPathName):
    typ = m.nodeType(fullPathName)
    if not isShape(fullPathName):
        shapes = m.listRelatives(fullPathName, shapes=True, fullPath=True, noIntermediate=True)
        if shapes:
            types = set([m.nodeType(x) for x in shapes])
            typ += ', ' + ', '.join(types)
    return typ
