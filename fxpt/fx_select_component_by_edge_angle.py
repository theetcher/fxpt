import math
from array import array

import maya.cmds as m
from maya.mel import eval as meval
import pymel.core as pm

import maya.OpenMaya as om

from fxpt.fx_prefsaver import prefsaver, serializers

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


# TODO: strange selection display when highlight is off in VP2.0

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
        
        self.prefSaver = prefsaver.PrefSaver(serializers.SerializerOptVar(OPT_VAR_NAME))

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

            pm.setUITemplate('DefaultTemplate', pushTemplate=True)

            pm.menu(label='Edit', tearOff=False)
            pm.menuItem(label='Reset Settings', command=self.ui_resetSettings)
            pm.menu(label='Help', tearOff=False)
            pm.menuItem(label='Help on ' + WIN_TITLE, command=pm.Callback(self.ui_showHelp, 1))

            with pm.formLayout() as self.ui_LAY_mainForm:

                with pm.tabLayout(tabsVisible=False) as self.ui_TAB_top:
                    pm.tabLayout(self.ui_TAB_top, e=True, height=1)

                    with pm.formLayout() as self.ui_LAY_attachForm:

                        with pm.tabLayout(tabsVisible=False, scrollable=True, innerMarginWidth=4) as self.ui_TAB_inner:

                            with pm.columnLayout(adjustableColumn=True) as self.ui_LAY_mainColumn:

                                with pm.frameLayout(
                                        label='Control Panel',
                                        collapsable=True,
                                        collapse=False,
                                        marginHeight=3,
                                ):

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

                                            pm.setUITemplate('DefaultTemplate', popTemplate=True)  # strange slider group visual with default template

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

                                            pm.setUITemplate('DefaultTemplate', pushTemplate=True)

                                        with pm.rowLayout(numberOfColumns=2, columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH], columnAttach=[1, 'right', 5]):

                                            pm.text(label='Max Angle')

                                            pm.setUITemplate('DefaultTemplate', popTemplate=True)  # strange slider group visual with default template

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

                                            pm.setUITemplate('DefaultTemplate', pushTemplate=True)

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

            self.ui_LAY_attachForm.attachForm(self.ui_TAB_inner, 'top', 0)
            self.ui_LAY_attachForm.attachForm(self.ui_TAB_inner, 'left', 0)
            self.ui_LAY_attachForm.attachForm(self.ui_TAB_inner, 'right', 0)
            self.ui_LAY_attachForm.attachForm(self.ui_TAB_inner, 'bottom', 0)

            self.ui_LAY_mainForm.attachForm(self.ui_TAB_top, 'top', 0)
            self.ui_LAY_mainForm.attachForm(self.ui_TAB_top, 'left', 0)
            self.ui_LAY_mainForm.attachForm(self.ui_TAB_top, 'right', 0)
            self.ui_LAY_mainForm.attachControl(self.ui_TAB_top, 'bottom', 5, self.ui_BTN_select)

            self.ui_LAY_mainForm.attachNone(self.ui_BTN_select, 'top')
            self.ui_LAY_mainForm.attachForm(self.ui_BTN_select, 'left', 5)
            self.ui_LAY_mainForm.attachPosition(self.ui_BTN_select, 'right', 2, 50)
            self.ui_LAY_mainForm.attachForm(self.ui_BTN_select, 'bottom', 5)

            self.ui_LAY_mainForm.attachNone(self.ui_BTN_close, 'top')
            self.ui_LAY_mainForm.attachPosition(self.ui_BTN_close, 'left', 2, 50)
            self.ui_LAY_mainForm.attachForm(self.ui_BTN_close, 'right', 5)
            self.ui_LAY_mainForm.attachForm(self.ui_BTN_close, 'bottom', 5)

        pm.setUITemplate('DefaultTemplate', popTemplate=True)

        self.ui_initSettings()
        self.ui_loadSettings()

        window.show()
        m.refresh()

    def ui_initSettings(self):
        self.prefSaver.addControl(self.ui_RADBTNGRP_component, prefsaver.UIType.PMRadioButtonGrp3, 1)
        self.prefSaver.addControl(self.ui_FLTSLGRP_minAngle, prefsaver.UIType.PMFloatSliderGrp, 0)
        self.prefSaver.addControl(self.ui_FLTSLGRP_maxAngle, prefsaver.UIType.PMFloatSliderGrp, 45)
        self.prefSaver.addControl(self.ui_CHK_highlight, prefsaver.UIType.PMCheckBox, True)

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
        import webbrowser
        webbrowser.open('http://davydenko.info/edge_angle_select/', new=0, autoraise=True)


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

