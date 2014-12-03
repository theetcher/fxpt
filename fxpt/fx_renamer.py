#region imports
import re
import uuid
import maya.cmds as m
import maya.OpenMaya as om
import pymel.core as pm

from fxpt.fx_prefsaver import PrefSaver, Serializers
#endregion imports

#region constants
SCRIPT_VERSION = 'v1.0'
SCRIPT_NAME = 'FX Renamer'
WIN_NAME = 'fx_renamer_win'
WIN_HELPNAME = 'fx_renamer_helpwin'
WIN_TITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION
WIN_HELPTITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION + ' Help'
OPT_VAR_NAME = 'fx_renamer_prefs'
UI_LABEL_WIDTH = 100
UI_INPUT_WIDTH = 240

RENAME_ACTION_SIMPLE_RENAME = 1
RENAME_ACTION_FIND_REPLACE = 2
RENAME_ACTION_PREFIX = 3
RENAME_ACTION_SUFFIX = 4
RENAME_ACTION_NUMBER = 5

SHAPE_PROCESSING_ACCORDING_TO_TRANSFORM = 1
SHAPE_PROCESSING_IGNORE = 2
SHAPE_PROCESSING_AS_ORDINARY_NODE = 3
#endregion constants

#TODO: help windows


def isValidMayaName(shortName):
    return bool(re.search(r'^[a-zA-Z_]\w*$', shortName))


def isAllSymbolsValid(s):
    return not bool(re.search(r'\W+', s))


# noinspection PyMethodMayBeStatic
class NodeHandle():
    def __init__(self, fullPath):
        self.mObject = self.fullPathToMObject(fullPath)
        self.originalName = self.getName()

    def fullPathToMObject(self, fullPath):
        selectionList = om.MSelectionList()
        mObject = om.MObject()
        selectionList.add(fullPath)
        selectionList.getDependNode(0, mObject)
        return mObject

    def mObjectToFullPath(self, mObject):
        if self.mObject.hasFn(om.MFn.kDagNode):
            mfn = om.MFnDagNode()
            mfn.setObject(mObject)
            return str(mfn.fullPathName())
        else:
            mfn = om.MFnDependencyNode()
            mfn.setObject(mObject)
            return str(mfn.name())

    def renameToTempName(self):
        uid = str(uuid.uuid4().hex)
        tempName = self.getAvailableName('fx_renamer_tmp_name_' + uid + '_')
        m.rename(self.getFullPathName(), tempName, ignoreShape=True)

    def rename(self, rd):
        newName = self.getNewNameFromRenameDesc(rd)
        availableName = self.getAvailableName(newName)
        if rd.shapeProcessing == SHAPE_PROCESSING_ACCORDING_TO_TRANSFORM:
            self.processShapes(availableName)
        m.rename(self.getFullPathName(), availableName, ignoreShape=True)

    def getNewNameFromRenameDesc(self, rd):
        if rd.action == RENAME_ACTION_SIMPLE_RENAME:
            return rd.simpleNameStr
        if rd.action == RENAME_ACTION_FIND_REPLACE:
            return re.sub(rd.findStr, rd.replaceStr, self.originalName)
        if rd.action == RENAME_ACTION_PREFIX:
            return rd.prefixStr + self.originalName
        if rd.action == RENAME_ACTION_SUFFIX:
            return self.originalName + rd.suffixStr
        else:
            assert False, 'unknown action id.'

    def processShapes(self, parentShortName):
        fullPathName = self.getFullPathName()
        parentBaseName, parentIndex = self.splitIndex(parentShortName)

        shapes = m.listRelatives(fullPathName, shapes=True, fullPath=True, noIntermediate=True)
        if not shapes:  # case: no shapes
            return

        shapeNodeHandles = [NodeHandle(x) for x in sorted(shapes)]

        for nh in shapeNodeHandles:
            nh.renameToTempName()

        if len(shapeNodeHandles) == 1:  # case: 1 shape -> '<parentName>Shape<parentIndex>'
            rd = self.getSimpleRenameDesc(parentBaseName + 'Shape' + parentIndex)
            shapeNodeHandles[0].rename(rd)

        else:  # case: more than 1 shape.
            typesDict = {}
            for nh in shapeNodeHandles:
                nType = self.getNodeType(nh.getFullPathName())
                if nType in typesDict:
                    typesDict[nType].append(nh)
                else:
                    typesDict[nType] = [nh]

            for shapeType, nodeHandles in typesDict.items():
                for nh, shapeNumber in zip(nodeHandles, range(1, len(nodeHandles) + 1)):
                    if len(typesDict) == 1:  # case: all shapes of the same type -> '<parentShortName>_Shape<shapeNumber>'
                        rd = self.getSimpleRenameDesc(parentShortName + '_' + 'Shape' + str(shapeNumber))
                    else:  # case: shapes of different types -> '<parentShortName>_<shapeType>Shape<shapeNumber>'
                        rd = self.getSimpleRenameDesc(parentShortName + '_' + shapeType + 'Shape' + str(shapeNumber))
                    nh.rename(rd)

    def getFullPathName(self):
        return self.mObjectToFullPath(self.mObject)

    def getPathAndName(self):
        fullPath = self.mObjectToFullPath(self.mObject)
        splittedName = fullPath.split('|')
        shortName = splittedName.pop()
        return '|'.join(splittedName), shortName

    def getPath(self):
        return self.getPathAndName()[0]

    def getName(self):
        return self.getPathAndName()[1]

    def isShape(self):
        selectionList = om.MSelectionList()
        mObject = om.MObject()
        selectionList.add(self.getFullPathName())
        selectionList.getDependNode(0, mObject)
        return mObject.hasFn(om.MFn.kShape)

    def isReadOnly(self):
        return m.lockNode(self.getFullPathName(), q=True)[0]

    def getAvailableName(self, shortName):
        while m.objExists(self.joinName((self.getPath(), shortName))):
            shortName = self.incrementIndex(shortName)
        return shortName

    def incrementIndex(self, shortName):
        name, index = self.splitIndex(shortName)
        if index:
            index = int(index) + 1
        else:
            index = 1
        return name + str(index)

    def splitIndex(self, shortName):
        match = re.search(r'(.*\D)(\d*)$', shortName)
        assert match, 'Failed to match anything during split index.'
        return match.group(1), match.group(2)

    def joinName(self, lst):
        return '|'.join(lst)

    def getNodeType(self, fullPathName):
        return m.ls(fullPathName, showType=True)[1]

    def getSimpleRenameDesc(self, newName):
        rd = RenameDesc()
        rd.action = RENAME_ACTION_SIMPLE_RENAME
        rd.shapeProcessing = SHAPE_PROCESSING_AS_ORDINARY_NODE
        rd.simpleNameStr = newName
        return rd


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


