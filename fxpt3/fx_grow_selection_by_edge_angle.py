import math
import webbrowser

import maya.cmds as m
from maya.mel import eval as meval
import maya.api.OpenMaya as om

from fxpt3.fx_prefsaver import prefsaver, serializers

SCRIPT_VERSION = 'v1.5'
SCRIPT_NAME = 'Grow Selection By Edge Angle'
WIN_NAME = 'fx_growSelectionByAngle_win'
WIN_TITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION
UI_LABEL_WIDTH = 100
UI_INPUT_WIDTH = 240
UI_APPLY_BUTTON_STRING = 'Set Target Geometry'
OPT_VAR_NAME = 'fx_growSelectionByAngle_prefs'


class BadSelectionError(Exception):
    pass


def setFacePickMode():
    # these MEL procedures come with Maya's UI scripts, they don't exist in batch mode
    if not m.about(batch=True):
        meval('changeSelectMode -component; setComponentPickMask "All" 0; setComponentPickMask "Facet" true;')


class ObjectPolyData(object):

    def __init__(self, dagPath, polyIds):
        self.dagPath = dagPath
        self.initSelection = sorted(set(polyIds))
        # neighbors[faceId] = [(neighborFaceId, edgeAngleInDegrees), ...], only across edges shared by exactly two faces
        self.neighbors = []
        self.generateNeighbors()

    def generateNeighbors(self):
        faceIter = om.MItMeshPolygon(self.dagPath)
        faceCount = faceIter.count()
        normals = [None] * faceCount
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

        self.neighbors = [[] for _ in range(faceCount)]
        for faces in edgeFaces:
            if len(faces) == 2:
                f1, f2 = faces
                angle = math.degrees(normals[f1].angle(normals[f2]))
                self.neighbors[f1].append((f2, angle))
                self.neighbors[f2].append((f1, angle))

    def isValid(self):
        return self.dagPath.isValid() and m.objExists(self.dagPath.fullPathName())

    def grow(self, _min, _max):
        """Returns the ids of the initial faces plus all faces reachable from them across edges with an angle in [_min, _max]."""
        selected = bytearray(len(self.neighbors))
        for faceId in self.initSelection:
            selected[faceId] = 1

        front = list(self.initSelection)
        while front:
            nextFront = []
            for faceId in front:
                for neighborId, angle in self.neighbors[faceId]:
                    if not selected[neighborId] and _min <= angle <= _max:
                        selected[neighborId] = 1
                        nextFront.append(neighborId)
            front = nextFront

        return [i for i, s in enumerate(selected) if s]


class GrowProcessor(object):

    def __init__(self):
        self.polyData = []

    def setTargetGeom(self):
        """Takes the selected polygons as the grow start. Raises BadSelectionError if no polygons are selected."""
        selList = om.MGlobal.getActiveSelectionList()
        polyData = []

        for i in range(selList.length()):
            try:
                dagPath, components = selList.getComponent(i)
            except (TypeError, RuntimeError):
                # not a DAG item (e.g. a shading node)
                continue

            if components.isNull() or components.apiType() != om.MFn.kMeshPolygonComponent:
                continue

            ids = om.MFnSingleIndexedComponent(components).getElements()
            polyData.append(ObjectPolyData(dagPath, ids))

        if not polyData:
            raise BadSelectionError()

        self.polyData = polyData

    def getValidObjects(self):
        # target meshes may have been deleted since they were set
        self.polyData = [obj for obj in self.polyData if obj.isValid()]
        return self.polyData

    def highlightTarget(self, state):
        objects = self.getValidObjects()
        if not objects:
            return
        selList = om.MSelectionList()
        if state:
            for obj in objects:
                selList.add(obj.dagPath)
        om.MGlobal.setHiliteList(selList)

    def getValidPolygons(self, _min, _max):
        selList = om.MSelectionList()
        for obj in self.getValidObjects():
            compFn = om.MFnSingleIndexedComponent()
            components = compFn.create(om.MFn.kMeshPolygonComponent)
            compFn.addElements(obj.grow(_min, _max))
            selList.add((obj.dagPath, components))
        return selList

    def selectValidGeom(self, _min, _max, highlightState):
        setFacePickMode()
        self.highlightTarget(highlightState)
        # API selection: not undoable, so dragging the sliders doesn't flood the undo queue
        om.MGlobal.setActiveSelectionList(self.getValidPolygons(_min, _max))


# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic,PyUnusedLocal
class GrowSelectionByAngleUI(object):

    def __init__(self):
        self.prefSaver = prefsaver.PrefSaver(serializers.SerializerOptVar(OPT_VAR_NAME))
        self.growProcessor = GrowProcessor()

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
                changeCommand=self.ui_CHK_highlight_change
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
            message='Invalid selection.\nSelect at least one polygon and press "' + UI_APPLY_BUTTON_STRING + '".',
            button=['OK'],
            defaultButton='OK',
            icon='critical'
        )

    def ui_setTargetGeometry(self, *args):
        try:
            self.growProcessor.setTargetGeom()
        except BadSelectionError:
            self.ui_badSelectionWarning()
        else:
            self.selectValidGeometry()

    def ui_CHK_highlight_change(self, *args):
        self.growProcessor.highlightTarget(self.getHighlightState())
        self.ui_saveSettings()

    def getHighlightState(self):
        return m.checkBox(self.ui_CHK_highlight, q=True, value=True)

    def selectValidGeometry(self, *args):
        _min = m.floatSliderGrp(self.ui_FLTSLGRP_minAngle, q=True, value=True)
        _max = m.floatSliderGrp(self.ui_FLTSLGRP_maxAngle, q=True, value=True)
        self.growProcessor.selectValidGeom(_min, _max, self.getHighlightState())

    def ui_showHelp(self, *args):
        webbrowser.open('http://davydenko.info/edge_angle_grow/', new=0, autoraise=True)


def run():
    GrowSelectionByAngleUI()


def runNoUI(_min, _max, highlight):
    growProcessor = GrowProcessor()
    try:
        growProcessor.setTargetGeom()
    except BadSelectionError:
        m.confirmDialog(
            title='Error',
            message='Invalid selection.\nSelect at least one polygon.',
            button=['OK'],
            defaultButton='OK',
            icon='critical'
        )
        return
    growProcessor.selectValidGeom(_min, _max, highlight)
