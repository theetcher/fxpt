import math
# import time
from array import array

import maya.cmds as m
from maya.mel import eval as meval
import pymel.core as pm
# from pymel.core.datatypes import Vector

import maya.OpenMaya as om

SCRIPT_VERSION = 'v1.0'
SCRIPT_NAME = 'Select Component By Edge Angle'
WIN_NAME = 'fx_selectComponentByAngle_win'
WIN_HELPNAME = 'fx_selectComponentByAngle_helpwin'
WIN_TITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION
WIN_HELPTITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION + ' Help'
UI_LABEL_WIDTH = 100
UI_INPUT_WIDTH = 240
UI_APPLY_BUTTON_STRING = 'Set Target Geometry'


def getParent(node):
    parents = m.listRelatives(node, parent=True, fullPath=True)
    if parents:
        return parents[0]
    else:
        return None


def longNameOf(node):
    if node and m.objExists(node):
        longNames = m.ls(node, l=True)
        if longNames:
            return longNames[0]


def selectComponents(components):
    if components:
        m.select(components)
    else:
        m.select(cl=True)


# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic
class SelectComponentByAngleUI:

    def __init__(self):
        
        self.targetGeom = []
        self.geometryData = GeometryData()

        self.ui_createUI()
        self.ui_setTargetGeometry()

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

        self.ui_mainForm = pm.formLayout()

        self.ui_LAY_mainScroll = pm.scrollLayout(
            childResizable=True
        )

        self.ui_LAY_frameControlPanel = pm.frameLayout(
            label='Control Panel',
            collapsable=True,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True
        )

        pm.columnLayout(adjustableColumn=True)

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_RADBTNGRP_component = pm.radioButtonGrp(
            label='Component',
            labelArray3=['Polygons', 'Edges', 'Vertices'],
            numberOfRadioButtons=3,
            columnWidth=[1, UI_LABEL_WIDTH],
            columnAttach=[1, 'right', 5],
            changeCommand=self.selectValidGeometry,
        )

        pm.separator(style='in', height=10)

        pm.rowLayout(
            numberOfColumns=2,
            columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH],
            columnAttach=[1, 'right', 5]
        )

        # - - - - - - - - - - - - - - - - - - - -

        pm.text(label='Min Angle')

        self.ui_FLTSLGRP_minAngle = pm.floatSliderGrp(
            field=True,
            minValue=0,
            maxValue=180,
            fieldMinValue=0,
            fieldMaxValue=180,
            value=0,
            step=0.001,
            fieldStep=0.001,
            sliderStep=0.001,
            changeCommand=self.selectValidGeometry,
            dragCommand=self.selectValidGeometry
        )

        pm.setParent('..')  # local row -> frame column

        pm.rowLayout(
            numberOfColumns=2,
            columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH],
            columnAttach=[1, 'right', 5]
        )

        # - - - - - - - - - - - - - - - - - - - -

        pm.text(label='Max Angle')

        self.ui_FLTSLGRP_maxAngle = pm.floatSliderGrp(
            field=True,
            minValue=0,
            maxValue=180,
            fieldMinValue=0,
            fieldMaxValue=180,
            value=0,
            step=0.001,
            fieldStep=0.001,
            sliderStep=0.001,
            changeCommand=self.selectValidGeometry,
            dragCommand=self.selectValidGeometry
        )

        pm.setParent('..')  # local row -> frame column

        pm.separator(style='in', height=10)

        pm.rowLayout(
            numberOfColumns=2,
            columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH],
            columnAttach=[1, 'right', 5]
        )

        # - - - - - - - - - - - - - - - - - - - -

        pm.text(label='Highlight')

        self.ui_CHK_highlight = pm.checkBox(
            label='',
            changeCommand=self.ui_CHK_highlight_change
        )

        # - - - - - - - - - - - - - - - - - - - -

        pm.setParent(self.ui_mainForm)

        self.ui_BTN_select = pm.button(
            label=UI_APPLY_BUTTON_STRING,
            command=self.ui_setTargetGeometry
        )

        self.ui_BTN_close = pm.button(
            label='Close',
            command=self.ui_close
        )

        # - - - - - Organize Main Form Layout - - - - -

        self.ui_mainForm.attachForm(self.ui_LAY_mainScroll, 'top', 2)
        self.ui_mainForm.attachForm(self.ui_LAY_mainScroll, 'left', 2)
        self.ui_mainForm.attachForm(self.ui_LAY_mainScroll, 'right', 2)
        self.ui_mainForm.attachControl(self.ui_LAY_mainScroll, 'bottom', 2, self.ui_BTN_select)

        self.ui_mainForm.attachNone(self.ui_BTN_select, 'top')
        self.ui_mainForm.attachForm(self.ui_BTN_select, 'left', 2)
        self.ui_mainForm.attachPosition(self.ui_BTN_select, 'right', 2, 50)
        self.ui_mainForm.attachForm(self.ui_BTN_select, 'bottom', 2)

        self.ui_mainForm.attachNone(self.ui_BTN_close, 'top')
        self.ui_mainForm.attachPosition(self.ui_BTN_close, 'left', 2, 50)
        self.ui_mainForm.attachForm(self.ui_BTN_close, 'right', 2)
        self.ui_mainForm.attachForm(self.ui_BTN_close, 'bottom', 2)

        self.ui_initSettings()
        self.ui_loadSettings()

        self.window.show()
        m.refresh()

    def ui_initSettings(self):
        optVars = pm.env.optionVars
        if 'fx_selectComponentByAngle_component' not in optVars:
            optVars['fx_selectComponentByAngle_component'] = 1
        if 'fx_selectComponentByAngle_minAngle' not in optVars:
            optVars['fx_selectComponentByAngle_minAngle'] = 0.0
        if 'fx_selectComponentByAngle_maxAngle' not in optVars:
            optVars['fx_selectComponentByAngle_maxAngle'] = 45.0
        if 'fx_selectComponentByAngle_highlight' not in optVars:
            optVars['fx_selectComponentByAngle_highlight'] = 1

    def ui_loadSettings(self):
        optVars = pm.env.optionVars
        self.ui_RADBTNGRP_component.setSelect(optVars['fx_selectComponentByAngle_component'])
        self.ui_FLTSLGRP_minAngle.setValue(optVars['fx_selectComponentByAngle_minAngle'])
        self.ui_FLTSLGRP_maxAngle.setValue(optVars['fx_selectComponentByAngle_maxAngle'])
        self.ui_CHK_highlight.setValue(optVars['fx_selectComponentByAngle_highlight'])

    def ui_saveSettings(self):
        optVars = pm.env.optionVars
        optVars['fx_selectComponentByAngle_component'] = self.ui_RADBTNGRP_component.getSelect()
        optVars['fx_selectComponentByAngle_minAngle'] = self.ui_FLTSLGRP_minAngle.getValue()
        optVars['fx_selectComponentByAngle_maxAngle'] = self.ui_FLTSLGRP_maxAngle.getValue()
        optVars['fx_selectComponentByAngle_highlight'] = self.ui_CHK_highlight.getValue()

    # noinspection PyUnusedLocal
    def ui_resetSettings(self, *args):
        optionVarsList = (
            'fx_selectComponentByAngle_component',
            'fx_selectComponentByAngle_minAngle',
            'fx_selectComponentByAngle_maxAngle',
            'fx_selectComponentByAngle_highlight'
        )
        optVars = pm.env.optionVars
        for var in optionVarsList:
            optVars.pop(var)
        self.ui_initSettings()
        self.ui_loadSettings()
        self.selectValidGeometry()

    # noinspection PyUnusedLocal
    def ui_close(self, *args):
        self.ui_saveSettings()
        if pm.window(WIN_NAME, exists=True):
            pm.deleteUI(WIN_NAME, window=True)

    # noinspection PyUnusedLocal
    def ui_setTargetGeometry(self, *args):
        self.setTargetGeometry()

        if not self.targetGeom:
            return

        self.geometryData.generateGeometryInfo(self.targetGeom)
        self.selectValidGeometry()

    # noinspection PyUnusedLocal
    def ui_CHK_highlight_change(self, *args):
        if not self.targetGeom:
            return
        if self.ui_CHK_highlight.getValue():
            m.hilite(self.targetGeom, replace=True)
        else:
            m.hilite(self.targetGeom, unHilite=True)

    def setTargetGeometry(self):
        meshes = m.ls(
            selection=True,
            long=True,
            dagObjects=True,
            allPaths=True,
            type='mesh',
            noIntermediate=True
        )
        if meshes:
            for x in meshes:
                transform = getParent(x)
                if transform:
                    self.targetGeom.append(x)
        else:
            pm.confirmDialog(
                title='Error',
                message='Invalid selection.\nSelect at least one polygon object and press "' + UI_APPLY_BUTTON_STRING + '"`.',
                button=['OK'],
                defaultButton='OK',
                icon='critical'
            )

    # noinspection PyUnusedLocal,PyCallByClass
    def selectValidGeometry(self, *args):

        _min = self.ui_FLTSLGRP_minAngle.getValue()
        _max = self.ui_FLTSLGRP_maxAngle.getValue()

        meval('changeSelectMode -component; setComponentPickMask "All" 0; setComponentPickMask "Line" true;')
        self.ui_CHK_highlight_change(True)

        validEdges = self.geometryData.getValidEdges(_min, _max)
        om.MGlobal.setActiveSelectionList(validEdges)

        if self.ui_RADBTNGRP_component.getSelect() == 1:
            components = m.polyListComponentConversion(fromEdge=True, toFace=True)
            meval('setComponentPickMask "All" 0; setComponentPickMask "Facet" true;')
            selectComponents(components)
        elif self.ui_RADBTNGRP_component.getSelect() == 3:
            components = m.polyListComponentConversion(fromEdge=True, toVertex=True)
            meval('setComponentPickMask "All" 0; setComponentPickMask "Point" true;')
            selectComponents(components)

    # noinspection PyUnusedLocal
    def ui_showHelp(self, tab, *args):

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

        self.ui_TXT_help = pm.text('', align='center')

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
- Info -
This tool select polymesh components based on "Edge Angle",
i.e. angle between normals of 2 polygons sharing this particular edge.
Non-manifold geometry is not supported (meshes with edges sharing more than 2 polygons).

