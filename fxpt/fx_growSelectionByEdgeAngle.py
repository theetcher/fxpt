import math
from array import array

from pymel.core import *

from fxpt.fx_prefsaver import PrefSaver, Serializers

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

        self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerOptVar(OPT_VAR_NAME))
        
        self.targetGeom = []
        self.geometryData = GeometryData()

        self.ui_createUI()
        self.ui_setTargetGeometry()

    def ui_createUI(self):
        self.winName = WIN_NAME
        self.winTitle = WIN_TITLE

        if window(WIN_NAME, exists=True):
            deleteUI(WIN_NAME, window=True)

        with window(
            WIN_NAME,
            title=WIN_TITLE,
            maximizeButton=False,
            menuBar=True,
            menuBarVisible=True
        ) as self.window:

            menu(label='Edit', tearOff=False)
            menuItem(label='Reset Settings', command=self.ui_resetSettings)
            menu(label='Help', tearOff=False)
            menuItem(label='Help on ' + WIN_TITLE, command=Callback(self.ui_showHelp, 1))
            menuItem(divider=True)
            menuItem(label='Script Information', command=Callback(self.ui_showHelp, 2))

            with formLayout() as self.ui_mainForm:

                with scrollLayout(childResizable=True) as self.ui_LAY_mainScroll:

                    with frameLayout(
                        label='Control Panel',
                        collapsable=True,
                        marginHeight=3,
                        borderStyle='etchedIn',
                        borderVisible=True
                    ) as self.ui_LAY_frameControlPanel:

                        with columnLayout(adjustableColumn=True):

                            with rowLayout(
                                numberOfColumns=2,
                                columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH],
                                columnAttach=[1, 'right', 5]
                            ):

                                text(label='Min Angle')

                                self.ui_FLTSLGRP_minAngle = floatSliderGrp(
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

                            with rowLayout(
                                numberOfColumns=2,
                                columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH],
                                columnAttach=[1, 'right', 5]
                            ):

                                text(label='Max Angle')

                                self.ui_FLTSLGRP_maxAngle = floatSliderGrp(
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

                            separator(style='in', height=10)

                            with rowLayout(
                                numberOfColumns=2,
                                columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH],
                                columnAttach=[1, 'right', 5]
                            ):
                                text(label='Highlight')

                                self.ui_CHK_highlight = checkBox(
                                    'ui_CHK_highlight',
                                    label='',
                                    changeCommand=self.ui_CHK_highlight_change
                                )

                self.ui_BTN_select = button(
                    label=UI_APPLY_BUTTON_STRING,
                    command=self.ui_setTargetGeometry
                )

                self.ui_BTN_close = button(
                    label='Close',
                    command=self.ui_close
                )

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
        refresh()

    # noinspection PyMethodMayBeStatic
    def ui_initSettings(self):
        print('ui_initSettings()')
        self.prefSaver.addControl(self.ui_FLTSLGRP_minAngle, PrefSaver.UIType.PMFloatSliderGrp, 0)
        self.prefSaver.addControl(self.ui_FLTSLGRP_maxAngle, PrefSaver.UIType.PMFloatSliderGrp, 45)
        self.prefSaver.addControl(self.ui_CHK_highlight, PrefSaver.UIType.PMCheckBox, True)

    def ui_loadSettings(self):
        print('ui_loadSettings()')
        self.prefSaver.loadPrefs()

    def ui_saveSettings(self):
        print('ui_saveSettings()')
        self.prefSaver.savePrefs()

    # noinspection PyUnusedLocal
    def ui_resetSettings(self, *args):
        print('ui_resetSettings()')
        self.prefSaver.resetPrefs()
        self.selectValidGeometry()

    # noinspection PyUnusedLocal
    def ui_close(self, *args):
        self.ui_saveSettings()
        if window(WIN_NAME, exists=True):
            deleteUI(WIN_NAME, window=True)

    # noinspection PyMethodMayBeStatic
    def ui_badSelectionWarning(self):
        confirmDialog(
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

        mel.eval('changeSelectMode -component; setComponentPickMask "All" 0; setComponentPickMask "Facet" true;')
        self.ui_CHK_highlight_change(True)

        validEdges = self.geometryData.getValidEdges(_min, _max)
        # noinspection PyCallByClass,PyTypeChecker
        om.MGlobal.setActiveSelectionList(validEdges)

    # noinspection PyUnusedLocal
    def ui_showHelp(self, tab, *args):

        if window(WIN_HELPNAME, exists=True):
            deleteUI(WIN_HELPNAME, window=True)

        with window(
            WIN_HELPNAME,
            title=WIN_HELPTITLE,
            maximizeButton=False
        ) as self.helpWindow:

            with formLayout() as self.ui_LAY_formMainHelp:

                with tabLayout(
                    innerMarginWidth=50,
                    innerMarginHeight=50,
                    childResizable=True
                ) as self.ui_LAY_tabHelp:

                    with formLayout() as self.ui_LAY_formHelpMargin:

                        with scrollLayout(childResizable=True) as self.ui_LAY_scrollHelp:

                            self.ui_LAY_formHelpMargin.attachForm(self.ui_LAY_scrollHelp, 'top', 2)
                            self.ui_LAY_formHelpMargin.attachForm(self.ui_LAY_scrollHelp, 'left', 2)
                            self.ui_LAY_formHelpMargin.attachForm(self.ui_LAY_scrollHelp, 'right', 2)
                            self.ui_LAY_formHelpMargin.attachForm(self.ui_LAY_scrollHelp, 'bottom', 2)

                            with frameLayout(
                                label='Help on ' + WIN_TITLE,
                                collapsable=False,
                                marginHeight=3,
                                borderStyle='etchedIn',
                                borderVisible=True
                            ):

                                with rowLayout(columnAttach=[1, 'both', 10]):

                                    self.ui_TXT_help = text('', align='center')

                    with formLayout() as self.ui_LAY_formAboutMargin:

                        with scrollLayout(childResizable=True) as self.ui_LAY_scrollAbout:

                            self.ui_LAY_formAboutMargin.attachForm(self.ui_LAY_scrollAbout, 'top', 2)
                            self.ui_LAY_formAboutMargin.attachForm(self.ui_LAY_scrollAbout, 'left', 2)
                            self.ui_LAY_formAboutMargin.attachForm(self.ui_LAY_scrollAbout, 'right', 2)
                            self.ui_LAY_formAboutMargin.attachForm(self.ui_LAY_scrollAbout, 'bottom', 2)

                            with frameLayout(
                                label='About ' + WIN_TITLE,
                                collapsable=False,
                                marginHeight=3,
                                borderStyle='etchedIn',
                                borderVisible=True
                            ):

                                with rowLayout(
                                    columnAttach=[1, 'both', 10]
                                ):

                                    self.ui_TXT_about = text('', align='center')

                self.ui_BTN_closeHelp = button(
                    'Close',
                    command=lambda x: deleteUI(WIN_HELPNAME)
                )

            self.ui_LAY_formMainHelp.attachForm(self.ui_LAY_tabHelp, 'top', 2)
            self.ui_LAY_formMainHelp.attachForm(self.ui_LAY_tabHelp, 'left', 2)
            self.ui_LAY_formMainHelp.attachForm(self.ui_LAY_tabHelp, 'right', 2)
            self.ui_LAY_formMainHelp.attachControl(self.ui_LAY_tabHelp, 'bottom', 2, self.ui_BTN_closeHelp)

            self.ui_LAY_formMainHelp.attachNone(self.ui_BTN_closeHelp, 'top')
            self.ui_LAY_formMainHelp.attachForm(self.ui_BTN_closeHelp, 'left', 2)
            self.ui_LAY_formMainHelp.attachForm(self.ui_BTN_closeHelp, 'right', 2)
            self.ui_LAY_formMainHelp.attachForm(self.ui_BTN_closeHelp, 'bottom', 2)

            tabLayout(
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
This tool will grow polygon selection based on "Edge Angle",
i.e. angle between normals of 2 polygons sharing particular edge.
In other words. You've got selected polygon(s). Adjacent polygons
will be added to selection (selection will be grown)
if Edge Angle between polygons is in some range (set in UI).
This growing will proceed until there is no valid polygons to grow.
Similar tool called "Select by angle" can be found in 3DSMAX.
Non-manifold geometry is not supported (meshes with edges sharing more than 2 polygons).

- Workflow -
Select one or more starting polygons on one or several polymeshes and run the script.
Tool Control Panel will popup and
grow selection will be performed based on Control Panel settings.
You can tweak options and interactively see the result.
If you want to select other starting polygons or
may be switch to different meshes
and don't want to close the window,
choose some polygons and press "Set Target Geometry".

- Min and Max Angle -
Polygons will be selected if Edge Angle is between theese values.

- Highlight -
Toggles object highlight.
Sometimes its hard to see components selected when object highlight is on.
Use this check box to unhighlight mesh objects and
clearly observe only polygon selection.

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


