import math
import webbrowser

import maya.cmds as m
from maya.mel import eval as meval
import maya.api.OpenMaya as om

from fxpt3.fx_prefsaver import prefsaver, serializers

SCRIPT_VERSION = 'v1.0'
SCRIPT_NAME = 'Select Component By Edge Angle'
WIN_NAME = 'fx_selectComponentByAngle_win'
WIN_TITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION
UI_LABEL_WIDTH = 100
UI_INPUT_WIDTH = 240
UI_APPLY_BUTTON_STRING = 'Set Target Geometry'
OPT_VAR_NAME = 'fx_selectComponentByEdgeAngle_prefs'

COMPONENT_POLYGONS = 1
COMPONENT_EDGES = 2
COMPONENT_VERTICES = 3


# TODO: strange selection display when highlight is off in VP2.0


def setPickMask(mask, changeToComponentMode=False):
    # these MEL procedures come with Maya's UI scripts, they don't exist in batch mode
    if m.about(batch=True):
        return
    cmd = 'setComponentPickMask "All" 0; setComponentPickMask "{0}" true;'.format(mask)
    if changeToComponentMode:
        cmd = 'changeSelectMode -component; ' + cmd
    meval(cmd)


def selectComponents(components):
    if components:
        m.select(components)
    else:
        m.select(cl=True)


def getSelectedMeshes():
    # objectsOnly: also take the meshes of selected components (e.g. the edges this tool selected)
    return m.ls(
        selection=True,
        long=True,
        dagObjects=True,
        objectsOnly=True,
        allPaths=True,
        type='mesh',
        noIntermediate=True
    ) or []


class EdgeData(object):

    def __init__(self, mesh):
        self.mesh = mesh
        selList = om.MSelectionList()
        selList.add(mesh)
        self.dagPath = selList.getDagPath(0)
        # ids and angles (degrees) of the edges shared by exactly two faces
        self.edgeIds = []
        self.edgeAngles = []
        self.generate()

    def generate(self):
        faceIter = om.MItMeshPolygon(self.dagPath)
        normals = [None] * faceIter.count()
        meshFn = om.MFnMesh(self.dagPath)
        edgeFaces = [[] for _ in range(meshFn.numEdges)]

        while not faceIter.isDone():
            faceId = faceIter.index()
            # not faceIter.getNormal(om.MSpace.kWorld): kWorld is an int, so that call matches the
            # getNormal(vertexIndex) overload and returns a vertex normal
            normals[faceId] = meshFn.getPolygonNormal(faceId, om.MSpace.kWorld)
            for edgeId in faceIter.getEdges():
                edgeFaces[edgeId].append(faceId)
            faceIter.next()

        for edgeId, faces in enumerate(edgeFaces):
            if len(faces) == 2:
                self.edgeIds.append(edgeId)
                self.edgeAngles.append(math.degrees(normals[faces[0]].angle(normals[faces[1]])))

    def isValid(self):
        return self.dagPath.isValid() and m.objExists(self.dagPath.fullPathName())

    def getValidEdgeIds(self, _min, _max):
        return [edgeId for edgeId, angle in zip(self.edgeIds, self.edgeAngles) if _min <= angle <= _max]


class GeometryData(object):

    def __init__(self):
        self.edgeData = []

    def setTargetGeometry(self, meshes):
        self.edgeData = [EdgeData(mesh) for mesh in meshes]

    def getTargetGeometry(self):
        # target meshes may have been deleted since they were set
        self.edgeData = [obj for obj in self.edgeData if obj.isValid()]
        return [obj.dagPath.fullPathName() for obj in self.edgeData]

    def getValidEdges(self, _min, _max):
        selList = om.MSelectionList()
        self.getTargetGeometry()
        for obj in self.edgeData:
            compFn = om.MFnSingleIndexedComponent()
            components = compFn.create(om.MFn.kMeshEdgeComponent)
            compFn.addElements(obj.getValidEdgeIds(_min, _max))
            selList.add((obj.dagPath, components))
        return selList


def selectValidComponents(geometryData, _min, _max, component, highlight):
    targets = geometryData.getTargetGeometry()

    setPickMask('Line', changeToComponentMode=True)
    if targets:
        if highlight:
            m.hilite(targets, replace=True)
        else:
            m.hilite(targets, unHilite=True)

    # API selection: not undoable, so dragging the sliders doesn't flood the undo queue
    om.MGlobal.setActiveSelectionList(geometryData.getValidEdges(_min, _max))

    if component == COMPONENT_POLYGONS:
        components = m.polyListComponentConversion(fromEdge=True, toFace=True)
        setPickMask('Facet')
        selectComponents(components)
    elif component == COMPONENT_VERTICES:
        components = m.polyListComponentConversion(fromEdge=True, toVertex=True)
        setPickMask('Point')
        selectComponents(components)


# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic,PyUnusedLocal
class SelectComponentByAngleUI(object):

    def __init__(self):
        self.prefSaver = prefsaver.PrefSaver(serializers.SerializerOptVar(OPT_VAR_NAME))
        self.geometryData = GeometryData()

        self.ui_createUI()
        self.ui_initSettings()
        self.ui_loadSettings()

        m.showWindow(self.window)
        m.refresh()

        self.ui_setTargetGeometry()

    def ui_createUI(self):
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

            self.ui_LAY_mainColumn = m.columnLayout(adjustableColumn=True)

            m.frameLayout(
                label='Control Panel',
                collapsable=True,
                collapse=False,
                marginHeight=3
            )

            m.columnLayout(adjustableColumn=True)

            # control names are the same as in the legacy PyMEL version, so prefs saved by it still match
            self.ui_RADBTNGRP_component = m.radioButtonGrp(
                'ui_RADBTNGRP_component',
                label='Component',
                labelArray3=('Polygons', 'Edges', 'Vertices'),
                numberOfRadioButtons=3,
                columnWidth=(1, UI_LABEL_WIDTH),
                columnAttach=(1, 'right', 5),
                changeCommand=self.ui_onChange
            )

            m.separator(style='in', height=10)

            self.ui_FLTSLGRP_minAngle = self.ui_createAngleSlider('Min Angle', 'ui_FLTSLGRP_minAngle')
            self.ui_FLTSLGRP_maxAngle = self.ui_createAngleSlider('Max Angle', 'ui_FLTSLGRP_maxAngle')

            m.separator(style='in', height=10)

            m.rowLayout(
                numberOfColumns=2,
                columnWidth2=(UI_LABEL_WIDTH, UI_INPUT_WIDTH),
                columnAttach=(1, 'right', 5)
            )
            m.text(label='Highlight')
            self.ui_CHK_highlight = m.checkBox(
                'ui_CHK_highlight',
                label='',
                changeCommand=self.ui_onChange
            )

            m.setParent(self.ui_LAY_mainForm)

            self.ui_BTN_select = m.button(
                label=UI_APPLY_BUTTON_STRING,
                command=self.ui_setTargetGeometry
            )

            self.ui_BTN_close = m.button(
                label='Close',
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
                (self.ui_BTN_select, 'left', 5),
                (self.ui_BTN_select, 'bottom', 5),
                (self.ui_BTN_close, 'right', 5),
                (self.ui_BTN_close, 'bottom', 5),
            ],
            attachControl=[
                (self.ui_TAB_top, 'bottom', 5, self.ui_BTN_select),
            ],
            attachPosition=[
                (self.ui_BTN_select, 'right', 2, 50),
                (self.ui_BTN_close, 'left', 2, 50),
            ],
            attachNone=[
                (self.ui_BTN_select, 'top'),
                (self.ui_BTN_close, 'top'),
            ]
        )

    def ui_createAngleSlider(self, label, name):
        m.rowLayout(
            numberOfColumns=2,
            columnWidth2=(UI_LABEL_WIDTH, UI_INPUT_WIDTH),
            columnAttach=(1, 'right', 5)
        )
        m.text(label=label)
        m.setUITemplate('DefaultTemplate', popTemplate=True)  # strange slider group visual with default template
        try:
            slider = m.floatSliderGrp(
                name,
                field=True,
                minValue=0,
                maxValue=180,
                fieldMinValue=0,
                fieldMaxValue=180,
                value=0,
                step=0.001,
                fieldStep=0.001,
                sliderStep=0.001,
                changeCommand=self.ui_onChange,
                dragCommand=self.selectValidGeometry
            )
        finally:
            m.setUITemplate('DefaultTemplate', pushTemplate=True)
        m.setParent('..')
        return slider

    def ui_initSettings(self):
        self.prefSaver.addControl(self.ui_RADBTNGRP_component, prefsaver.UIType.MRadioButtonGrp3, COMPONENT_POLYGONS)
        self.prefSaver.addControl(self.ui_FLTSLGRP_minAngle, prefsaver.UIType.MFloatSliderGrp, 0)
        self.prefSaver.addControl(self.ui_FLTSLGRP_maxAngle, prefsaver.UIType.MFloatSliderGrp, 45)
        self.prefSaver.addControl(self.ui_CHK_highlight, prefsaver.UIType.MCheckBox, True)

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self, *args):
        # prefs are saved on every change, so closing the window with [X] loses nothing
        if m.window(WIN_NAME, exists=True):
            self.prefSaver.savePrefs()

    def ui_onChange(self, *args):
        self.selectValidGeometry()
        self.ui_saveSettings()

    def ui_resetSettings(self, *args):
        self.prefSaver.resetPrefs()
        self.ui_onChange()

    def ui_close(self, *args):
        if m.window(WIN_NAME, exists=True):
            self.ui_saveSettings()
            m.deleteUI(WIN_NAME, window=True)

    def ui_badSelectionWarning(self):
        m.confirmDialog(
            title='Error',
            message='Invalid selection.\nSelect at least one polygon object and press "' + UI_APPLY_BUTTON_STRING + '".',
            button=['OK'],
            defaultButton='OK',
            icon='critical'
        )

    def ui_setTargetGeometry(self, *args):
        meshes = getSelectedMeshes()
        if not meshes:
            # keep the previous target, if any
            self.ui_badSelectionWarning()
            return

        self.geometryData.setTargetGeometry(meshes)

        if not self.getHighlightState():
            m.select(cl=True)
        self.selectValidGeometry()

    def getHighlightState(self):
        return m.checkBox(self.ui_CHK_highlight, q=True, value=True)

    def selectValidGeometry(self, *args):
        selectValidComponents(
            self.geometryData,
            m.floatSliderGrp(self.ui_FLTSLGRP_minAngle, q=True, value=True),
            m.floatSliderGrp(self.ui_FLTSLGRP_maxAngle, q=True, value=True),
            m.radioButtonGrp(self.ui_RADBTNGRP_component, q=True, select=True),
            self.getHighlightState()
        )

    def ui_showHelp(self, *args):
        webbrowser.open('http://davydenko.info/edge_angle_select/', new=0, autoraise=True)


def run():
    SelectComponentByAngleUI()
