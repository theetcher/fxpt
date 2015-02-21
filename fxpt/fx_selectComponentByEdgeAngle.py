import math
from array import array

import maya.cmds as m
from maya.mel import eval as meval
import pymel.core as pm

import maya.OpenMaya as om

from fxpt.fx_prefsaver import PrefSaver, Serializers

SCRIPT_VERSION = 'v1.0'
SCRIPT_NAME = 'Select Component By Edge Angle'
WIN_NAME = 'fx_selectComponentByAngle_win'
WIN_HELPNAME = 'fx_selectComponentByAngle_helpwin'
WIN_TITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION
WIN_HELPTITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION + ' Help'
UI_LABEL_WIDTH = 100
UI_INPUT_WIDTH = 240
UI_APPLY_BUTTON_STRING = 'Set Target Geometry'
OPT_VAR_NAME = 'fx_selectComponentByEdgeAngle_prefs'


#TODO: strange selection display when highlight is off in VP2.0

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
        
        self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerOptVar(OPT_VAR_NAME))

        self.targetGeom = []
        self.geometryData = GeometryData()

        self.ui_createUI()
        self.ui_setTargetGeometry()

    def ui_createUI(self):
        self.winName = WIN_NAME
        self.winTitle = WIN_TITLE

        if pm.window(WIN_NAME, exists=True):
            pm.deleteUI(WIN_NAME, window=True)

        with pm.window(WIN_NAME, title=WIN_TITLE, maximizeButton=False, menuBar=True, menuBarVisible=True) as window:
            pm.menu(label='Edit', tearOff=False)
            pm.menuItem(label='Reset Settings', command=self.ui_resetSettings)
            pm.menu(label='Help', tearOff=False)
            pm.menuItem(label='Help on ' + WIN_TITLE, command=pm.Callback(self.ui_showHelp, 1))
            pm.menuItem(divider=True)
            pm.menuItem(label='Script Information', command=pm.Callback(self.ui_showHelp, 2))

            with pm.formLayout() as ui_mainForm:

                with pm.scrollLayout(childResizable=True) as ui_LAY_mainScroll:

                    with pm.frameLayout(label='Control Panel', collapsable=True, marginHeight=3, borderStyle='etchedIn', borderVisible=True):

                        with pm.columnLayout(adjustableColumn=True):

                            self.ui_RADBTNGRP_component = pm.radioButtonGrp(
                                'ui_RADBTNGRP_component',
                                label='Component',
                                labelArray3=['Polygons', 'Edges', 'Vertices'],
                                numberOfRadioButtons=3,
                                columnWidth=[1, UI_LABEL_WIDTH],
                                columnAttach=[1, 'right', 5],
                                changeCommand=self.selectValidGeometry,
                            )

                            pm.separator(style='in', height=10)

                            with pm.rowLayout(numberOfColumns=2, columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH], columnAttach=[1, 'right', 5]):

                                pm.text(label='Min Angle')

                                self.ui_FLTSLGRP_minAngle = pm.floatSliderGrp(
                                    'ui_FLTSLGRP_minAngle',
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

                            with pm.rowLayout(numberOfColumns=2, columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH], columnAttach=[1, 'right', 5]):

                                pm.text(label='Max Angle')

                                self.ui_FLTSLGRP_maxAngle = pm.floatSliderGrp(
                                    'ui_FLTSLGRP_maxAngle',
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

                            pm.separator(style='in', height=10)

                            with pm.rowLayout(numberOfColumns=2, columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH], columnAttach=[1, 'right', 5]):

                                pm.text(label='Highlight')

                                self.ui_CHK_highlight = pm.checkBox(
                                    'ui_CHK_highlight',
                                    label='',
                                    changeCommand=self.ui_CHK_highlight_change
                                )

                self.ui_BTN_select = pm.button(
                    label=UI_APPLY_BUTTON_STRING,
                    command=self.ui_setTargetGeometry
                )

                self.ui_BTN_close = pm.button(
                    label='Close',
                    command=self.ui_close
                )

            ui_mainForm.attachForm(ui_LAY_mainScroll, 'top', 2)
            ui_mainForm.attachForm(ui_LAY_mainScroll, 'left', 2)
            ui_mainForm.attachForm(ui_LAY_mainScroll, 'right', 2)
            ui_mainForm.attachControl(ui_LAY_mainScroll, 'bottom', 2, self.ui_BTN_select)

            ui_mainForm.attachNone(self.ui_BTN_select, 'top')
            ui_mainForm.attachForm(self.ui_BTN_select, 'left', 2)
            ui_mainForm.attachPosition(self.ui_BTN_select, 'right', 2, 50)
            ui_mainForm.attachForm(self.ui_BTN_select, 'bottom', 2)

            ui_mainForm.attachNone(self.ui_BTN_close, 'top')
            ui_mainForm.attachPosition(self.ui_BTN_close, 'left', 2, 50)
            ui_mainForm.attachForm(self.ui_BTN_close, 'right', 2)
            ui_mainForm.attachForm(self.ui_BTN_close, 'bottom', 2)

        self.ui_initSettings()
        self.ui_loadSettings()

        window.show()
        m.refresh()

    def ui_initSettings(self):
        self.prefSaver.addControl(self.ui_RADBTNGRP_component, PrefSaver.UIType.PMRadioButtonGrp3, 1)
        self.prefSaver.addControl(self.ui_FLTSLGRP_minAngle, PrefSaver.UIType.PMFloatSliderGrp, 0)
        self.prefSaver.addControl(self.ui_FLTSLGRP_maxAngle, PrefSaver.UIType.PMFloatSliderGrp, 45)
        self.prefSaver.addControl(self.ui_CHK_highlight, PrefSaver.UIType.PMCheckBox, True)

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    # noinspection PyUnusedLocal
    def ui_resetSettings(self, *args):
        self.prefSaver.resetPrefs()
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

        #TODO: fix stuff below with highlight option
        # strange things to make highlight working on window show and "Set Target Geometry" if option is false
        if not self.getHighlightState():
            self.setHighlight(False)
            self.selectValidGeometry()
            self.setHighlight(True)
            self.selectValidGeometry()
        else:
            self.selectValidGeometry()

    # noinspection PyUnusedLocal
    def ui_CHK_highlight_change(self, arg):
        self.selectValidGeometry()

    def getHighlightState(self):
        return self.ui_CHK_highlight.getValue()

    def doHighlight(self):
        self.setHighlight(self.getHighlightState())

    def setHighlight(self, state):
        if not self.targetGeom:
            return
        if state:
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
        self.doHighlight()

        validEdges = self.geometryData.getValidEdges(_min, _max)
        # noinspection PyTypeChecker
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

        with pm.window(WIN_HELPNAME, title=WIN_HELPTITLE, maximizeButton=False) as helpWindow:

            with pm.formLayout() as ui_LAY_formMainHelp:

                with pm.tabLayout(innerMarginWidth=50, innerMarginHeight=50, childResizable=True) as ui_LAY_tabHelp:

                    with pm.formLayout() as ui_LAY_formHelpMargin:

                        with pm.scrollLayout(childResizable=True) as ui_LAY_scrollHelp:

                            ui_LAY_formHelpMargin.attachForm(ui_LAY_scrollHelp, 'top', 2)
                            ui_LAY_formHelpMargin.attachForm(ui_LAY_scrollHelp, 'left', 2)
                            ui_LAY_formHelpMargin.attachForm(ui_LAY_scrollHelp, 'right', 2)
                            ui_LAY_formHelpMargin.attachForm(ui_LAY_scrollHelp, 'bottom', 2)

                            with pm.frameLayout(
                                label='Help on ' + WIN_TITLE,
                                collapsable=False,
                                marginHeight=3,
                                borderStyle='etchedIn',
                                borderVisible=True
                            ):

                                with pm.rowLayout(columnAttach=[1, 'both', 10]):

                                    ui_TXT_help = pm.text('', align='center')

                    with pm.formLayout() as ui_LAY_formAboutMargin:

                        with pm.scrollLayout(childResizable=True) as ui_LAY_scrollAbout:

                            ui_LAY_formAboutMargin.attachForm(ui_LAY_scrollAbout, 'top', 2)
                            ui_LAY_formAboutMargin.attachForm(ui_LAY_scrollAbout, 'left', 2)
                            ui_LAY_formAboutMargin.attachForm(ui_LAY_scrollAbout, 'right', 2)
                            ui_LAY_formAboutMargin.attachForm(ui_LAY_scrollAbout, 'bottom', 2)

                            with pm.frameLayout(
                                label='About ' + WIN_TITLE,
                                collapsable=False,
                                marginHeight=3,
                                borderStyle='etchedIn',
                                borderVisible=True
                            ):

                                with pm.rowLayout(columnAttach=[1, 'both', 10]):

                                    ui_TXT_about = pm.text('', align='center')

                ui_BTN_closeHelp = pm.button(
                    'Close',
                    command=lambda x: pm.deleteUI(WIN_HELPNAME)
                )

            ui_LAY_formMainHelp.attachForm(ui_LAY_tabHelp, 'top', 2)
            ui_LAY_formMainHelp.attachForm(ui_LAY_tabHelp, 'left', 2)
            ui_LAY_formMainHelp.attachForm(ui_LAY_tabHelp, 'right', 2)
            ui_LAY_formMainHelp.attachControl(ui_LAY_tabHelp, 'bottom', 2, ui_BTN_closeHelp)

            ui_LAY_formMainHelp.attachNone(ui_BTN_closeHelp, 'top')
            ui_LAY_formMainHelp.attachForm(ui_BTN_closeHelp, 'left', 2)
            ui_LAY_formMainHelp.attachForm(ui_BTN_closeHelp, 'right', 2)
            ui_LAY_formMainHelp.attachForm(ui_BTN_closeHelp, 'bottom', 2)

            # - - - - - - - - - - - - - - - - - - - -

            pm.tabLayout(
                ui_LAY_tabHelp,
                edit=True,
                tabLabel=(
                    (ui_LAY_formHelpMargin, 'Help'),
                    (ui_LAY_formAboutMargin, 'About')
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

        ui_TXT_help.setLabel(textHelp)
        ui_TXT_about.setLabel(textAbout)

        ui_LAY_tabHelp.setSelectTabIndex(tab)
        helpWindow.show()


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
            connectedFaces = om.MIntArray()

            edgeDataObj = EdgeData(dagPath, edgeIter.count())
            self.edgeData.append(edgeDataObj)

            _mvector = om.MVector
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

