import maya.cmds as m
import pymel.core as pm
import random

from fxpt.fx_prefsaver import PrefSaver, Serializers

WIN_NAME = 'fx_transformRandomizerWin'
WIN_TITLE = 'Transform Randomizer v1.0'
WIN_HELP_NAME = 'fx_transformRandomizerHelpWin'
WIN_HELP_TITLE = WIN_TITLE + ' Help'
OPT_VAR_NAME = 'fx_randomizer_prefs'


# noinspection PyMethodMayBeStatic,PyAttributeOutsideInit
class RandomizerUI(object):
    def __init__(self):

        ui_labelWidth = 140
        ui_inputWidth = 240

        if pm.window(WIN_NAME, exists=True):
            pm.deleteUI(WIN_NAME, window=True)

        with pm.window(
            WIN_NAME,
            title=WIN_TITLE,
            maximizeButton=False,
            menuBar=True,
            menuBarVisible=True
        ) as self.window:

            pm.menu(label='Edit', tearOff=False)
            pm.menuItem(label='Reset Settings', command=self.ui_resetSettings)
            pm.menu(label='Help', tearOff=False)
            pm.menuItem(label='Help on ' + WIN_TITLE, command=pm.Callback(self.ui_showHelp, 1))
            pm.menuItem(divider=True)
            pm.menuItem(label='Script Information', command=pm.Callback(self.ui_showHelp, 2))

            with pm.formLayout() as self.ui_mainForm:

                with pm.scrollLayout(childResizable=True) as self.ui_LAY_mainScroll:

                    with pm.columnLayout(adjustableColumn=True) as self.ui_LAY_mainColumn:

                        with pm.frameLayout(
                            label='Control Panel',
                            collapsable=True,
                            marginHeight=3,
                            borderStyle='etchedIn',
                            borderVisible=True
                        ) as self.ui_LAY_frameControlPanel:

                            with pm.rowColumnLayout(
                                numberOfColumns=12,
                                rowSpacing=[1, 5],
                                #            Label       X       Y         Z       XYZ      Mag     Sep      Reset     Bias      Sep       Min       Max
                                columnWidth=[(1, 60), (2, 20), (3, 20), (4, 20), (5, 76), (6, 60), (7, 20), (8, 20), (9, 120), (10, 20), (11, 60), (12, 60)]
                            ) as self.ui_LAY_mainRowColumn:

                                #----- Header Row -----

                                pm.separator(style='none')
                                pm.separator(style='none')
                                pm.separator(style='none')
                                pm.separator(style='none')
                                pm.separator(style='none')
                                pm.text(label='Magnitude', )
                                pm.separator(style='none')
                                pm.separator(style='none')
                                pm.text(label='Bias', )
                                pm.separator(style='none')
                                pm.text(label='Min', )
                                pm.text(label='Max', )

                                #----- Translate Row -----

                                pm.text(label='Translate ', align='right')
                                pm.button(label='X', command=pm.Callback(self.randomizeTranslate, ['tx']))
                                pm.button(label='Y', command=pm.Callback(self.randomizeTranslate, ['ty']))
                                pm.button(label='Z', command=pm.Callback(self.randomizeTranslate, ['tz']))
                                pm.button(label='XYZ', command=pm.Callback(self.randomizeTranslate, ['tx', 'ty', 'tz']))
                                self.ui_FLTFLD_translateMagnitude = pm.floatField('ui_FLTFLD_translateMagnitude', changeCommand=self.ui_refresh, value=10)
                                pm.separator(style='none')
                                self.ui_BTN_translateBiasReset = pm.button(label='0')
                                self.ui_INTSLGRP_translateBias = pm.intSliderGrp(
                                    'ui_INTSLGRP_translateBias',
                                    columnWidth=[1, 30],
                                    field=True,
                                    minValue=-100,
                                    maxValue=100,
                                    fieldMinValue=-100,
                                    fieldMaxValue=100,
                                    value=0,
                                    step=1,
                                    fieldStep=1,
                                    sliderStep=1,
                                    changeCommand=self.ui_refresh,
                                    dragCommand=self.ui_refresh
                                )
                                pm.button(self.ui_BTN_translateBiasReset, edit=True, command=pm.Callback(self.ui_resetBias, self.ui_INTSLGRP_translateBias))
                                pm.text(label='=')
                                self.ui_FLTFLD_translateMin = pm.floatField(enable=False, value=-5)
                                self.ui_FLTFLD_translateMax = pm.floatField(enable=False, value=95)

                                #----- Rotate Row -----

                                pm.text(label='Rotate ', align='right')
                                pm.button(label='X', command=pm.Callback(self.randomizeRotate, ['rx']))
                                pm.button(label='Y', command=pm.Callback(self.randomizeRotate, ['ry']))
                                pm.button(label='Z', command=pm.Callback(self.randomizeRotate, ['rz']))
                                pm.button(label='XYZ', command=pm.Callback(self.randomizeRotate, ['rx', 'ry', 'rz']))
                                self.ui_FLTFLD_rotateMagnitude = pm.floatField('ui_FLTFLD_rotateMagnitude', changeCommand=self.ui_refresh, value=90)
                                pm.separator(style='none')
                                self.ui_BTN_rotateBiasReset = pm.button(label='0')
                                self.ui_INTSLGRP_rotateBias = pm.intSliderGrp(
                                    'ui_INTSLGRP_rotateBias',
                                    columnWidth=[1, 30],
                                    field=True,
                                    minValue=-100,
                                    maxValue=100,
                                    fieldMinValue=-100,
                                    fieldMaxValue=100,
                                    value=0,
                                    step=1,
                                    fieldStep=1,
                                    sliderStep=1,
                                    changeCommand=self.ui_refresh,
                                    dragCommand=self.ui_refresh
                                )
                                pm.button(self.ui_BTN_rotateBiasReset, edit=True, command=pm.Callback(self.ui_resetBias, self.ui_INTSLGRP_rotateBias))
                                pm.text(label='=')
                                self.ui_FLTFLD_rotateMin = pm.floatField(enable=False, value=-5)
                                self.ui_FLTFLD_rotateMax = pm.floatField(enable=False, value=95)

                                #----- Scale Row -----

                                pm.text(label='Scale ', align='right')
                                pm.button(label='X', command=pm.Callback(self.randomizeScale, ['sx']))
                                pm.button(label='Y', command=pm.Callback(self.randomizeScale, ['sy']))
                                pm.button(label='Z', command=pm.Callback(self.randomizeScale, ['sz']))
                                pm.flowLayout()
                                pm.button(label='XYZ', command=pm.Callback(self.randomizeScale, ['sx', 'sy', 'sz']))
                                pm.button(label='Uniform', command=pm.Callback(self.randomizeScale, ['uniform']))
                                pm.setParent('..')
                                self.ui_FLTFLD_scaleMagnitude = pm.floatField('ui_FLTFLD_scaleMagnitude', changeCommand=self.ui_refresh, value=2)
                                pm.separator(style='none')
                                self.ui_BTN_scaleBiasReset = pm.button(label='0')
                                self.ui_INTSLGRP_scaleBias = pm.intSliderGrp(
                                    'ui_INTSLGRP_scaleBias',
                                    columnWidth=[1, 30],
                                    field=True,
                                    minValue=-100,
                                    maxValue=100,
                                    fieldMinValue=-100,
                                    fieldMaxValue=100,
                                    value=0,
                                    step=1,
                                    fieldStep=1,
                                    sliderStep=1,
                                    changeCommand=self.ui_refresh,
                                    dragCommand=self.ui_refresh
                                )
                                pm.button(self.ui_BTN_scaleBiasReset, edit=True, command=pm.Callback(self.ui_resetBias, self.ui_INTSLGRP_scaleBias))
                                pm.text(label='=')
                                self.ui_FLTFLD_scaleMin = pm.floatField(enable=False, value=-5)
                                self.ui_FLTFLD_scaleMax = pm.floatField(enable=False, value=95)

                        with pm.frameLayout(
                            label='Seed Control',
                            collapsable=True,
                            marginHeight=3,
                            borderStyle='etchedIn',
                            borderVisible=True
                        ) as self.ui_LAY_frameSeedControl:

                            with pm.columnLayout(adjustableColumn=True):

                                with pm.rowLayout(
                                    numberOfColumns=2,
                                    columnWidth2=[ui_labelWidth, ui_inputWidth],
                                    columnAttach=[1, 'right', 5]
                                ):

                                    pm.text(label='Use Seed')
                                    self.ui_CHK_useSeed = pm.checkBox(
                                        'ui_CHK_useSeed',
                                        value=True,
                                        label='',
                                        changeCommand=self.ui_refresh
                                    )

                                with pm.rowLayout(
                                    numberOfColumns=2,
                                    columnWidth2=[ui_labelWidth, ui_inputWidth],
                                    columnAttach=[1, 'right', 5]
                                ):

                                    pm.text(label='Seed')

                                    self.ui_INTSLGRP_seedValue = pm.intSliderGrp(
                                        'ui_INTSLGRP_seedValue',
                                        field=True,
                                        minValue=1,
                                        maxValue=10000,
                                        fieldMinValue=1,
                                        fieldMaxValue=10000,
                                        value=1234,
                                        step=1,
                                        fieldStep=1,
                                        sliderStep=1
                                    )

                pm.setParent(self.ui_mainForm)

                self.ui_BTN_close = pm.button(
                    label='Close',
                    command=self.ui_close
                )

        pm.formLayout(self.ui_mainForm, e=True, attachForm=[self.ui_LAY_mainScroll, 'top', 2])
        pm.formLayout(self.ui_mainForm, e=True, attachForm=[self.ui_LAY_mainScroll, 'left', 2])
        pm.formLayout(self.ui_mainForm, e=True, attachForm=[self.ui_LAY_mainScroll, 'right', 2])
        pm.formLayout(self.ui_mainForm, e=True, attachControl=[self.ui_LAY_mainScroll, 'bottom', 2, self.ui_BTN_close])

        pm.formLayout(self.ui_mainForm, e=True, attachNone=[self.ui_BTN_close, 'top'])
        pm.formLayout(self.ui_mainForm, e=True, attachForm=[self.ui_BTN_close, 'left', 2])
        pm.formLayout(self.ui_mainForm, e=True, attachForm=[self.ui_BTN_close, 'right', 2])
        pm.formLayout(self.ui_mainForm, e=True, attachForm=[self.ui_BTN_close, 'bottom', 2])

        self.prefSaver = PrefSaver.PrefSaver(Serializers.SerializerOptVar(OPT_VAR_NAME))
        self.ui_initSettings()
        self.ui_loadSettings()

        self.window.show()

    def ui_initSettings(self):
        self.prefSaver.addControl(self.ui_FLTFLD_translateMagnitude, PrefSaver.UIType.PMFloatField, 1)
        self.prefSaver.addControl(self.ui_FLTFLD_rotateMagnitude, PrefSaver.UIType.PMFloatField, 180)
        self.prefSaver.addControl(self.ui_FLTFLD_scaleMagnitude, PrefSaver.UIType.PMFloatField, 2)
        self.prefSaver.addControl(self.ui_INTSLGRP_translateBias, PrefSaver.UIType.PMIntSliderGrp, 0)
        self.prefSaver.addControl(self.ui_INTSLGRP_rotateBias, PrefSaver.UIType.PMIntSliderGrp, 0)
        self.prefSaver.addControl(self.ui_INTSLGRP_scaleBias, PrefSaver.UIType.PMIntSliderGrp, 0)
        self.prefSaver.addControl(self.ui_CHK_useSeed, PrefSaver.UIType.PMCheckBox, False)
        self.prefSaver.addControl(self.ui_INTSLGRP_seedValue, PrefSaver.UIType.PMIntSliderGrp, 1234)

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()
        self.ui_refresh()

    def ui_saveSettings(self):
        self.prefSaver.savePrefs()

    # noinspection PyUnusedLocal
    def ui_resetSettings(self, *args):
        self.prefSaver.resetPrefs()
        self.ui_refresh()

    # noinspection PyUnusedLocal
    def ui_refresh(self, *arg):

        magnitude = m.floatField(self.ui_FLTFLD_translateMagnitude, q=True, value=True)
        bias = m.intSliderGrp(self.ui_INTSLGRP_translateBias, q=True, value=True)
        _min, _max = self.calculateMinMax(magnitude, bias)
        m.floatField(self.ui_FLTFLD_translateMin, e=True, value=_min)
        m.floatField(self.ui_FLTFLD_translateMax, e=True, value=_max)

        magnitude = m.floatField(self.ui_FLTFLD_rotateMagnitude, q=True, value=True)
        bias = m.intSliderGrp(self.ui_INTSLGRP_rotateBias, q=True, value=True)
        _min, _max = self.calculateMinMax(magnitude, bias)
        m.floatField(self.ui_FLTFLD_rotateMin, e=True, value=_min)
        m.floatField(self.ui_FLTFLD_rotateMax, e=True, value=_max)

        magnitude = m.floatField(self.ui_FLTFLD_scaleMagnitude, q=True, value=True)
        bias = m.intSliderGrp(self.ui_INTSLGRP_scaleBias, q=True, value=True)
        _min, _max = self.calculateMinMaxScale(magnitude, bias)
        m.floatField(self.ui_FLTFLD_scaleMin, e=True, value=_min)
        m.floatField(self.ui_FLTFLD_scaleMax, e=True, value=_max)

        useSeed = m.checkBox(self.ui_CHK_useSeed, q=True, value=True)
        m.intSliderGrp(self.ui_INTSLGRP_seedValue, e=True, enable=useSeed)

    def calculateMinMax(self, mag, bias):

        bias = float(bias) / 100

        if bias > 0:
            _min = -mag + bias * mag
            _max = mag
        else:
            _min = -mag
            _max = mag + bias * mag

        return _min, _max

    def calculateMinMaxScale(self, mag, bias):

        bias = float(bias) / 100

        if bias > 0:
            _min = bias + ((1 - bias) / mag)
            _max = mag
        else:
            _min = 1 / mag
            _max = (mag - 1) * bias + mag

        return _min, _max

    def calculateRandomScale(self, mag, bias):

        _min, _max = self.calculateMinMax(1, bias)

        randomValue = random.uniform(_min, _max)

        if randomValue > 0:
            randomValue = randomValue * (mag - 1) + 1
        else:
            randomValue = randomValue * (1 - 1 / mag) + 1

        return randomValue

    def getSeed(self):
        if not m.checkBox(self.ui_CHK_useSeed, q=True, value=True):
            return None
        else:
            return m.intSliderGrp(self.ui_INTSLGRP_seedValue, q=True, value=True)

    def getSelectedTransforms(self):
        return m.ls(sl=True, transforms=True)

    # noinspection PyUnusedLocal
    def ui_resetBias(self, ui_target, *arg):
        m.intSliderGrp(ui_target, edit=True, value=0)
        self.ui_refresh()

    # noinspection PyUnusedLocal
    def randomizeTranslate(self, attrs, *arg):
        mag = m.floatField(self.ui_FLTFLD_translateMagnitude, q=True, value=True)
        bias = m.intSliderGrp(self.ui_INTSLGRP_translateBias, q=True, value=True)
        self.doRandomize(attrs, mag, bias)

    # noinspection PyUnusedLocal
    def randomizeRotate(self, attrs, *arg):
        mag = m.floatField(self.ui_FLTFLD_rotateMagnitude, q=True, value=True)
        bias = m.intSliderGrp(self.ui_INTSLGRP_rotateBias, q=True, value=True)
        self.doRandomize(attrs, mag, bias)

    # noinspection PyUnusedLocal
    def randomizeScale(self, attrs, *arg):
        mag = m.floatField(self.ui_FLTFLD_scaleMagnitude, q=True, value=True)
        bias = m.intSliderGrp(self.ui_INTSLGRP_scaleBias, q=True, value=True)
        self.doRandomize(attrs, mag, bias)

    def doRandomize(self, attrs, mag, bias):
        self.ui_saveSettings()

        random.seed(self.getSeed())
        objects = self.getSelectedTransforms()
        for obj in objects:
            for attr in attrs:

                if attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
                    attrValue = m.getAttr(obj + '.' + attr)
                    _min, _max = self.calculateMinMax(mag, bias)
                    attrValue = random.uniform(_min, _max) + attrValue
                    m.setAttr(obj + '.' + attr, attrValue)

                elif attr in ['sx', 'sy', 'sz']:
                    randomValue = self.calculateRandomScale(mag, bias)
                    attrValue = m.getAttr(obj + '.' + attr)
                    m.setAttr(obj + '.' + attr, attrValue * randomValue)

                elif attr in ['uniform']:
                    randomValue = self.calculateRandomScale(mag, bias)
                    for attrIn in ('sx', 'sy', 'sz'):
                        attrValue = m.getAttr(obj + '.' + attrIn)
                        m.setAttr(obj + '.' + attrIn, attrValue * randomValue)

    # noinspection PyUnusedLocal
    def ui_close(self, *args):
        self.ui_saveSettings()
        if pm.window(WIN_NAME, exists=True):
            pm.deleteUI(WIN_NAME)

    # noinspection PyUnusedLocal
    def ui_showHelp(self, tab, *args):
        if pm.window(WIN_HELP_NAME, exists=True):
            pm.deleteUI(WIN_HELP_NAME)

        with pm.window(
            WIN_HELP_NAME,
            title=WIN_HELP_TITLE,
            maximizeButton=False,
            menuBar=True,
            menuBarVisible=True
        ) as self.windowHelp:

            with pm.formLayout() as self.ui_LAY_formMainHelp:

                with pm.tabLayout(innerMarginWidth=50, innerMarginHeight=50, childResizable=True) as self.ui_LAY_tabHelp:

                    with pm.formLayout() as self.ui_LAY_formHelpMargin:

                        with pm.scrollLayout(childResizable=True) as self.ui_LAY_scrollHelp:

                            pm.formLayout(self.ui_LAY_formHelpMargin, e=True, attachForm=[self.ui_LAY_scrollHelp, 'top', 2])
                            pm.formLayout(self.ui_LAY_formHelpMargin, e=True, attachForm=[self.ui_LAY_scrollHelp, 'left', 2])
                            pm.formLayout(self.ui_LAY_formHelpMargin, e=True, attachForm=[self.ui_LAY_scrollHelp, 'right', 2])
                            pm.formLayout(self.ui_LAY_formHelpMargin, e=True, attachForm=[self.ui_LAY_scrollHelp, 'bottom', 2])

                            with pm.frameLayout(
                                label='Help on ' + WIN_TITLE,
                                collapsable=False,
                                marginHeight=3,
                                borderStyle='etchedIn',
                                borderVisible=True
                            ):

                                with pm.rowLayout(columnAttach=[1, 'both', 10]):

                                    self.ui_TXT_help = pm.text('Tab1', align='center')

                    with pm.formLayout() as self.ui_LAY_formAboutMargin:

                        with pm.scrollLayout(childResizable=True) as self.ui_LAY_scrollAbout:

                            pm.formLayout(self.ui_LAY_formAboutMargin, e=True, attachForm=[self.ui_LAY_scrollAbout, 'top', 2])
                            pm.formLayout(self.ui_LAY_formAboutMargin, e=True, attachForm=[self.ui_LAY_scrollAbout, 'left', 2])
                            pm.formLayout(self.ui_LAY_formAboutMargin, e=True, attachForm=[self.ui_LAY_scrollAbout, 'right', 2])
                            pm.formLayout(self.ui_LAY_formAboutMargin, e=True, attachForm=[self.ui_LAY_scrollAbout, 'bottom', 2])

                            with pm.frameLayout(
                                label='About ' + WIN_TITLE,
                                collapsable=False,
                                marginHeight=3,
                                borderStyle='etchedIn',
                                borderVisible=True
                            ):

                                with pm.rowLayout(columnAttach=[1, 'both', 10]):

                                    self.ui_TXT_about = pm.text('')

                self.ui_BTN_closeHelp = pm.button(
                    'Close',
                    command=lambda x: pm.deleteUI(WIN_HELP_NAME)
                )

            pm.formLayout(self.ui_LAY_formMainHelp, e=True, attachForm=[self.ui_LAY_tabHelp, 'top', 2])
            pm.formLayout(self.ui_LAY_formMainHelp, e=True, attachForm=[self.ui_LAY_tabHelp, 'left', 2])
            pm.formLayout(self.ui_LAY_formMainHelp, e=True, attachForm=[self.ui_LAY_tabHelp, 'right', 2])
            pm.formLayout(self.ui_LAY_formMainHelp, e=True, attachControl=[self.ui_LAY_tabHelp, 'bottom', 2, self.ui_BTN_closeHelp])

            pm.formLayout(self.ui_LAY_formMainHelp, e=True, attachNone=[self.ui_BTN_closeHelp, 'top'])
            pm.formLayout(self.ui_LAY_formMainHelp, e=True, attachForm=[self.ui_BTN_closeHelp, 'left', 2])
            pm.formLayout(self.ui_LAY_formMainHelp, e=True, attachForm=[self.ui_BTN_closeHelp, 'right', 2])
            pm.formLayout(self.ui_LAY_formMainHelp, e=True, attachForm=[self.ui_BTN_closeHelp, 'bottom', 2])

            pm.tabLayout(
                self.ui_LAY_tabHelp,
                edit=True,
                tabLabel=(
                    (self.ui_LAY_formHelpMargin, 'Help'),
                    (self.ui_LAY_formAboutMargin, 'About')
                )
            )

            # - - - - - - - - - - - - - - - - - - - -

            textHelp = """
    This tool randomizes \"Translate\", \"Rotate\" and \"Scale\" attributes of selected objects.

    Workflow
    Select objects which transforms you want to randomize. Adjust settings if you want to.
    Press butons \"X\", \"Y\", \"Z\", \"XYZ\", or \"Uniform\" to randomize corresponding attributes.

    Magnitude
    Maximum random value.

    Bias
    Shift randomization to positive or negative value range. The result of this shifting
    is reflected in \"Min\" and \"Max\" fields.

    \"0\" Button
    Resets \"Bias\" to 0

    Min and Max
    Minimum and maximum possible random values according to current \"Magnitude\" and \"Bias\"

    Seed
    Use Seed value to randomize in fixed random pattern, which is not changing between each randomization.

    Reset Settings
    Use \"Edit\" - \"Reset Settings\" to restore defaults
    """

            textAbout = "\n" + WIN_TITLE + """
    Programmed by Eugene Davydenko, 2011

    This script may be freely distributed.
    Modify at your own risk.

    email: etchermail@gmail.com
    """

            pm.text(self.ui_TXT_help, e=True, label=textHelp)
            pm.text(self.ui_TXT_about, e=True, label=textAbout)

            pm.tabLayout(self.ui_LAY_tabHelp, e=True, selectTabIndex=tab)

        self.windowHelp.show()


def run():
    RandomizerUI()
