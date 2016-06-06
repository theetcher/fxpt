import maya.cmds as m
import pymel.core as pm

from . import cfg, com, normalizer

SCRIPT_VERSION = 'v1.0'
SCRIPT_NAME = 'Smart Normal'
WIN_NAME = 'fx_smartNormal_win'
WIN_TITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION
UI_LABEL_WIDTH = 120
UI_INPUT_WIDTH = 240
UI_APPLY_BUTTON_STRING = 'Set Target Geometry'


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

                                            pm.text(label='Curvature Threshold')

                                            pm.setUITemplate('DefaultTemplate', popTemplate=True)  # strange slider group visual with default template

                                            self.ui_FLTSLGRP_curveThresh = pm.floatSliderGrp(
                                                'ui_FLTSLGRP_curveThresh',
                                                field=True,
                                                minValue=0.001,
                                                maxValue=0.2,
                                                fieldMinValue=0.001,
                                                fieldMaxValue=10,
                                                value=0.001,
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
                                                maxValue=180,
                                                fieldMinValue=0,
                                                fieldMaxValue=180,
                                                value=0,
                                                step=0.001,
                                                fieldStep=0.001,
                                                sliderStep=0.001,
                                                changeCommand=self.dummyFunc,
                                                dragCommand=self.dummyFunc
                                            )

                                            pm.setUITemplate('DefaultTemplate', pushTemplate=True)

                                if cfg.DEBUG:

                                    with pm.frameLayout(
                                            label='Debug',
                                            collapsable=True,
                                            collapse=False,
                                            marginHeight=3,
                                    ):

                                        with pm.columnLayout(adjustableColumn=True):
                                            with pm.rowLayout(numberOfColumns=2, columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH], columnAttach=[1, 'right', 5]):

                                                pm.text(label='Display Curvature')

                                                self.ui_CHK_displayCurvature = pm.checkBox(
                                                    'ui_CHK_highlight',
                                                    label='',
                                                    changeCommand=self.ui_CHK_displayCurvature_change
                                                )

                                            with pm.rowLayout(numberOfColumns=2, columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH], columnAttach=[1, 'right', 5]):

                                                pm.text(label='Max Value')

                                                pm.setUITemplate('DefaultTemplate', popTemplate=True)  # strange slider group visual with default template

                                                self.ui_FLTSLGRP_curvatureMaxValue = pm.floatSliderGrp(
                                                    'ui_FLTSLGRP_curvatureMaxValue',
                                                    field=True,
                                                    minValue=0.001,
                                                    maxValue=1,
                                                    fieldMinValue=0.001,
                                                    fieldMaxValue=10,
                                                    value=1,
                                                    step=0.001,
                                                    fieldStep=0.001,
                                                    sliderStep=0.001,
                                                    changeCommand=self.ui_FLTSLGRP_curvatureMaxValue_change,
                                                    dragCommand=self.ui_FLTSLGRP_curvatureMaxValue_change
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

    def ui_CHK_displayCurvature_change(self, arg):
        pass

    def getCurvatureThresholdValue(self):
        return self.ui_FLTSLGRP_curveThresh.getValue()

    def getCurvatureDisplayMaxValue(self):
        return self.ui_FLTSLGRP_curvatureMaxValue.getValue()

    def ui_FLTSLGRP_curveThresh_change(self, arg):
        self.processNormalizers()

    def ui_FLTSLGRP_curvatureMaxValue_change(self, arg):
        self.updateNormalizersDisplay()

    def processNormalizers(self):
        for n in self.normalizers:
            n.process(self.getCurvatureThresholdValue(), self.getCurvatureDisplayMaxValue())

    def updateNormalizersDisplay(self):
        for n in self.normalizers:
            n.updateDisplay(self.getCurvatureThresholdValue(), self.getCurvatureDisplayMaxValue())

    def dummyFunc(self, *args, **kwargs):
        pass

    def setTargetGeometry(self):
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

        self.processNormalizers()
