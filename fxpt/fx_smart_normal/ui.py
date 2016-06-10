import maya.cmds as m
import pymel.core as pm

from . import com, geom_processor, backuper, prefsaver

SCRIPT_VERSION = 'v1.0'
SCRIPT_NAME = 'Smart Normal'
WIN_NAME = 'fx_smartNormal_win'
WIN_TITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION
UI_LABEL_WIDTH = 120
UI_INPUT_WIDTH = 240


class Parameters(object):
    curveThresh = 0.09
    growAngle = 5
    dispCurve = False
    curveScale = 1


# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic,PyUnusedLocal
class SmartNormalUI(object):
    """
    :type processors: list[geom_processor.GeomProcessor]
    :type backupers: list[backuper.Backuper]
    :type prefSaver: prefsaver.PrefSaver
    :type accept: bool
    """
    def __init__(self):
        self.processors = []
        self.backupers = []
        self.accept = False
        self.prefSaver = prefsaver.PrefSaver(Parameters)

        self.ui_createUI()

        self.prefSaver.prefsToParams()
        self.syncUiToParams()

        self.initGeometry()

    def ui_createUI(self):
        self.winName = WIN_NAME
        self.winTitle = WIN_TITLE

        if pm.window(WIN_NAME, exists=True):
            pm.deleteUI(WIN_NAME, window=True)

        with pm.window(WIN_NAME, title=WIN_TITLE, maximizeButton=False, menuBar=True, menuBarVisible=True) as self.window:

            pm.setUITemplate('DefaultTemplate', pushTemplate=True)

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

                                        with pm.rowLayout(numberOfColumns=2, columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH], columnAttach=[1, 'right', 5]):

                                            pm.text(label='Curvature Threshold')

                                            pm.setUITemplate('DefaultTemplate', popTemplate=True)  # strange slider group visual with default template

                                            self.ui_FLTSLGRP_curveThresh = pm.floatSliderGrp(
                                                'ui_FLTSLGRP_curveThresh',
                                                field=True,
                                                minValue=0.001,
                                                maxValue=0.2,
                                                fieldMinValue=0.001,
                                                fieldMaxValue=10,
                                                value=0.09,
                                                step=0.001,
                                                fieldStep=0.001,
                                                sliderStep=0.001,
                                                changeCommand=self.ui_FLTSLGRP_curveThresh_change,
                                                dragCommand=self.ui_FLTSLGRP_curveThresh_change
                                            )

                                            pm.setUITemplate('DefaultTemplate', pushTemplate=True)

                                        with pm.rowLayout(numberOfColumns=2, columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH], columnAttach=[1, 'right', 5]):

                                            pm.text(label='Grow Angle')

                                            pm.setUITemplate('DefaultTemplate', popTemplate=True)  # strange slider group visual with default template

                                            self.ui_FLTSLGRP_growAngle = pm.floatSliderGrp(
                                                'ui_FLTSLGRP_growAngle',
                                                field=True,
                                                minValue=0,
                                                maxValue=10,
                                                fieldMinValue=0,
                                                fieldMaxValue=30,
                                                value=5,
                                                step=0.001,
                                                fieldStep=0.001,
                                                sliderStep=0.001,
                                                changeCommand=self.ui_FLTSLGRP_growAngle_change,
                                                dragCommand=self.ui_FLTSLGRP_growAngle_change
                                            )

                                            pm.setUITemplate('DefaultTemplate', pushTemplate=True)

                                with pm.frameLayout(
                                        label='Display',
                                        collapsable=True,
                                        collapse=False,
                                        marginHeight=3,
                                ):

                                    with pm.columnLayout(adjustableColumn=True):
                                        with pm.rowLayout(numberOfColumns=2, columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH], columnAttach=[1, 'right', 5]):

                                            pm.text(label='Display Curvature')

                                            self.ui_CHK_displayCurve = pm.checkBox(
                                                'ui_CHK_highlight',
                                                label='',
                                                changeCommand=self.ui_CHK_displayCurve_change
                                            )

                                        with pm.rowLayout(numberOfColumns=2, columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH], columnAttach=[1, 'right', 5]):

                                            pm.text(label='Curvature Scale')

                                            pm.setUITemplate('DefaultTemplate', popTemplate=True)  # strange slider group visual with default template

                                            self.ui_FLTSLGRP_curveScale = pm.floatSliderGrp(
                                                'ui_FLTSLGRP_curveScale',
                                                field=True,
                                                minValue=0.001,
                                                maxValue=1,
                                                fieldMinValue=0.001,
                                                fieldMaxValue=10,
                                                value=1,
                                                step=0.001,
                                                fieldStep=0.001,
                                                sliderStep=0.001,
                                                changeCommand=self.ui_FLTSLGRP_curveScale_change,
                                                dragCommand=self.ui_FLTSLGRP_curveScale_change
                                            )

                                            pm.setUITemplate('DefaultTemplate', pushTemplate=True)

                self.ui_BTN_ok = pm.button(
                    label='OK',
                    command=self.onOkClicked
                )

                self.ui_BTN_cancel = pm.button(
                    label='Cancel',
                    command=self.onCancelClicked
                )

            self.ui_LAY_attachForm.attachForm(self.ui_TAB_inner, 'top', 0)
            self.ui_LAY_attachForm.attachForm(self.ui_TAB_inner, 'left', 0)
            self.ui_LAY_attachForm.attachForm(self.ui_TAB_inner, 'right', 0)
            self.ui_LAY_attachForm.attachForm(self.ui_TAB_inner, 'bottom', 0)

            self.ui_LAY_mainForm.attachForm(self.ui_TAB_top, 'top', 0)
            self.ui_LAY_mainForm.attachForm(self.ui_TAB_top, 'left', 0)
            self.ui_LAY_mainForm.attachForm(self.ui_TAB_top, 'right', 0)
            self.ui_LAY_mainForm.attachControl(self.ui_TAB_top, 'bottom', 5, self.ui_BTN_ok)

            self.ui_LAY_mainForm.attachNone(self.ui_BTN_ok, 'top')
            self.ui_LAY_mainForm.attachForm(self.ui_BTN_ok, 'left', 5)
            self.ui_LAY_mainForm.attachPosition(self.ui_BTN_ok, 'right', 2, 50)
            self.ui_LAY_mainForm.attachForm(self.ui_BTN_ok, 'bottom', 5)

            self.ui_LAY_mainForm.attachNone(self.ui_BTN_cancel, 'top')
            self.ui_LAY_mainForm.attachPosition(self.ui_BTN_cancel, 'left', 2, 50)
            self.ui_LAY_mainForm.attachForm(self.ui_BTN_cancel, 'right', 5)
            self.ui_LAY_mainForm.attachForm(self.ui_BTN_cancel, 'bottom', 5)

        pm.setUITemplate('DefaultTemplate', popTemplate=True)

        pm.scriptJob(uiDeleted=(self.window, self.onUiDeleted))

        self.window.show()
        m.refresh()

    def close(self):
        if pm.window(WIN_NAME, exists=True):
            pm.deleteUI(WIN_NAME, window=True)

    def onCancelClicked(self, *args):
        self.accept = False
        self.close()

    def onOkClicked(self, *args):
        self.accept = True
        self.close()

    def onUiDeleted(self):
        if self.accept:
            self.prefSaver.paramsToPrefs()
            for b in self.backupers:
                b.restoreDisplay()
        else:
            for b in self.backupers:
                b.restoreAll()

    def syncUiToParams(self):
        self.ui_FLTSLGRP_curveThresh.setValue(Parameters.curveThresh)
        self.ui_FLTSLGRP_growAngle.setValue(Parameters.growAngle)
        self.ui_CHK_displayCurve.setValue(Parameters.dispCurve)
        self.ui_FLTSLGRP_curveScale.setValue(Parameters.curveScale)

    def gatherParameters(self):
        Parameters.curveThresh = self.ui_FLTSLGRP_curveThresh.getValue()
        Parameters.growAngle = self.ui_FLTSLGRP_growAngle.getValue()
        Parameters.dispCurve = self.ui_CHK_displayCurve.getValue()
        Parameters.curveScale = self.ui_FLTSLGRP_curveScale.getValue()

    def ui_FLTSLGRP_curveThresh_change(self, arg):
        self.gatherParameters()
        self.processAll()

    def ui_FLTSLGRP_growAngle_change(self, arg):
        self.gatherParameters()
        self.processAll()

    def ui_CHK_displayCurve_change(self, state):
        self.gatherParameters()
        if not state:
            for b in self.backupers:
                b.restoreDisplay()
        self.processDisplay()

    def ui_FLTSLGRP_curveScale_change(self, arg):
        self.gatherParameters()
        self.processDisplay()

    def processAll(self):
        for n in self.processors:
            n.processAll()

    def processDisplay(self):
        for n in self.processors:
            n.processDisplay()

    def initGeometry(self):
        selection = m.ls(sl=True)

        meshes = m.ls(
            selection=True,
            long=True,
            dagObjects=True,
            allPaths=True,
            type='mesh',
            noIntermediate=True
        )
        if meshes:
            for mesh in meshes:
                transform = com.getParent(mesh)
                if transform:
                    self.backupers.append(backuper.Backuper(mesh))

                    m.polyNormalPerVertex(transform, ufn=True)
                    m.polySoftEdge(transform, a=180, ch=False)

                    geomProcessor = geom_processor.GeomProcessor(mesh)
                    geomProcessor.params = Parameters
                    self.processors.append(geomProcessor)
        else:
            pm.confirmDialog(
                title='Error',
                message='Invalid selection.\nSelect at least one polygon object and press "' + UI_APPLY_BUTTON_STRING + '"`.',
                button=['OK'],
                defaultButton='OK',
                icon='critical'
            )
            return

        m.select(selection, r=True)
        self.processAll()

    def backup(self, mesh):
        pass
