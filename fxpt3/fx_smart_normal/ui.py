import maya.cmds as m

from fxpt3.fx_smart_normal import com, geom_processor, backuper, prefsaver

SCRIPT_VERSION = 'v1.0'
SCRIPT_NAME = 'Smart Normal'
WIN_NAME = 'fx_smartNormal_win'
WIN_TITLE = SCRIPT_NAME + ' ' + SCRIPT_VERSION
UI_LABEL_WIDTH = 120
UI_INPUT_WIDTH = 240

CTRL_CURVE_THRESH = 'ui_FLTSLGRP_curveThresh'
CTRL_GROW_ANGLE = 'ui_FLTSLGRP_growAngle'
CTRL_DISPLAY_CURVE = 'ui_CHK_highlight'
CTRL_CURVE_SCALE = 'ui_FLTSLGRP_curveScale'


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
        self.initGeometry()

        if not self.processors:
            return

        self.accept = False
        self.prefSaver = prefsaver.PrefSaver(Parameters)

        self.ui_createUI()

        self.prefSaver.prefsToParams()
        self.syncUiToParams()
        self.processAll()

    def ui_createRow(self):
        return m.rowLayout(numberOfColumns=2, columnWidth2=[UI_LABEL_WIDTH, UI_INPUT_WIDTH], columnAttach=[1, 'right', 5])

    def ui_createSliderGrp(self, name, minValue, maxValue, fieldMinValue, fieldMaxValue, value, command):
        m.setUITemplate('DefaultTemplate', popTemplate=True)  # strange slider group visual with default template
        ctrl = m.floatSliderGrp(
            name,
            field=True,
            minValue=minValue,
            maxValue=maxValue,
            fieldMinValue=fieldMinValue,
            fieldMaxValue=fieldMaxValue,
            value=value,
            step=0.001,
            fieldStep=0.001,
            sliderStep=0.001,
            changeCommand=command,
            dragCommand=command
        )
        m.setUITemplate('DefaultTemplate', pushTemplate=True)
        return ctrl

    def ui_createUI(self):
        self.winName = WIN_NAME
        self.winTitle = WIN_TITLE

        self.close()

        self.window = m.window(WIN_NAME, title=WIN_TITLE, maximizeButton=False, menuBar=True, menuBarVisible=True)

        m.setUITemplate('DefaultTemplate', pushTemplate=True)

        self.ui_LAY_mainForm = m.formLayout()

        self.ui_TAB_top = m.tabLayout(tabsVisible=False)
        m.tabLayout(self.ui_TAB_top, e=True, height=1)

        self.ui_LAY_attachForm = m.formLayout()

        self.ui_TAB_inner = m.tabLayout(tabsVisible=False, scrollable=True, innerMarginWidth=4)

        self.ui_LAY_mainColumn = m.columnLayout(adjustableColumn=True)

        # Control Panel
        m.frameLayout(label='Control Panel', collapsable=True, collapse=False, marginHeight=3)
        m.columnLayout(adjustableColumn=True)

        self.ui_createRow()
        m.text(label='Curvature Threshold')
        self.ui_FLTSLGRP_curveThresh = self.ui_createSliderGrp(
            CTRL_CURVE_THRESH, 0.001, 0.2, 0.001, 10, 0.09, self.ui_FLTSLGRP_curveThresh_change)
        m.setParent('..')  # rowLayout

        self.ui_createRow()
        m.text(label='Grow Angle')
        self.ui_FLTSLGRP_growAngle = self.ui_createSliderGrp(
            CTRL_GROW_ANGLE, 0, 10, 0, 30, 5, self.ui_FLTSLGRP_growAngle_change)
        m.setParent('..')  # rowLayout

        m.setParent('..')  # columnLayout
        m.setParent('..')  # frameLayout

        # Display
        m.frameLayout(label='Display', collapsable=True, collapse=False, marginHeight=3)
        m.columnLayout(adjustableColumn=True)

        self.ui_createRow()
        m.text(label='Display Curvature')
        self.ui_CHK_displayCurve = m.checkBox(
            CTRL_DISPLAY_CURVE,
            label='',
            changeCommand=self.ui_CHK_displayCurve_change
        )
        m.setParent('..')  # rowLayout

        self.ui_createRow()
        m.text(label='Curvature Scale')
        self.ui_FLTSLGRP_curveScale = self.ui_createSliderGrp(
            CTRL_CURVE_SCALE, 0.001, 1, 0.001, 10, 1, self.ui_FLTSLGRP_curveScale_change)
        m.setParent('..')  # rowLayout

        m.setParent('..')  # columnLayout
        m.setParent('..')  # frameLayout

        m.setParent('..')  # ui_LAY_mainColumn
        m.setParent('..')  # ui_TAB_inner
        m.setParent('..')  # ui_LAY_attachForm
        m.setParent('..')  # ui_TAB_top

        self.ui_BTN_ok = m.button(label='OK', command=self.onOkClicked)
        self.ui_BTN_cancel = m.button(label='Cancel', command=self.onCancelClicked)

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
                (self.ui_BTN_ok, 'left', 5),
                (self.ui_BTN_ok, 'bottom', 5),
                (self.ui_BTN_cancel, 'right', 5),
                (self.ui_BTN_cancel, 'bottom', 5),
            ],
            attachControl=[
                (self.ui_TAB_top, 'bottom', 5, self.ui_BTN_ok),
            ],
            attachPosition=[
                (self.ui_BTN_ok, 'right', 2, 50),
                (self.ui_BTN_cancel, 'left', 2, 50),
            ],
            attachNone=[
                (self.ui_BTN_ok, 'top'),
                (self.ui_BTN_cancel, 'top'),
            ]
        )

        m.setUITemplate('DefaultTemplate', popTemplate=True)

        m.scriptJob(uiDeleted=(self.window, self.onUiDeleted))

        m.showWindow(self.window)
        m.refresh()

    def close(self):
        if m.window(WIN_NAME, exists=True):
            m.deleteUI(WIN_NAME, window=True)

    def onCancelClicked(self, *args):
        self.accept = False
        self.close()

    def onOkClicked(self, *args):
        self.accept = True
        self.close()

    def onUiDeleted(self):
        self.clearDisplay()
        if self.accept:
            self.prefSaver.paramsToPrefs()
            for b in self.backupers:
                b.restoreDisplay()
                b.deleteBackup()
        else:
            for b in self.backupers:
                b.restoreAll()

    def syncUiToParams(self):
        m.floatSliderGrp(self.ui_FLTSLGRP_curveThresh, e=True, value=Parameters.curveThresh)
        m.floatSliderGrp(self.ui_FLTSLGRP_growAngle, e=True, value=Parameters.growAngle)
        m.checkBox(self.ui_CHK_displayCurve, e=True, value=Parameters.dispCurve)
        m.floatSliderGrp(self.ui_FLTSLGRP_curveScale, e=True, value=Parameters.curveScale)

    def gatherParameters(self):
        Parameters.curveThresh = m.floatSliderGrp(self.ui_FLTSLGRP_curveThresh, q=True, value=True)
        Parameters.growAngle = m.floatSliderGrp(self.ui_FLTSLGRP_growAngle, q=True, value=True)
        Parameters.dispCurve = m.checkBox(self.ui_CHK_displayCurve, q=True, value=True)
        Parameters.curveScale = m.floatSliderGrp(self.ui_FLTSLGRP_curveScale, q=True, value=True)

    def ui_FLTSLGRP_curveThresh_change(self, *args):
        self.gatherParameters()
        self.processAll()

    def ui_FLTSLGRP_growAngle_change(self, *args):
        self.gatherParameters()
        self.processAll()

    def ui_CHK_displayCurve_change(self, *args):
        self.gatherParameters()
        if not Parameters.dispCurve:
            self.clearDisplay()
            for b in self.backupers:
                b.restoreDisplay()
        self.processDisplay()

    def ui_FLTSLGRP_curveScale_change(self, *args):
        self.gatherParameters()
        self.processDisplay()

    def processAll(self):
        for n in self.processors:
            n.processAll()

    def processDisplay(self):
        for n in self.processors:
            n.processDisplay()

    def clearDisplay(self):
        for n in self.processors:
            n.clearDisplay()

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
        if not meshes:
            self.showError('Invalid selection. Select at least one mesh.')
            return

        try:
            for mesh in meshes:
                transform = com.getParent(mesh)
                if transform:
                    self.backupers.append(backuper.Backuper(mesh, transform))
                    m.polyNormalPerVertex(mesh, ufn=True)
                    m.polySoftEdge(transform, a=180, ch=False)

                    geomProcessor = geom_processor.GeomProcessor(mesh)
                    geomProcessor.params = Parameters
                    self.processors.append(geomProcessor)
        except (AssertionError, RuntimeError) as e:
            # put back the meshes already modified, so a failure doesn't leave unlocked normals and hidden copies behind
            for b in self.backupers:
                b.restoreAll()
            self.backupers = []
            self.processors = []
            self.showError(str(e))
            return
        finally:
            existing = [s for s in selection if m.objExists(s)]
            if existing:
                m.select(existing, r=True)
            else:
                m.select(cl=True)

    def showError(self, message):
        m.confirmDialog(
            title='Error',
            message=message,
            button=['OK'],
            defaultButton='OK',
            icon='critical'
        )
