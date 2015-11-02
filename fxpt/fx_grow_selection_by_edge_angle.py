import math
from array import array

import pymel.core as pm

from fxpt.fx_prefsaver import prefsaver, serializers

import maya.OpenMaya as om

SCRIPT_VERSION = 'v1.2'
SCRIPT_NAME = 'Grow Selection By Edge Angle'
WIN_NAME = 'fx_growSelectionByAngle_win'
WIN_HELPNAME = 'fx_growSelectionByAngle_helpwin'
WIN_TITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION
WIN_HELPTITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION + ' Help'
UI_LABEL_WIDTH = 100
UI_INPUT_WIDTH = 240
UI_APPLY_BUTTON_STRING = 'Set Target Geometry'
OPT_VAR_NAME = 'fx_growSelectionByAngle_prefs'


# noinspection PyAttributeOutsideInit
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

        with pm.window(
            WIN_NAME,
            title=WIN_TITLE,
            maximizeButton=False,
            menuBar=True,
            menuBarVisible=True
        ) as self.window:

            pm.setUITemplate('DefaultTemplate', pushTemplate=True)

            pm.menu(label='Edit', tearOff=False)
            pm.menuItem(label='Reset Settings', command=self.ui_resetSettings)
            pm.menu(label='Help', tearOff=False)
            pm.menuItem(label='Help on ' + WIN_TITLE, command=self.ui_showHelp)

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

                                        with pm.rowLayout(
                                            numberOfColumns=2,
                                            columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH],
                                            columnAttach=[1, 'right', 5]
                                        ):

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

                                        with pm.rowLayout(
                                            numberOfColumns=2,
                                            columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH],
                                            columnAttach=[1, 'right', 5]
                                        ):

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

                                        with pm.rowLayout(
                                            numberOfColumns=2,
                                            columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH],
                                            columnAttach=[1, 'right', 5]
                                        ):
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

        self.window.show()
        pm.refresh()

    # noinspection PyMethodMayBeStatic
    def ui_initSettings(self):
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

    # noinspection PyMethodMayBeStatic
    def ui_badSelectionWarning(self):
        pm.confirmDialog(
            title='Error',
            message='Invalid selection.\nSelect at least one polygon and press "' + UI_APPLY_BUTTON_STRING + '".',
            button=['OK'],
            defaultButton='OK',
            icon='critical'
        )

    # noinspection PyUnusedLocal
    def ui_setTargetGeometry(self, *args):

        self.targetGeom = []

        selList = om.MSelectionList()
        # noinspection PyCallByClass,PyTypeChecker
        om.MGlobal.getActiveSelectionList(selList)

        if selList.isEmpty():
            self.ui_badSelectionWarning()
            return

        selListIter = om.MItSelectionList(selList)
        while not selListIter.isDone():

            components = om.MObject()
            dagPath = om.MDagPath()
            selListIter.getDagPath(dagPath, components)

            if components.isNull():
                selListIter.next()
                continue

            compListFn = om.MFnComponent(components)
            compType = compListFn.componentType()

            if compType == om.MFn.kMeshPolygonComponent:
                compListFn = om.MFnSingleIndexedComponent(components)
                ids = om.MIntArray()
                compListFn.getElements(ids)
                selItem = SelectionItem(dagPath, ids)
                self.targetGeom.append(selItem)

            selListIter.next()

        if not self.targetGeom:
            self.ui_badSelectionWarning()
            return

        self.geometryData.generateGeometryInfo(self.targetGeom)
        self.selectValidGeometry()

    # noinspection PyUnusedLocal
    def ui_CHK_highlight_change(self, *args):
        if not self.targetGeom:
            return

        selList = om.MSelectionList()
        if self.ui_CHK_highlight.getValue():
            for obj in self.targetGeom:
                selList.add(obj.dagPath)
        # noinspection PyCallByClass,PyTypeChecker
        om.MGlobal.setHiliteList(selList)

    # noinspection PyUnusedLocal
    def selectValidGeometry(self, *args):
        _min = self.ui_FLTSLGRP_minAngle.getValue()
        _max = self.ui_FLTSLGRP_maxAngle.getValue()

        pm.mel.eval('changeSelectMode -component; setComponentPickMask "All" 0; setComponentPickMask "Facet" true;')
        self.ui_CHK_highlight_change(True)

        validEdges = self.geometryData.getValidEdges(_min, _max)
        # noinspection PyCallByClass,PyTypeChecker
        om.MGlobal.setActiveSelectionList(validEdges)

    # noinspection PyUnusedLocal,PyMethodMayBeStatic
    def ui_showHelp(self, *args):
        import webbrowser
        webbrowser.open('http://davydenko.info/edge_angle_grow/', new=0, autoraise=True)