- Workflow -
Select one ore more polygon meshes and run the script. Tool Control Panel will popup
and component selection will be performed based on Control Panel settings.
You can tweak options and interactively see the result.
If you want to select components on other objects
and don't want to close the window,
choose some polymeshes and press "Set Target Geometry".

- Component -
Choose component to select by Edge Angle.

- Min and Max Angle -
Component will be selected if Edge Angle is between theese values.

- Highlight -
Toggles object highlight.
Sometimes its hard to see components selected when object highligh is on.
Use this check box to unhighlight mesh objects and
clearly observe only component selection.

- Reset Settings -
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


class GeometryData:
    def __init__(self):
        self.edgeData = []

    def generateGeometryInfo(self, objList):

        pi = math.pi

        self.edgeData = []

        for obj in objList:

            selList = om.MSelectionList()
            selList.add(longNameOf(obj))
            dagPath = om.MDagPath()
            selList.getDagPath(0, dagPath)

            edgeIter = om.MItMeshEdge(dagPath)
            faceIter = om.MItMeshPolygon(dagPath)
            # normal1 = om.MVector()
            # normal2 = om.MVector()
            connectedFaces = om.MIntArray()
            # dummy = om.MScriptUtil()

            edgeDataObj = EdgeData(dagPath, edgeIter.count())
            self.edgeData.append(edgeDataObj)

            _mvector = om.MVector
            # normalCache = []
            normalCache = [_mvector() for _ in xrange(faceIter.count())]
            while not faceIter.isDone():
                faceIter.getNormal(normalCache[faceIter.index()], om.MSpace.kWorld)
                faceIter.next()

            i = 0
            while not edgeIter.isDone():

                edgeIter.getConnectedFaces(connectedFaces)

                if connectedFaces.length() == 2:
                    normal1 = normalCache[connectedFaces[0]]
                    normal2 = normalCache[connectedFaces[1]]
                    angle = normal1.angle(normal2) * 180 / pi

                    edgeDataObj.edgeIds[i] = edgeIter.index()
                    edgeDataObj.edgeAngles[i] = angle
                    i += 1

                edgeIter.next()

    def getValidEdges(self, _min, _max):

        selList = om.MSelectionList()
        compListFn = om.MFnSingleIndexedComponent()
        indexes = om.MIntArray()

        for obj in self.edgeData:
            components = compListFn.create(om.MFn.kMeshEdgeComponent)
            indexes.clear()
            for i, angle in enumerate(obj.edgeAngles):
                if _min <= angle <= _max:
                    indexes.append(obj.edgeIds[i])
            compListFn.addElements(indexes)
            selList.add(obj.dagPath, components)

        return selList


class EdgeData:
    def __init__(self, dagPath, arraySize):
        self.dagPath = dagPath
        self.edgeIds = array('i', [-1] * arraySize)
        self.edgeAngles = array('d', [-1000] * arraySize)


def run():
    SelectComponentByAngleUI()

