import maya.OpenMaya as om
import maya.cmds as m

from fxpt.fx_utils.qtFontCreator import QtFontCreator
from fxpt.fx_utils.utils import getFxUtilsDir

OPT_VAR_PREFIX = 'fx_search_'
OPT_VAR_CURRENT_TAB = OPT_VAR_PREFIX + 'currentTabName'

qtFontCreator = QtFontCreator(getFxUtilsDir() + '/proggy_tiny_sz.ttf', 12)
FONT_MONOSPACE_QFONT = qtFontCreator.getQFont()
FONT_MONOSPACE_LETTER_SIZE = qtFontCreator.getLetterSize('i')


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
    # return m.ls(fullPathName, showType=True)[1]
    return m.nodeType(fullPathName)


def attrExists(node, attr):
    return bool(m.attributeQuery(attr, node=node, exists=True))


def getNodeTypeString(fullPathName):
    typ = typeOf(fullPathName)
    if not isShape(fullPathName):
        shapes = m.listRelatives(fullPathName, shapes=True, fullPath=True, noIntermediate=True)
        if shapes:
            types = set([typeOf(x) for x in shapes])
            typ += ', ' + ', '.join(types)
    return typ