class GeometryData:
    def __init__(self):

        self.polyData = []

    def generateGeometryInfo(self, objList):

        pi = math.pi
        connectedFaces = om.MIntArray()
        polyEdgesIds = om.MIntArray()
        edgeFaces = om.MIntArray()
        dummy = om.MScriptUtil()
        dummyIntPtr = dummy.asIntPtr()

        self.polyData = []

        for obj in objList:

            edgeIter = om.MItMeshEdge(obj.dagPath)
            faceIter = om.MItMeshPolygon(obj.dagPath)

            # face normal cache

            _mvector = om.MVector
            normalCache = [_mvector() for _ in xrange(faceIter.count())]
            while not faceIter.isDone():
                faceIter.getNormal(normalCache[faceIter.index()], om.MSpace.kWorld)
                faceIter.next()

            # edge angle cache

            edgeAnglesCache = array('d', [-1000] * edgeIter.count())
            i = 0
            while not edgeIter.isDone():

                cfLength = edgeIter.getConnectedFaces(connectedFaces)

                if cfLength == 2:
                    normal1 = normalCache[connectedFaces[0]]
                    normal2 = normalCache[connectedFaces[1]]
                    edgeAnglesCache[i] = normal1.angle(normal2) * 180 / pi

                i += 1
                edgeIter.next()

            # fill poly data

            objPolyData = ObjectPolyData()
            self.polyData.append(objPolyData)
            objPolyData.dagPath = obj.dagPath
            objPolyData.polygons = [PolyData() for _ in xrange(faceIter.count())]

            i = 0
            faceIter.reset()
            while not faceIter.isDone():

                polyData = objPolyData.polygons[i]
                faceIter.getEdges(polyEdgesIds)

                for edgeId in polyEdgesIds:

                    edgeIter.setIndex(edgeId, dummyIntPtr)
                    cfLength = edgeIter.getConnectedFaces(edgeFaces)

                    if cfLength == 2:
                        otherFace = edgeFaces[1] if edgeFaces[0] == i else edgeFaces[0]
                        polyData.connectedFaces[otherFace] = edgeAnglesCache[edgeId]

                i += 1
                faceIter.next()

            for p in obj.polyIds:
                objPolyData.polygons[p].selected = True
                objPolyData.polygons[p].initSelection = True

    def growSelection(self, _min, _max):

        for obj in self.polyData:

            polysToGrowNextIter = [i for i, poly in enumerate(obj.polygons) if poly.selected]

            while True:
                selectionWasGrown = False

                polysToGrow = polysToGrowNextIter
                polysToGrowNextIter = []

                for polyId in polysToGrow:
                    for polyNeighbourId in obj.polygons[polyId].connectedFaces:
                        if (
                                (_min <= obj.polygons[polyId].connectedFaces[polyNeighbourId] <= _max) and
                                (not obj.polygons[polyNeighbourId].selected)
                        ):
                            polysToGrowNextIter.append(polyNeighbourId)
                            obj.polygons[polyNeighbourId].selected = True
                            selectionWasGrown = True

                if not selectionWasGrown:
                    break

    def resetSelection(self):

        for obj in self.polyData:
            for poly in obj.polygons:
                poly.selected = poly.initSelection

    def getValidEdges(self, _min, _max):

        self.resetSelection()
        self.growSelection(_min, _max)

        selList = om.MSelectionList()
        compListFn = om.MFnSingleIndexedComponent()
        indexes = om.MIntArray()

        for obj in self.polyData:
            components = compListFn.create(om.MFn.kMeshPolygonComponent)
            indexes.clear()

            for i, poly in enumerate(obj.polygons):
                if poly.selected:
                    indexes.append(i)

            compListFn.addElements(indexes)
            selList.add(obj.dagPath, components)

        return selList


class PolyData:
    def __init__(self):
        self.selected = False
        self.initSelection = False
        self.connectedFaces = {}

    def __str__(self):
        endStr = '\n'
        outStr = ''
        outStr += 'initSelected = ' + str(self.initSelection) + ', selected = ' + str(self.selected) + endStr
        for key in self.connectedFaces:
            outStr += '[' + str(key) + '] = ' + str(self.connectedFaces[key]) + endStr
        return outStr


class ObjectPolyData:
    def __init__(self):
        self.dagPath = None
        self.polygons = []

    def __str__(self):
        endStr = '\n'
        outStr = ''
        outStr += 'DagPath = ' + self.dagPath.fullPathName() + endStr
        for i, poly in enumerate(self.polygons):
            outStr += 'polyId = ' + str(i) + endStr
            outStr += str(poly) + endStr
        return outStr


class SelectionItem:
    def __init__(self, dagPath, polyIds):
        self.dagPath = dagPath
        self.polyIds = polyIds

    def __str__(self):
        endStr = '\n'
        outStr = ''
        outStr += 'DagPath = ' + self.dagPath.fullPathName() + endStr
        for i, elem in enumerate(self.polyIds):
            outStr += 'polyIds[' + str(i) + '] = ' + str(self.polyIds[i]) + endStr
        return outStr


def run():
    SelectComponentByAngleUI()


