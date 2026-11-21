import re
import uuid
import webbrowser

import maya.cmds as m
import maya.api.OpenMaya as om

from fxpt3.fx_prefsaver import prefsaver, serializers

SCRIPT_VERSION = 'v1.0'
SCRIPT_NAME = 'FX Renamer'
WIN_NAME = 'fx_renamer_win'
WIN_TITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION
OPT_VAR_NAME = 'fx_renamer_prefs'
UI_LABEL_WIDTH = 100

RENAME_ACTION_SIMPLE_RENAME = 1
RENAME_ACTION_FIND_REPLACE = 2
RENAME_ACTION_PREFIX = 3
RENAME_ACTION_SUFFIX = 4
RENAME_ACTION_NUMBER = 5

SHAPE_PROCESSING_ACCORDING_TO_TRANSFORM = 1
SHAPE_PROCESSING_IGNORE = 2
SHAPE_PROCESSING_AS_ORDINARY_NODE = 3


def isValidMayaName(shortName):
    return bool(re.search(r'^[a-zA-Z_]\w*$', shortName))


def isAllSymbolsValid(s):
    return not bool(re.search(r'\W+', s))


class RenameError(Exception):
    pass


# noinspection PyMethodMayBeStatic
class NodeHandle(object):
    def __init__(self, fullPath):
        selectionList = om.MSelectionList()
        selectionList.add(fullPath)
        self.mObject = selectionList.getDependNode(0)
        self.mObjectHandle = om.MObjectHandle(self.mObject)
        self.isDag = self.mObject.hasFn(om.MFn.kDagNode)
        self.originalName = self.getName()

    def getFullPathName(self):
        if self.isDag:
            return om.MFnDagNode(self.mObject).fullPathName()
        return om.MFnDependencyNode(self.mObject).name()

    def getPathAndName(self):
        splitName = self.getFullPathName().split('|')
        shortName = splitName.pop()
        return '|'.join(splitName), shortName

    def getPath(self):
        return self.getPathAndName()[0]

    def getName(self):
        return self.getPathAndName()[1]

    def isShape(self):
        return self.mObject.hasFn(om.MFn.kShape)

    def isReadOnly(self):
        # shared nodes are Maya's startup nodes (lambert1, time1, persp...), which can't be renamed
        mfn = om.MFnDependencyNode(self.mObject)
        return mfn.isLocked or mfn.isShared or mfn.isFromReferencedFile

    def renameToTempName(self):
        tempName = self.getAvailableName('fx_renamer_tmp_name_' + uuid.uuid4().hex + '_')
        m.rename(self.getFullPathName(), tempName, ignoreShape=True)

    def rename(self, newName, processShapes):
        availableName = self.getAvailableName(newName)
        if processShapes:
            self.processShapes(availableName)
        m.rename(self.getFullPathName(), availableName, ignoreShape=True)

    def processShapes(self, parentShortName):
        parentBaseName, parentIndex = splitIndex(parentShortName)

        shapes = m.listRelatives(self.getFullPathName(), shapes=True, fullPath=True, noIntermediate=True)
        if not shapes:  # case: no shapes
            return

        shapeNodeHandles = [NodeHandle(x) for x in sorted(shapes)]

        for nh in shapeNodeHandles:
            nh.renameToTempName()

        if len(shapeNodeHandles) == 1:  # case: 1 shape -> '<parentName>Shape<parentIndex>'
            shapeNodeHandles[0].rename(parentBaseName + 'Shape' + parentIndex, False)
            return

        # case: more than 1 shape.
        typesDict = {}
        for nh in shapeNodeHandles:
            typesDict.setdefault(m.nodeType(nh.getFullPathName()), []).append(nh)

        for shapeType, nodeHandles in typesDict.items():
            for shapeNumber, nh in enumerate(nodeHandles, 1):
                if len(typesDict) == 1:  # case: all shapes of the same type -> '<parentShortName>_Shape<shapeNumber>'
                    nh.rename(parentShortName + '_Shape' + str(shapeNumber), False)
                else:  # case: shapes of different types -> '<parentShortName>_<shapeType>Shape<shapeNumber>'
                    nh.rename(parentShortName + '_' + shapeType + 'Shape' + str(shapeNumber), False)

    def getAvailableName(self, shortName):
        while self.nameExists(shortName):
            shortName = incrementIndex(shortName)
        return shortName

    def nameExists(self, shortName):
        if self.isDag:
            # DAG names only need to be unique among siblings
            return m.objExists(self.getPath() + '|' + shortName)
        # '|name' never matches a DG node, check the bare name
        return m.objExists(shortName)


