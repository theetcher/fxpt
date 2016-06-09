import maya.cmds as m
import pymel.core as pm

from . import com, normalizer

SCRIPT_VERSION = 'v1.0'
SCRIPT_NAME = 'Smart Normal'
WIN_NAME = 'fx_smartNormal_win'
WIN_TITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION
UI_LABEL_WIDTH = 120
UI_INPUT_WIDTH = 240
UI_APPLY_BUTTON_STRING = 'Set Target Geometry'


class Parameters(object):
    envelope = None
    curveThresh = None
    areaTolerance = None
    growAngle = None
    dispCurve = None
    curveScale = None


# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic,PyUnusedLocal
class SmartNormalUI(object):
    """
    :type normalizers: list[normalizer.Normalizer]
    """
    def __init__(self):
        self.normalizers = []
        self.ui_createUI()
        self.setTargetGeometry()

    def ui_createUI(self):
        self.winName = WIN_NAME
        self.winTitle = WIN_TITLE

        if pm.window(WIN_NAME, exists=True):
            pm.deleteUI(WIN_NAME, window=True)

        with pm.window(WIN_NAME, title=WIN_TITLE, maximizeButton=False, menuBar=True, menuBarVisible=True) as window:

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

                                            pm.text(label='Envelope')

                                            pm.setUITemplate('DefaultTemplate', popTemplate=True)  # strange slider group visual with default template

                                            self.ui_FLTSLGRP_envelope = pm.floatSliderGrp(
                                                'ui_FLTSLGRP_envelope',
                                                field=True,
                                                minValue=0,
                                                maxValue=1,
                                                fieldMinValue=0,
                                                fieldMaxValue=1,
                                                value=1,
                                                step=0.001,
                                                fieldStep=0.001,
                                                sliderStep=0.001,
                                                changeCommand=self.ui_FLTSLGRP_envelope_change,
                                                dragCommand=self.ui_FLTSLGRP_envelope_change
                                            )

                                            pm.setUITemplate('DefaultTemplate', pushTemplate=True)

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

                                            pm.text(label='Area Tolerance')

                                            pm.setUITemplate('DefaultTemplate', popTemplate=True)  # strange slider group visual with default template

                                            self.ui_FLTSLGRP_areaTolerance = pm.floatSliderGrp(
                                                'ui_FLTSLGRP_areaTolerance',
                                                field=True,
                                                minValue=0,
                                                maxValue=1,
                                                fieldMinValue=0,
                                                fieldMaxValue=1,
                                                value=0.01,
                                                step=0.001,
                                                fieldStep=0.001,
                                                sliderStep=0.001,
                                                changeCommand=self.ui_FLTSLGRP_areaTolerance_change,
                                                dragCommand=self.ui_FLTSLGRP_areaTolerance_change
                                            )

                                            pm.setUITemplate('DefaultTemplate', pushTemplate=True)

                                        with pm.rowLayout(numberOfColumns=2, columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH], columnAttach=[1, 'right', 5]):

                                            pm.text(label='Grow Angle')

                                            pm.setUITemplate('DefaultTemplate', popTemplate=True)  # strange slider group visual with default template

                                            self.ui_FLTSLGRP_growAngle = pm.floatSliderGrp(
                                                'ui_FLTSLGRP_growAngle',
                                                field=True,
                                                minValue=0,
                                                maxValue=30,
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

        window.show()
        m.refresh()

    def ui_close(self, *args):
        if pm.window(WIN_NAME, exists=True):
            pm.deleteUI(WIN_NAME, window=True)

    def ui_setTargetGeometry(self, *args):
        self.setTargetGeometry()

    def gatherParameters(self):
        Parameters.envelope = self.ui_FLTSLGRP_envelope.getValue()
        Parameters.curveThresh = self.ui_FLTSLGRP_curveThresh.getValue()
        Parameters.areaTolerance = self.ui_FLTSLGRP_areaTolerance.getValue()
        Parameters.growAngle = self.ui_FLTSLGRP_growAngle.getValue()
        Parameters.dispCurve = self.ui_CHK_displayCurve.getValue()
        Parameters.curveScale = self.ui_FLTSLGRP_curveScale.getValue()

    def ui_FLTSLGRP_envelope_change(self, arg):
        self.processNormalizers()

    def ui_FLTSLGRP_curveThresh_change(self, arg):
        self.processNormalizers()

    def ui_FLTSLGRP_areaTolerance_change(self, arg):
        self.processNormalizers()

    def ui_FLTSLGRP_growAngle_change(self, arg):
        self.processNormalizers()

    def ui_CHK_displayCurve_change(self, arg):
        self.updateNormalizersDisplay()

    def ui_FLTSLGRP_curveScale_change(self, arg):
        self.updateNormalizersDisplay()

    def processNormalizers(self):
        self.gatherParameters()
        for n in self.normalizers:
            n.process(Parameters)

    def updateNormalizersDisplay(self):
        self.gatherParameters()
        for n in self.normalizers:
            n.updateDisplay(Parameters)

    def dummyFunc(self, *args, **kwargs):
        pass

    def setTargetGeometry(self):
        selection = m.ls(sl=True)

        self.normalizers = []
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
                transform = com.getParent(x)
                m.polyNormalPerVertex(transform, ufn=True)
                m.polySoftEdge(transform, a=180)
                if transform:
                    self.normalizers.append(normalizer.Normalizer(x))
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
        self.processNormalizers()