class RenameDesc():
    def __init__(self):
        self.action = None
        self.simpleNameStr = None
        self.findStr = None
        self.replaceStr = None
        self.prefixStr = None
        self.suffixStr = None
        self.shapeProcessing = None


# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic
class RenamerUI():
    def __init__(self):
        self.optionVarLinks = []
        self.ui_createUI()

        self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerOptVar(OPT_VAR_NAME))
        self.ui_initSettings()
        self.ui_loadSettings()

    # noinspection PyMethodMayBeStatic
    def ui_initSettings(self):
        self.prefSaver.addControl(self.ui_RADBTNGRP_shapeProcessing, PrefSaver.UIType.PMRadioButtonGrp3, 1)
        self.prefSaver.addControl(self.ui_TXTFLDGRP_simpleRename, PrefSaver.UIType.PMTextFieldGrp, '')
        self.prefSaver.addControl(self.ui_TXTFLDGRP_find, PrefSaver.UIType.PMTextFieldGrp, '')
        self.prefSaver.addControl(self.ui_TXTFLDGRP_replace, PrefSaver.UIType.PMTextFieldGrp, '')
        self.prefSaver.addControl(self.ui_TXTFLDGRP_prefix, PrefSaver.UIType.PMTextFieldGrp, '')
        self.prefSaver.addControl(self.ui_TXTFLDGRP_suffix, PrefSaver.UIType.PMTextFieldGrp, '')
        self.prefSaver.addControl(self.ui_TXTFLDGRP_renameNumber, PrefSaver.UIType.PMTextFieldGrp, '')
        self.prefSaver.addControl(self.ui_INTFLDGRP_startIndex, PrefSaver.UIType.PMIntFieldGrp1, [1])
        self.prefSaver.addControl(self.ui_LAY_frameOptions, PrefSaver.UIType.PMFrameLayout, False)
        self.prefSaver.addControl(self.ui_LAY_frameSimpleRename, PrefSaver.UIType.PMFrameLayout, False)
        self.prefSaver.addControl(self.ui_LAY_frameFindReplace, PrefSaver.UIType.PMFrameLayout, False)
        self.prefSaver.addControl(self.ui_LAY_framePrefix, PrefSaver.UIType.PMFrameLayout, False)
        self.prefSaver.addControl(self.ui_LAY_frameSuffix, PrefSaver.UIType.PMFrameLayout, False)
        self.prefSaver.addControl(self.ui_LAY_frameRenameNumber, PrefSaver.UIType.PMFrameLayout, False)

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    # noinspection PyUnusedLocal
    def ui_resetSettings(self, *args, **kwargs):
        self.prefSaver.resetPrefs()

    def ui_createUI(self):
        self.winName = WIN_NAME
        self.winTitle = WIN_TITLE

        if pm.window(WIN_NAME, exists=True):
            pm.deleteUI(WIN_NAME, window=True)

        self.window = pm.window(
            WIN_NAME,
            title=WIN_TITLE,
            maximizeButton=False,
            menuBar=True,
            menuBarVisible=True
        )

        pm.menu(label='Edit', tearOff=False)
        pm.menuItem(label='Reset Settings', command=self.ui_resetSettings)
        pm.menu(label='Help', tearOff=False)
        pm.menuItem(label='Help on ' + WIN_TITLE, command=pm.Callback(self.ui_showHelp, 1))
        pm.menuItem(divider=True)
        pm.menuItem(label='Script Information', command=pm.Callback(self.ui_showHelp, 2))

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_LAY_mainForm = pm.formLayout()

        self.ui_LAY_mainScroll = pm.scrollLayout(
            childResizable=True
        )

        self.ui_LAY_mainColumn = pm.columnLayout(adjustableColumn=True)

        # - - - "Options" frame - - -

        self.ui_LAY_frameOptions = pm.frameLayout(
            'ui_LAY_frameOptions',
            label='Options',
            collapsable=True,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True
        )

        pm.columnLayout(adjustableColumn=True, columnOffset=('both', 2))

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_RADBTNGRP_shapeProcessing = pm.radioButtonGrp(
            'ui_RADBTNGRP_shapeProcessing',
            label='Shape Processing:',
            labelArray3=["Rename shapes according to it's transforms\n(even if it's not selected)",
                         "Don't rename shapes", 'Treat shapes as ordinary nodes'],
            numberOfRadioButtons=3,
            columnWidth=[1, UI_LABEL_WIDTH],
            columnAttach=[1, 'right', 5],
            vertical=True,
            select=SHAPE_PROCESSING_ACCORDING_TO_TRANSFORM
        )

        pm.separator(style='none', height=2)

        pm.setParent(self.ui_LAY_mainColumn)

        # - - - "Rename" frame - - -

        self.ui_LAY_frameSimpleRename = pm.frameLayout(
            'ui_LAY_frameSimpleRename',
            label='Rename',
            collapsable=True,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True
        )

        pm.columnLayout(adjustableColumn=True, columnOffset=('both', 2))

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_TXTFLDGRP_simpleRename = pm.textFieldGrp(
            'ui_TXTFLDGRP_simpleRename',
            label='New Name',
            columnWidth=[1, UI_LABEL_WIDTH],
            columnAttach=[1, 'right', 5],
            adjustableColumn=2
        )

        pm.separator(style='none', height=2)

        self.ui_BTN_simpleRename = pm.button(
            label='Rename',
            command=pm.Callback(self.ui_onRenameClick, RENAME_ACTION_SIMPLE_RENAME)
        )

        pm.setParent(self.ui_LAY_mainColumn)

        # - - - "Find and Replace" frame - - -

        self.ui_LAY_frameFindReplace = pm.frameLayout(
            'ui_LAY_frameFindReplace',
            label='Find and Replace',
            collapsable=True,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True
        )

        pm.columnLayout(adjustableColumn=True, columnOffset=('both', 2))

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_TXTFLDGRP_find = pm.textFieldGrp(
            'ui_TXTFLDGRP_find',
            label='Find',
            columnWidth=[1, UI_LABEL_WIDTH],
            columnAttach=[1, 'right', 5],
            adjustableColumn=2
        )

        self.ui_TXTFLDGRP_replace = pm.textFieldGrp(
            'ui_TXTFLDGRP_replace',
            label='Replace With',
            columnWidth=[1, UI_LABEL_WIDTH],
            columnAttach=[1, 'right', 5],
            adjustableColumn=2
        )

        pm.separator(style='none', height=2)

        self.ui_BTN_findReplace = pm.button(
            label='Find and Replace',
            command=pm.Callback(self.ui_onRenameClick, RENAME_ACTION_FIND_REPLACE)
        )

        pm.setParent(self.ui_LAY_mainColumn)

        # - - - "Add Prefix" frame - - -

        self.ui_LAY_framePrefix = pm.frameLayout(
            'ui_LAY_framePrefix',
            label='Add Prefix',
            collapsable=True,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True
        )

        pm.columnLayout(adjustableColumn=True, columnOffset=('both', 2))

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_TXTFLDGRP_prefix = pm.textFieldGrp(
            'ui_TXTFLDGRP_prefix',
            label='Prefix',
            columnWidth=[1, UI_LABEL_WIDTH],
            columnAttach=[1, 'right', 5],
            adjustableColumn=2
        )

        pm.separator(style='none', height=2)

        self.ui_BTN_prefix = pm.button(
            label='Add Prefix',
            command=pm.Callback(self.ui_onRenameClick, RENAME_ACTION_PREFIX)
        )

        pm.setParent(self.ui_LAY_mainColumn)

        # - - - "Add Suffix" frame - - -

        self.ui_LAY_frameSuffix = pm.frameLayout(
            'ui_LAY_frameSuffix',
            label='Add Suffix',
            collapsable=True,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True
        )

        pm.columnLayout(adjustableColumn=True, columnOffset=('both', 2))

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_TXTFLDGRP_suffix = pm.textFieldGrp(
            'ui_TXTFLDGRP_suffix',
            label='Suffix',
            columnWidth=[1, UI_LABEL_WIDTH],
            columnAttach=[1, 'right', 5],
            adjustableColumn=2
        )

        pm.separator(style='none', height=2)

        self.ui_BTN_prefix = pm.button(
            label='Add Suffix',
            command=pm.Callback(self.ui_onRenameClick, RENAME_ACTION_SUFFIX)
        )

        pm.setParent(self.ui_LAY_mainColumn)

        # - - - "Rename and Number" frame - - -

        self.ui_LAY_frameRenameNumber = pm.frameLayout(
            'ui_LAY_frameRenameNumber',
            label='Rename and Number',
            collapsable=True,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True
        )

        localColumn = pm.columnLayout(adjustableColumn=True, columnOffset=('both', 2))

        # - - - - - - - - - - - - - - - - - - - -

        pm.frameLayout(
            labelVisible=False,
            collapsable=False,
            marginHeight=3,
            borderStyle='in',
            borderVisible=True,
            enable=False
        )
        pm.columnLayout(adjustableColumn=True, columnOffset=('both', 3))
        helpText = ''
        helpText += 'Type "#" symbol(s) in New Name where you want to place numbering.\n'
        helpText += 'For example:\n'
        helpText += '   pCube#  ->  pCube1, pCube2, ..., pCube15, ...\n'
        helpText += '   pCube####  ->  pCube0001, pCube0002, ..., pCube0015, ...\n'
        helpText += '   obj_##_a  ->  obj_01_a, obj_02_a, ..., obj_15_a, ...\n'
        helpText += 'Omitting "#" will result in pattern:\n'
        helpText += '   pCube  ->  pCube1, pCube2, ..., pCube15, ...'
        self.ui_TXT_help = pm.text(helpText, align='left')

        pm.setParent(localColumn)

        pm.separator(style='none', height=2)

        self.ui_TXTFLDGRP_renameNumber = pm.textFieldGrp(
            'ui_TXTFLDGRP_renameNumber',
            label='New Name',
            columnWidth=[1, UI_LABEL_WIDTH],
            columnAttach=[1, 'right', 5],
            adjustableColumn=2
        )

        self.ui_INTFLDGRP_startIndex = pm.intFieldGrp(
            'ui_INTFLDGRP_startIndex',
            label='Start Index',
            columnWidth2=[UI_LABEL_WIDTH, 60],
            columnAttach=[1, 'right', 5]
        )

        pm.separator(style='none', height=2)

        self.ui_BTN_prefix = pm.button(
            label='Rename and Number',
            command=pm.Callback(self.ui_onRenameClick, RENAME_ACTION_NUMBER)
        )

        pm.setParent(self.ui_LAY_mainColumn)

        # - - - END OF ALL FRAMES - - -

        pm.setParent(self.ui_LAY_mainForm)

        self.ui_BTN_close = pm.button(
            label='Close',
            height=30,
            command=self.ui_close
        )

        # - - - - - Organize Main Form Layout - - - - -

        self.ui_LAY_mainForm.attachForm(self.ui_LAY_mainScroll, 'top', 2)
        self.ui_LAY_mainForm.attachForm(self.ui_LAY_mainScroll, 'left', 2)
        self.ui_LAY_mainForm.attachForm(self.ui_LAY_mainScroll, 'right', 2)
        self.ui_LAY_mainForm.attachControl(self.ui_LAY_mainScroll, 'bottom', 2, self.ui_BTN_close)

        self.ui_LAY_mainForm.attachNone(self.ui_BTN_close, 'top')
        self.ui_LAY_mainForm.attachForm(self.ui_BTN_close, 'left', 2)
        self.ui_LAY_mainForm.attachForm(self.ui_BTN_close, 'right', 2)
        self.ui_LAY_mainForm.attachForm(self.ui_BTN_close, 'bottom', 2)

        ################## UI Creation  Finished ################

        #        scriptJob(uid = [self.window, self.ui_close] )

        self.window.show()
        pm.refresh()

    def ui_onRenameClick(self, action):

        nodeHandles = self.getNodeHandlesOfSelectedNodes()
        if not nodeHandles:
            return

        if action != RENAME_ACTION_NUMBER:

            rd = RenameDesc()
            rd.action = action
            rd.shapeProcessing = self.ui_RADBTNGRP_shapeProcessing.getSelect()
            rd.simpleNameStr = self.ui_TXTFLDGRP_simpleRename.getText().strip()
            rd.findStr = self.ui_TXTFLDGRP_find.getText().strip()
            rd.replaceStr = self.ui_TXTFLDGRP_replace.getText().strip()
            rd.prefixStr = self.ui_TXTFLDGRP_prefix.getText().strip()
            rd.suffixStr = self.ui_TXTFLDGRP_suffix.getText().strip()

            if action == RENAME_ACTION_SIMPLE_RENAME:
                if not rd.simpleNameStr:
                    self.ui_errorInvalidSymbols('"New Name" field is empty.')
                    return
                elif not isValidMayaName(rd.simpleNameStr):
                    self.ui_errorInvalidSymbols('"New Name" field contains an invalid Maya name.')
                    return
            if action == RENAME_ACTION_FIND_REPLACE:
                if not rd.findStr:
                    self.ui_errorInvalidSymbols('"Find" field is empty.')
                    return
                elif not isAllSymbolsValid(rd.replaceStr):
                    self.ui_errorInvalidSymbols('"Replace With" field contains an invalid Maya symbol(s).')
                    return
            if action == RENAME_ACTION_PREFIX:
                if not rd.prefixStr:
                    self.ui_errorInvalidSymbols('"Prefix" field is empty.')
                    return
                elif not isAllSymbolsValid(rd.prefixStr):
                    self.ui_errorInvalidSymbols('"Prefix" field contains an invalid Maya symbol(s).')
                    return
            if action == RENAME_ACTION_SUFFIX:
                if not rd.suffixStr:
                    self.ui_errorInvalidSymbols('"Suffix" field is empty.')
                    return
                elif not isAllSymbolsValid(rd.suffixStr):
                    self.ui_errorInvalidSymbols('"Suffix" field contains an invalid Maya symbol(s).')
                    return

            for nh in nodeHandles:
                nh.renameToTempName()

            for nh in nodeHandles:
                nh.rename(rd)

        elif action == RENAME_ACTION_NUMBER:
            pattern = self.ui_TXTFLDGRP_renameNumber.getText().strip()
            if not pattern:
                self.ui_errorInvalidSymbols('"New Name" field is empty.')
                return

            splittedName = self.getSplittedNameByNumberingPattern(pattern)
            if not isAllSymbolsValid(splittedName[0]) or not isAllSymbolsValid(splittedName[2]):
                self.ui_errorInvalidSymbols('"New Name" field contains an invalid Maya symbol(s).')
                return

            padding = len(splittedName[1])

            rd = RenameDesc()
            rd.action = RENAME_ACTION_SIMPLE_RENAME
            rd.shapeProcessing = self.ui_RADBTNGRP_shapeProcessing.getSelect()

            for nh in nodeHandles:
                nh.renameToTempName()

            i = self.ui_INTFLDGRP_startIndex.getValue1()
            for nh in nodeHandles:
                rd.simpleNameStr = splittedName[0] + ('{0:0>' + str(padding) + '}').format(str(i)) + splittedName[2]
                nh.rename(rd)
                i += 1

        else:
            assert False, 'unknown action id.'

    def ui_errorInvalidSymbols(self, text):
        m.confirmDialog(
            title='Error',
            icon='critical',
            message=text,
            button='Close',
            defaultButton='Close',
            cancelButton='Close'
        )

    def getSplittedNameByNumberingPattern(self, pattern):
        match = re.search(r'^(\w*)(#*)(.*)$', pattern)
        return match.group(1), match.group(2), match.group(3)

    def getNodeHandlesOfSelectedNodes(self):
        selectedNodes = m.ls(sl=True, l=True)
        returnList = []
        for fullNodeName in selectedNodes:
            nh = NodeHandle(fullNodeName)
            if nh.isReadOnly() or (nh.isShape() and (not self.shapesAsOrdinaryNodes())):
                continue
            returnList.append(nh)
        return returnList

    def shapesAsOrdinaryNodes(self):
        return bool(self.ui_RADBTNGRP_shapeProcessing.getSelect() == SHAPE_PROCESSING_AS_ORDINARY_NODE)

    # noinspection PyUnusedLocal
    def ui_close(self, *args):
        self.ui_saveSettings()
        if pm.window(WIN_NAME, exists=True):
            pm.deleteUI(WIN_NAME, window=True)

    # noinspection PyUnusedLocal
    def ui_showHelp(self, tab, *args):

        ################# UI Creation ################

        if pm.window(WIN_HELPNAME, exists=True):
            pm.deleteUI(WIN_HELPNAME, window=True)

        self.helpWindow = pm.window(
            WIN_HELPNAME,
            title=WIN_HELPTITLE,
            maximizeButton=False
        )

        self.ui_LAY_formMainHelp = pm.formLayout()

        self.ui_LAY_tabHelp = pm.tabLayout(
            innerMarginWidth=50,
            innerMarginHeight=50,
            childResizable=True
        )

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_LAY_formHelpMargin = pm.formLayout()

        self.ui_LAY_scrollHelp = pm.scrollLayout(
            childResizable=True
        )

        self.ui_LAY_formHelpMargin.attachForm(self.ui_LAY_scrollHelp, 'top', 2)
        self.ui_LAY_formHelpMargin.attachForm(self.ui_LAY_scrollHelp, 'left', 2)
        self.ui_LAY_formHelpMargin.attachForm(self.ui_LAY_scrollHelp, 'right', 2)
        self.ui_LAY_formHelpMargin.attachForm(self.ui_LAY_scrollHelp, 'bottom', 2)

        pm.frameLayout(
            label='Help on ' + WIN_TITLE,
            collapsable=False,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True
        )

        pm.rowLayout(
            columnAttach=[1, 'both', 10]
        )

        self.ui_TXT_help = pm.text('', align='left')

        pm.setParent(self.ui_LAY_tabHelp)

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_LAY_formAboutMargin = pm.formLayout()

        self.ui_LAY_scrollAbout = pm.scrollLayout(
            childResizable=True
        )

        self.ui_LAY_formAboutMargin.attachForm(self.ui_LAY_scrollAbout, 'top', 2)
        self.ui_LAY_formAboutMargin.attachForm(self.ui_LAY_scrollAbout, 'left', 2)
        self.ui_LAY_formAboutMargin.attachForm(self.ui_LAY_scrollAbout, 'right', 2)
        self.ui_LAY_formAboutMargin.attachForm(self.ui_LAY_scrollAbout, 'bottom', 2)

        pm.frameLayout(
            label='About ' + WIN_TITLE,
            collapsable=False,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True
        )

        pm.rowLayout(
            columnAttach=[1, 'both', 10]
        )

        self.ui_TXT_about = pm.text('', align='center')

        pm.setParent(self.ui_LAY_formMainHelp)

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_BTN_closeHelp = pm.button(
            'Close',
            command=lambda x: pm.deleteUI(WIN_HELPNAME)
        )

        # - - - - - Organize Main Form Layout - - - - -

        self.ui_LAY_formMainHelp.attachForm(self.ui_LAY_tabHelp, 'top', 2)
        self.ui_LAY_formMainHelp.attachForm(self.ui_LAY_tabHelp, 'left', 2)
        self.ui_LAY_formMainHelp.attachForm(self.ui_LAY_tabHelp, 'right', 2)
        self.ui_LAY_formMainHelp.attachControl(self.ui_LAY_tabHelp, 'bottom', 2, self.ui_BTN_closeHelp)

        self.ui_LAY_formMainHelp.attachNone(self.ui_BTN_closeHelp, 'top')
        self.ui_LAY_formMainHelp.attachForm(self.ui_BTN_closeHelp, 'left', 2)
        self.ui_LAY_formMainHelp.attachForm(self.ui_BTN_closeHelp, 'right', 2)
        self.ui_LAY_formMainHelp.attachForm(self.ui_BTN_closeHelp, 'bottom', 2)

        # - - - - - - - - - - - - - - - - - - - -

        pm.tabLayout(
            self.ui_LAY_tabHelp,
            edit=True,
            tabLabel=(
                (self.ui_LAY_formHelpMargin, 'Help'),
                (self.ui_LAY_formAboutMargin, 'About')
            )
        )

        # - - - - - - - - - - - - - - - - - - - -

        textHelp = """
----- General Info -----

This tool will rename SELECTED nodes by some patterns and rules.
You can choose between:

   - Rename - renamer will try to rename all objects to some fixed string.
            If node with this name already exists in particular path,
            it will add or increment index after object's name.

   - Find and Replace - searches for some substring in SELECTED object's names
                      and substitutes all appearances with another string

   - Add Prefix - prefixes object names with specified string

   - Add Suffix - adds provided string to end of object's names

   - Rename and Number - renames sequentially all selected objects by
                       specified pattern. Type "#" symbol(s) in New Name
                       where you want to place numbering.
                       For example:
                          pCube#  ->  pCube1, pCube2, ..., pCube15, ...
                          pCube####  ->  pCube0001, pCube0002, ..., pCube0015, ...
                          obj_##_a  ->  obj_01_a, obj_02_a, ..., obj_15_a, ...
                       Omitting "#" will result in pattern:
                          pCube  ->  pCube1, pCube2, ..., pCube15, ...

----- Shape Processing -----

This option tells FX Renamer how to rename shapes.
   - Rename shapes according to it's transforms (even if it's not selected):
                 will rename shapes of processed nodes according to it's transform new name.
                 There some rules of renaming:

                 1.   Only one shape under transform - most common case.
                      Renamer will obey Maya's convention. New shape name will be:
                            <ParentNameWithoutIndex>Shape<ParentIndex> i.e.
                            pCube -> pCubeShape
                            pSphere100 -> pSphereShape100
                            obj10_A -> obj10_AShape

                 2.   Several shapes under transform but all of one type.
                      New shape names will be:
                            pCube -> pCube_Shape1, pCube_Shape2, ....
                            pSphere100 -> pSphere100_Shape1, pSphere100_Shape2, ...
                            obj10_A -> obj10_A_Shape1, obj10_A_Shape2, ...

                 3.   Several shapes under transform of different types.
                      New shape names will be:
                            pCube -> pCube_meshShape1, pCube_meshShape2, pCube_nurbsSurfaceShape1, ...
                            pSphere100 -> pSphere100_meshShape1, pSphere100_meshShape2, pSphere100_nurbsSurfaceShape1, ...
                            obj10_A -> obj10_A_meshShape1, obj10_A_meshShape2, obj10_A_nurbsSurfaceShape1, ...


   - Don't rename shapes:
                 ignores shapes at all, even if it's selected

   - Treat shapes as ordinary nodes:
                 if shape selected - rename it according to chosen rule
                 if it is not - ignore it

----- Reset Settings -----

Use "Edit" -> "Reset Settings" to restore defaults
"""

        textAbout = "\n" + SCRIPT_NAME + ' ' + SCRIPT_VERSION + """
Programmed by Eugene Davydenko, 2012

This script may be freely distributed.
Modify at your own risk.

email: etchermail@gmail.com
"""

        self.ui_TXT_help.setLabel(textHelp)
        self.ui_TXT_about.setLabel(textAbout)

        self.ui_LAY_tabHelp.setSelectTabIndex(tab)
        self.helpWindow.show()
        self.helpWindow.setHeight(500)
        self.helpWindow.setWidth(600)


def run():
    RenamerUI()