def splitIndex(shortName):
    match = re.search(r'(.*\D)(\d*)$', shortName)
    assert match, 'Failed to match anything during split index.'
    return match.group(1), match.group(2)


def incrementIndex(shortName):
    name, index = splitIndex(shortName)
    index = int(index) + 1 if index else 1
    return name + str(index)


def splitNameByNumberingPattern(pattern):
    match = re.search(r'^(\w*)(#*)(.*)$', pattern)
    return match.group(1), match.group(2), match.group(3)


def renameNodes(nodeHandles, newNames, processShapes):
    """Rename all nodes in one undo chunk. On failure, everything done so far is undone, so no node keeps a temp name."""
    m.undoInfo(openChunk=True, chunkName='fx_renamer')
    failure = None
    try:
        for nh in nodeHandles:
            nh.renameToTempName()
        for nh, newName in zip(nodeHandles, newNames):
            nh.rename(newName, processShapes)
    except RuntimeError as e:
        failure = e
    finally:
        m.undoInfo(closeChunk=True)

    if failure is not None:
        m.undo()
        raise RenameError('Rename failed, changes were undone.\n\n{0}'.format(str(failure).strip()))


# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic,PyUnusedLocal
class RenamerUI(object):
    def __init__(self):
        self.ui_createUI()

        self.prefSaver = prefsaver.PrefSaver(serializers.SerializerOptVar(OPT_VAR_NAME))
        self.ui_initSettings()
        self.ui_loadSettings()

    def ui_initSettings(self):
        # control names are the same as in the legacy PyMEL version, so prefs saved by it still match
        self.prefSaver.addControl(self.ui_RADBTNGRP_shapeProcessing, prefsaver.UIType.MRadioButtonGrp3, 1)
        self.prefSaver.addControl(self.ui_TXTFLDGRP_simpleRename, prefsaver.UIType.MTextFieldGrp, '')
        self.prefSaver.addControl(self.ui_TXTFLDGRP_find, prefsaver.UIType.MTextFieldGrp, '')
        self.prefSaver.addControl(self.ui_TXTFLDGRP_replace, prefsaver.UIType.MTextFieldGrp, '')
        self.prefSaver.addControl(self.ui_TXTFLDGRP_prefix, prefsaver.UIType.MTextFieldGrp, '')
        self.prefSaver.addControl(self.ui_TXTFLDGRP_suffix, prefsaver.UIType.MTextFieldGrp, '')
        self.prefSaver.addControl(self.ui_TXTFLDGRP_renameNumber, prefsaver.UIType.MTextFieldGrp, '')
        self.prefSaver.addControl(self.ui_INTFLDGRP_startIndex, prefsaver.UIType.MIntFieldGrp1, [1])
        self.prefSaver.addControl(self.ui_LAY_frameOptions, prefsaver.UIType.MFrameLayout, False)
        self.prefSaver.addControl(self.ui_LAY_frameSimpleRename, prefsaver.UIType.MFrameLayout, False)
        self.prefSaver.addControl(self.ui_LAY_frameFindReplace, prefsaver.UIType.MFrameLayout, False)
        self.prefSaver.addControl(self.ui_LAY_framePrefix, prefsaver.UIType.MFrameLayout, False)
        self.prefSaver.addControl(self.ui_LAY_frameSuffix, prefsaver.UIType.MFrameLayout, False)
        self.prefSaver.addControl(self.ui_LAY_frameRenameNumber, prefsaver.UIType.MFrameLayout, False)

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self, *args):
        # prefs are saved on every change, so closing the window with [X] loses nothing
        if m.window(WIN_NAME, exists=True):
            self.prefSaver.savePrefs()

    def ui_saveSettingsDeferred(self, *args):
        # frameLayout collapse/expand commands: save after the frame state has settled
        m.evalDeferred(self.ui_saveSettings)

    def ui_resetSettings(self, *args):
        self.prefSaver.resetPrefs()
        self.ui_saveSettings()

    def ui_createUI(self):
        # an open window from a previous run() already saved its prefs on every change
        if m.window(WIN_NAME, exists=True):
            m.deleteUI(WIN_NAME, window=True)

        self.window = m.window(
            WIN_NAME,
            title=WIN_TITLE,
            maximizeButton=False,
            menuBar=True,
            menuBarVisible=True
        )

        m.setUITemplate('DefaultTemplate', pushTemplate=True)
        try:
            m.menu(label='Edit', tearOff=False)
            m.menuItem(label='Reset Settings', command=self.ui_resetSettings)
            m.menu(label='Help', tearOff=False)
            m.menuItem(label='Help on ' + WIN_TITLE, command=self.ui_showHelp)

            self.ui_LAY_mainForm = m.formLayout()

            self.ui_TAB_top = m.tabLayout(tabsVisible=False)
            m.tabLayout(self.ui_TAB_top, e=True, height=1)

            self.ui_LAY_attachForm = m.formLayout()

            self.ui_TAB_inner = m.tabLayout(tabsVisible=False, scrollable=True, innerMarginWidth=4)

            self.ui_LAY_mainColumn = m.columnLayout(adjustableColumn=True, rowSpacing=4)

            # --------------------
            self.ui_LAY_frameOptions = self.ui_createFrame('ui_LAY_frameOptions', 'Options')
            m.columnLayout(adjustableColumn=True)
            self.ui_RADBTNGRP_shapeProcessing = m.radioButtonGrp(
                'ui_RADBTNGRP_shapeProcessing',
                label='Shape Processing:',
                labelArray3=["Rename shapes according to it's transforms\n(even if it's not selected)",
                             "Don't rename shapes", 'Treat shapes as ordinary nodes'],
                numberOfRadioButtons=3,
                columnWidth=(1, UI_LABEL_WIDTH),
                columnAttach=(1, 'right', 5),
                vertical=True,
                select=SHAPE_PROCESSING_ACCORDING_TO_TRANSFORM,
                changeCommand=self.ui_saveSettings
            )
            m.setParent(self.ui_LAY_mainColumn)

            # --------------------
            self.ui_LAY_frameSimpleRename = self.ui_createFrame('ui_LAY_frameSimpleRename', 'Rename')
            m.columnLayout(adjustableColumn=True, columnOffset=('both', 2))
            self.ui_TXTFLDGRP_simpleRename = self.ui_createTextFieldGrp('ui_TXTFLDGRP_simpleRename', 'New Name')
            self.ui_createActionButton('Rename', RENAME_ACTION_SIMPLE_RENAME)
            m.separator(style='none', height=2)
            m.setParent(self.ui_LAY_mainColumn)

            # --------------------
            self.ui_LAY_frameFindReplace = self.ui_createFrame('ui_LAY_frameFindReplace', 'Find and Replace')
            m.columnLayout(adjustableColumn=True, columnOffset=('both', 2))
            self.ui_TXTFLDGRP_find = self.ui_createTextFieldGrp('ui_TXTFLDGRP_find', 'Find')
            self.ui_TXTFLDGRP_replace = self.ui_createTextFieldGrp('ui_TXTFLDGRP_replace', 'Replace With')
            self.ui_createActionButton('Find and Replace', RENAME_ACTION_FIND_REPLACE)
            m.setParent(self.ui_LAY_mainColumn)

            # --------------------
            self.ui_LAY_framePrefix = self.ui_createFrame('ui_LAY_framePrefix', 'Add Prefix')
            m.columnLayout(adjustableColumn=True, columnOffset=('both', 2))
            self.ui_TXTFLDGRP_prefix = self.ui_createTextFieldGrp('ui_TXTFLDGRP_prefix', 'Prefix')
            self.ui_createActionButton('Add Prefix', RENAME_ACTION_PREFIX)
            m.setParent(self.ui_LAY_mainColumn)

            # --------------------
            self.ui_LAY_frameSuffix = self.ui_createFrame('ui_LAY_frameSuffix', 'Add Suffix')
            m.columnLayout(adjustableColumn=True, columnOffset=('both', 2))
            self.ui_TXTFLDGRP_suffix = self.ui_createTextFieldGrp('ui_TXTFLDGRP_suffix', 'Suffix')
            self.ui_createActionButton('Add Suffix', RENAME_ACTION_SUFFIX)
            m.setParent(self.ui_LAY_mainColumn)

            # --------------------
            self.ui_LAY_frameRenameNumber = self.ui_createFrame('ui_LAY_frameRenameNumber', 'Rename and Number')
            m.columnLayout(adjustableColumn=True, columnOffset=('both', 2))

            m.frameLayout(
                labelVisible=False,
                collapsable=False,
                marginHeight=3,
                enable=False
            )
            m.columnLayout(adjustableColumn=True, columnOffset=('both', 3))
            helpText = (
                'Type "#" symbol(s) in New Name where you want to place numbering.\n'
                'For example:\n'
                '   pCube#  ->  pCube1, pCube2, ..., pCube15, ...\n'
                '   pCube####  ->  pCube0001, pCube0002, ..., pCube0015, ...\n'
                '   obj_##_a  ->  obj_01_a, obj_02_a, ..., obj_15_a, ...\n'
                'Omitting "#" will result in pattern:\n'
                '   pCube  ->  pCube1, pCube2, ..., pCube15, ...'
            )
            m.text(label=helpText, align='left')
            m.setParent('..')  # columnLayout
            m.setParent('..')  # frameLayout

            m.separator(style='none', height=2)

            self.ui_TXTFLDGRP_renameNumber = self.ui_createTextFieldGrp('ui_TXTFLDGRP_renameNumber', 'New Name')
            self.ui_INTFLDGRP_startIndex = m.intFieldGrp(
                'ui_INTFLDGRP_startIndex',
                label='Start Index',
                columnWidth2=(UI_LABEL_WIDTH, 60),
                columnAttach=(1, 'right', 5),
                value1=1,
                changeCommand=self.ui_saveSettings
            )
            self.ui_createActionButton('Rename and Number', RENAME_ACTION_NUMBER)

            m.setParent(self.ui_LAY_mainForm)

            self.ui_BTN_close = m.button(
                label='Close',
                height=30,
                command=self.ui_close
            )
        finally:
            m.setUITemplate('DefaultTemplate', popTemplate=True)

        m.formLayout(
            self.ui_LAY_attachForm,
            e=True,
            attachForm=[
                (self.ui_TAB_inner, 'top', 0),
                (self.ui_TAB_inner, 'left', 0),
                (self.ui_TAB_inner, 'right', 0),
                (self.ui_TAB_inner, 'bottom', 0),
            ]
        )

        m.formLayout(
            self.ui_LAY_mainForm,
            e=True,
            attachForm=[
                (self.ui_TAB_top, 'top', 0),
                (self.ui_TAB_top, 'left', 0),
                (self.ui_TAB_top, 'right', 0),
                (self.ui_BTN_close, 'left', 5),
                (self.ui_BTN_close, 'bottom', 5),
                (self.ui_BTN_close, 'right', 5),
            ],
            attachControl=[
                (self.ui_TAB_top, 'bottom', 5, self.ui_BTN_close),
            ],
            attachNone=[
                (self.ui_BTN_close, 'top'),
            ]
        )

        m.showWindow(self.window)

    def ui_createFrame(self, name, label):
        return m.frameLayout(
            name,
            label=label,
            collapsable=True,
            collapse=False,
            marginHeight=5,
            collapseCommand=self.ui_saveSettingsDeferred,
            expandCommand=self.ui_saveSettingsDeferred
        )

    def ui_createTextFieldGrp(self, name, label):
        return m.textFieldGrp(
            name,
            label=label,
            columnWidth=(1, UI_LABEL_WIDTH),
            columnAttach=(1, 'right', 5),
            adjustableColumn=2,
            changeCommand=self.ui_saveSettings
        )

    def ui_createActionButton(self, label, action):
        m.separator(style='none', height=2)
        return m.button(
            label=label,
            command=lambda *args: self.ui_onRenameClick(action)
        )

    def getText(self, textFieldGrp):
        return m.textFieldGrp(textFieldGrp, q=True, text=True).strip()

    def getShapeProcessing(self):
        return m.radioButtonGrp(self.ui_RADBTNGRP_shapeProcessing, q=True, select=True)

    def ui_onRenameClick(self, action):
        self.ui_saveSettings()

        shapeProcessing = self.getShapeProcessing()
        nodeHandles = self.getNodeHandlesOfSelectedNodes(shapeProcessing)
        if not nodeHandles:
            m.warning('{0}: nothing to rename. Select nodes that are not locked, referenced or read-only.'.format(SCRIPT_NAME))
            return

        newNames = self.getNewNames(action, nodeHandles)
        if newNames is None:
            return

        invalidNames = [n for n in newNames if not isValidMayaName(n)]
        if invalidNames:
            self.ui_error('The result is not a valid Maya name: "{0}".'.format(invalidNames[0]))
            return

        try:
            renameNodes(nodeHandles, newNames, shapeProcessing == SHAPE_PROCESSING_ACCORDING_TO_TRANSFORM)
        except RenameError as e:
            self.ui_error(str(e))

    def getNewNames(self, action, nodeHandles):
        """Returns a new name for each node handle, or None (after showing an error) if the input is invalid."""
        if action == RENAME_ACTION_SIMPLE_RENAME:
            newName = self.getText(self.ui_TXTFLDGRP_simpleRename)
            if not newName:
                return self.ui_error('"New Name" field is empty.')
            if not isValidMayaName(newName):
                return self.ui_error('"New Name" field contains an invalid Maya name.')
            return [newName] * len(nodeHandles)

        if action == RENAME_ACTION_FIND_REPLACE:
            findStr = self.getText(self.ui_TXTFLDGRP_find)
            replaceStr = self.getText(self.ui_TXTFLDGRP_replace)
            if not findStr:
                return self.ui_error('"Find" field is empty.')
            if not isAllSymbolsValid(replaceStr):
                return self.ui_error('"Replace With" field contains an invalid Maya symbol(s).')
            try:
                regex = re.compile(findStr)
                return [regex.sub(replaceStr, nh.originalName) for nh in nodeHandles]
            except re.error as e:
                return self.ui_error('"Find" field is not a valid regular expression:\n{0}'.format(e))

        if action == RENAME_ACTION_PREFIX:
            prefixStr = self.getText(self.ui_TXTFLDGRP_prefix)
            if not prefixStr:
                return self.ui_error('"Prefix" field is empty.')
            if not isAllSymbolsValid(prefixStr):
                return self.ui_error('"Prefix" field contains an invalid Maya symbol(s).')
            return [prefixStr + nh.originalName for nh in nodeHandles]

        if action == RENAME_ACTION_SUFFIX:
            suffixStr = self.getText(self.ui_TXTFLDGRP_suffix)
            if not suffixStr:
                return self.ui_error('"Suffix" field is empty.')
            if not isAllSymbolsValid(suffixStr):
                return self.ui_error('"Suffix" field contains an invalid Maya symbol(s).')
            return [nh.originalName + suffixStr for nh in nodeHandles]

        if action == RENAME_ACTION_NUMBER:
            pattern = self.getText(self.ui_TXTFLDGRP_renameNumber)
            if not pattern:
                return self.ui_error('"New Name" field is empty.')
            head, hashes, tail = splitNameByNumberingPattern(pattern)
            if not isAllSymbolsValid(head) or not isAllSymbolsValid(tail):
                return self.ui_error('"New Name" field contains an invalid Maya symbol(s).')
            startIndex = m.intFieldGrp(self.ui_INTFLDGRP_startIndex, q=True, value1=True)
            padding = len(hashes)
            return [head + str(i).rjust(padding, '0') + tail for i in range(startIndex, startIndex + len(nodeHandles))]

        assert False, 'unknown action id.'

    def ui_error(self, text):
        m.confirmDialog(
            title='Error',
            icon='critical',
            message=text,
            button='Close',
            defaultButton='Close',
            cancelButton='Close'
        )

    def getNodeHandlesOfSelectedNodes(self, shapeProcessing):
        returnList = []
        for fullNodeName in m.ls(sl=True, long=True) or []:
            if '.' in fullNodeName:  # components, plugs
                continue
            nh = NodeHandle(fullNodeName)
            if nh.isReadOnly() or (nh.isShape() and shapeProcessing != SHAPE_PROCESSING_AS_ORDINARY_NODE):
                continue
            returnList.append(nh)
        return returnList

    def ui_close(self, *args):
        if m.window(WIN_NAME, exists=True):
            self.ui_saveSettings()
            m.deleteUI(WIN_NAME, window=True)

    def ui_showHelp(self, *args):
        webbrowser.open('http://davydenko.info/renamer/', new=0, autoraise=True)


def run():
    RenamerUI()
