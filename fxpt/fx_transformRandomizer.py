import maya.cmds as cmds
import random
from functools import partial


# noinspection PyMethodMayBeStatic,PyAttributeOutsideInit
class RandomizerUI(object):
    def __init__(self):

        self.winName = "fx_transformRandomizerWin"
        self.winTitle = "Transform Randomizer v1.0"
        ui_labelWidth = 140
        ui_inputWidth = 240

        # ################ UI Creation ################

        if cmds.window(
            self.winName,
            q=True,
            exists=True
        ):
            cmds.deleteUI(self.winName)

        self.window = cmds.window(
            self.winName,
            title=self.winTitle,
            maximizeButton=False,
            menuBar=True,
            menuBarVisible=True
        )

        cmds.menu(label='Edit', tearOff=False)
        cmds.menuItem(label='Reset Settings', command=self.ui_resetSettings)
        cmds.menu(label='Help', tearOff=False)
        cmds.menuItem(label='Help on ' + self.winTitle, command=partial(self.ui_showHelp, 1))
        cmds.menuItem(divider=True)
        cmds.menuItem(label='Script Information', command=partial(self.ui_showHelp, 2))

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_mainForm = cmds.formLayout()

        self.ui_LAY_mainScroll = cmds.scrollLayout(
            childResizable=True
        )

        self.ui_LAY_mainColumn = cmds.columnLayout(
            adjustableColumn=True
        )

        self.ui_LAY_frameControlPanel = cmds.frameLayout(
            label='Control Panel',
            collapsable=True,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True
        )

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_LAY_mainRowColumn = cmds.rowColumnLayout(
            numberOfColumns=12,
            rowSpacing=[1, 5],
            #            Label       X       Y         Z       XYZ      Mag     Sep      Reset     Bias      Sep       Min       Max
            columnWidth=[(1, 60), (2, 20), (3, 20), (4, 20), (5, 76), (6, 60), (7, 20), (8, 20), (9, 120), (10, 20), (11, 60), (12, 60)]
        )

        # - - - - - Header Row - - - - -

        cmds.separator(style='none')
        cmds.separator(style='none')
        cmds.separator(style='none')
        cmds.separator(style='none')
        cmds.separator(style='none')
        cmds.text(label='Magnitude', )
        cmds.separator(style='none')
        cmds.separator(style='none')
        cmds.text(label='Bias', )
        cmds.separator(style='none')
        cmds.text(label='Min', )
        cmds.text(label='Max', )

        # - - - - - Translate Row - - - - -

        cmds.text(label='Translate ', align='right')
        cmds.button(label='X', command=partial(self.randomizeTranslate, ['tx']))
        cmds.button(label='Y', command=partial(self.randomizeTranslate, ['ty']))
        cmds.button(label='Z', command=partial(self.randomizeTranslate, ['tz']))
        cmds.button(label='XYZ', command=partial(self.randomizeTranslate, ['tx', 'ty', 'tz']))
        self.ui_FLTFLD_translateMagnitude = cmds.floatField(
            changeCommand=self.ui_refresh,
            value=10
        )
        cmds.separator(style='none')
        self.ui_BTN_translateBiasReset = cmds.button(label='0')
        self.ui_INTSLGRP_translateBias = cmds.intSliderGrp(
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
        cmds.button(self.ui_BTN_translateBiasReset, edit=True,
                    command=partial(self.ui_resetBias, self.ui_INTSLGRP_translateBias))
        cmds.text(label='=')
        self.ui_FLTFLD_translateMin = cmds.floatField(enable=False, value=-5)
        self.ui_FLTFLD_translateMax = cmds.floatField(enable=False, value=95)

        # - - - - - Rotate Row - - - - -

        cmds.text(label='Rotate ', align='right')
        cmds.button(label='X', command=partial(self.randomizeRotate, ['rx']))
        cmds.button(label='Y', command=partial(self.randomizeRotate, ['ry']))
        cmds.button(label='Z', command=partial(self.randomizeRotate, ['rz']))
        cmds.button(label='XYZ', command=partial(self.randomizeRotate, ['rx', 'ry', 'rz']))
        self.ui_FLTFLD_rotateMagnitude = cmds.floatField(
            changeCommand=self.ui_refresh,
            value=90
        )
        cmds.separator(style='none')
        self.ui_BTN_rotateBiasReset = cmds.button(label='0')
        self.ui_INTSLGRP_rotateBias = cmds.intSliderGrp(
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
        cmds.button(self.ui_BTN_rotateBiasReset, edit=True,
                    command=partial(self.ui_resetBias, self.ui_INTSLGRP_rotateBias))
        cmds.text(label='=')
        self.ui_FLTFLD_rotateMin = cmds.floatField(enable=False, value=-5)
        self.ui_FLTFLD_rotateMax = cmds.floatField(enable=False, value=95)

        # - - - - - Scale Row - - - - -

        cmds.text(label='Scale ', align='right')
        cmds.button(label='X', command=partial(self.randomizeScale, ['sx']))
        cmds.button(label='Y', command=partial(self.randomizeScale, ['sy']))
        cmds.button(label='Z', command=partial(self.randomizeScale, ['sz']))
        cmds.flowLayout()
        cmds.button(label='XYZ', command=partial(self.randomizeScale, ['sx', 'sy', 'sz']))
        cmds.button(label='Uniform', command=partial(self.randomizeScale, ['uniform']))
        cmds.setParent('..')
        self.ui_FLTFLD_scaleMagnitude = cmds.floatField(
            changeCommand=self.ui_refresh,
            value=2
        )
        cmds.separator(style='none')
        self.ui_BTN_scaleBiasReset = cmds.button(label='0')
        self.ui_INTSLGRP_scaleBias = cmds.intSliderGrp(
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
        cmds.button(self.ui_BTN_scaleBiasReset, edit=True,
                    command=partial(self.ui_resetBias, self.ui_INTSLGRP_scaleBias))
        cmds.text(label='=')
        self.ui_FLTFLD_scaleMin = cmds.floatField(enable=False, value=-5)
        self.ui_FLTFLD_scaleMax = cmds.floatField(enable=False, value=95)

        # - - - - - - - - - - - - - - - - - - - -

        cmds.setParent(self.ui_LAY_mainColumn)

        self.ui_LAY_frameSeedControl = cmds.frameLayout(
            label='Seed Control',
            collapsable=True,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True
        )

        cmds.columnLayout(
            adjustableColumn=True
        )

        # - - - - - - - - - - - - - - - - - - - -

        cmds.rowLayout(
            numberOfColumns=2,
            columnWidth2=[ui_labelWidth, ui_inputWidth],
            columnAttach=[1, 'right', 5]
        )

        cmds.text(label='Use Seed')
        self.ui_CHK_useSeed = cmds.checkBox(
            value=True,
            label='',
            changeCommand=self.ui_refresh
        )

        cmds.setParent('..')  # local row -> seed column

        # - - - - - - - - - - - - - - - - - - - -

        cmds.rowLayout(
            numberOfColumns=2,
            columnWidth2=[ui_labelWidth, ui_inputWidth],
            columnAttach=[1, 'right', 5]
        )

        cmds.text(label='Seed')

        self.ui_INTSLGRP_seedValue = cmds.intSliderGrp(
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

        # - - - - - - - - - - - - - - - - - - - -

        cmds.setParent(self.ui_mainForm)

        self.ui_BTN_close = cmds.button(
            label='Close',
            command=self.ui_close
        )

        # - - - - - Organize Main Form Layout - - - - -

        cmds.formLayout(self.ui_mainForm, e=True, attachForm=[self.ui_LAY_mainScroll, 'top', 2])
        cmds.formLayout(self.ui_mainForm, e=True, attachForm=[self.ui_LAY_mainScroll, 'left', 2])
        cmds.formLayout(self.ui_mainForm, e=True, attachForm=[self.ui_LAY_mainScroll, 'right', 2])
        cmds.formLayout(self.ui_mainForm, e=True,
                        attachControl=[self.ui_LAY_mainScroll, 'bottom', 2, self.ui_BTN_close])

        cmds.formLayout(self.ui_mainForm, e=True, attachNone=[self.ui_BTN_close, 'top'])
        cmds.formLayout(self.ui_mainForm, e=True, attachForm=[self.ui_BTN_close, 'left', 2])
        cmds.formLayout(self.ui_mainForm, e=True, attachForm=[self.ui_BTN_close, 'right', 2])
        cmds.formLayout(self.ui_mainForm, e=True, attachForm=[self.ui_BTN_close, 'bottom', 2])

        # ################ UI Creation Finished ##################

        self.ui_initSettings()
        self.ui_loadSettings()

        cmds.showWindow(self.winName)

    def ui_initSettings(self):
        if not cmds.optionVar(exists='fx_transformRandomizer_magTranslate'):
            cmds.optionVar(floatValue=('fx_transformRandomizer_magTranslate', 1))
        if not cmds.optionVar(exists='fx_transformRandomizer_magRotate'):
            cmds.optionVar(floatValue=('fx_transformRandomizer_magRotate', 180))
        if not cmds.optionVar(exists='fx_transformRandomizer_magScale'):
            cmds.optionVar(floatValue=('fx_transformRandomizer_magScale', 2))

        if not cmds.optionVar(exists='fx_transformRandomizer_biasTranslate'):
            cmds.optionVar(intValue=('fx_transformRandomizer_biasTranslate', 0))
        if not cmds.optionVar(exists='fx_transformRandomizer_biasRotate'):
            cmds.optionVar(intValue=('fx_transformRandomizer_biasRotate', 0))
        if not cmds.optionVar(exists='fx_transformRandomizer_biasScale'):
            cmds.optionVar(intValue=('fx_transformRandomizer_biasScale', 0))

        if not cmds.optionVar(exists='fx_transformRandomizer_useSeed'):
            cmds.optionVar(intValue=('fx_transformRandomizer_useSeed', 0))
        if not cmds.optionVar(exists='fx_transformRandomizer_seedValue'):
            cmds.optionVar(intValue=('fx_transformRandomizer_seedValue', 1234))

    def ui_loadSettings(self):

        cmds.floatField(self.ui_FLTFLD_translateMagnitude, e=True,
                        value=cmds.optionVar(q='fx_transformRandomizer_magTranslate'))
        cmds.floatField(self.ui_FLTFLD_rotateMagnitude, e=True,
                        value=cmds.optionVar(q='fx_transformRandomizer_magRotate'))
        cmds.floatField(self.ui_FLTFLD_scaleMagnitude, e=True,
                        value=cmds.optionVar(q='fx_transformRandomizer_magScale'))

        cmds.intSliderGrp(self.ui_INTSLGRP_translateBias, e=True,
                          value=cmds.optionVar(q='fx_transformRandomizer_biasTranslate'))
        cmds.intSliderGrp(self.ui_INTSLGRP_rotateBias, e=True,
                          value=cmds.optionVar(q='fx_transformRandomizer_biasRotate'))
        cmds.intSliderGrp(self.ui_INTSLGRP_scaleBias, e=True,
                          value=cmds.optionVar(q='fx_transformRandomizer_biasScale'))

        cmds.checkBox(self.ui_CHK_useSeed, e=True, value=cmds.optionVar(q='fx_transformRandomizer_useSeed'))
        cmds.intSliderGrp(self.ui_INTSLGRP_seedValue, e=True,
                          value=cmds.optionVar(q='fx_transformRandomizer_seedValue'))

        self.ui_refresh()

    def ui_saveSettings(self):

        cmds.optionVar(floatValue=['fx_transformRandomizer_magTranslate',
                                   cmds.floatField(self.ui_FLTFLD_translateMagnitude, q=True, value=True)])
        cmds.optionVar(floatValue=['fx_transformRandomizer_magRotate',
                                   cmds.floatField(self.ui_FLTFLD_rotateMagnitude, q=True, value=True)])
        cmds.optionVar(floatValue=['fx_transformRandomizer_magScale',
                                   cmds.floatField(self.ui_FLTFLD_scaleMagnitude, q=True, value=True)])

        cmds.optionVar(floatValue=['fx_transformRandomizer_biasTranslate',
                                   cmds.intSliderGrp(self.ui_INTSLGRP_translateBias, q=True, value=True)])
        cmds.optionVar(floatValue=['fx_transformRandomizer_biasRotate',
                                   cmds.intSliderGrp(self.ui_INTSLGRP_rotateBias, q=True, value=True)])
        cmds.optionVar(floatValue=['fx_transformRandomizer_biasScale',
                                   cmds.intSliderGrp(self.ui_INTSLGRP_scaleBias, q=True, value=True)])

        cmds.optionVar(
            intValue=['fx_transformRandomizer_useSeed', cmds.checkBox(self.ui_CHK_useSeed, q=True, value=True)])
        cmds.optionVar(intValue=['fx_transformRandomizer_seedValue',
                                 cmds.intSliderGrp(self.ui_INTSLGRP_seedValue, q=True, value=True)])

    # noinspection PyUnusedLocal
    def ui_resetSettings(self, *args):
        optionVars = (
            'fx_transformRandomizer_magTranslate',
            'fx_transformRandomizer_magRotate',
            'fx_transformRandomizer_magScale',
            'fx_transformRandomizer_biasTranslate',
            'fx_transformRandomizer_biasRotate',
            'fx_transformRandomizer_biasScale',
            'fx_transformRandomizer_useSeed',
            'fx_transformRandomizer_seedValue'
        )

        for var in optionVars:
            cmds.optionVar(remove=var)

        self.ui_initSettings()
        self.ui_loadSettings()

    # noinspection PyUnusedLocal
    def ui_refresh(self, *arg):

        magnitude = cmds.floatField(self.ui_FLTFLD_translateMagnitude, q=True, value=True)
        bias = cmds.intSliderGrp(self.ui_INTSLGRP_translateBias, q=True, value=True)
        _min, _max = self.calculateMinMax(magnitude, bias)
        cmds.floatField(self.ui_FLTFLD_translateMin, e=True, value=_min)
        cmds.floatField(self.ui_FLTFLD_translateMax, e=True, value=_max)

        magnitude = cmds.floatField(self.ui_FLTFLD_rotateMagnitude, q=True, value=True)
        bias = cmds.intSliderGrp(self.ui_INTSLGRP_rotateBias, q=True, value=True)
        _min, _max = self.calculateMinMax(magnitude, bias)
        cmds.floatField(self.ui_FLTFLD_rotateMin, e=True, value=_min)
        cmds.floatField(self.ui_FLTFLD_rotateMax, e=True, value=_max)

        magnitude = cmds.floatField(self.ui_FLTFLD_scaleMagnitude, q=True, value=True)
        bias = cmds.intSliderGrp(self.ui_INTSLGRP_scaleBias, q=True, value=True)
        _min, _max = self.calculateMinMaxScale(magnitude, bias)
        cmds.floatField(self.ui_FLTFLD_scaleMin, e=True, value=_min)
        cmds.floatField(self.ui_FLTFLD_scaleMax, e=True, value=_max)

        useSeed = cmds.checkBox(self.ui_CHK_useSeed, q=True, value=True)
        cmds.intSliderGrp(self.ui_INTSLGRP_seedValue, e=True, enable=useSeed)

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
        if not cmds.checkBox(self.ui_CHK_useSeed, q=True, value=True):
            return None
        else:
            return cmds.intSliderGrp(self.ui_INTSLGRP_seedValue, q=True, value=True)

    def getSelectedTransforms(self):
        return cmds.ls(sl=True, transforms=True)

    # noinspection PyUnusedLocal
    def ui_resetBias(self, ui_target, *arg):
        cmds.intSliderGrp(ui_target, edit=True, value=0)
        self.ui_refresh()

    # noinspection PyUnusedLocal
    def randomizeTranslate(self, attrs, *arg):
        mag = cmds.floatField(self.ui_FLTFLD_translateMagnitude, q=True, value=True)
        bias = cmds.intSliderGrp(self.ui_INTSLGRP_translateBias, q=True, value=True)
        self.doRandomize(attrs, mag, bias)

    # noinspection PyUnusedLocal
    def randomizeRotate(self, attrs, *arg):
        mag = cmds.floatField(self.ui_FLTFLD_rotateMagnitude, q=True, value=True)
        bias = cmds.intSliderGrp(self.ui_INTSLGRP_rotateBias, q=True, value=True)
        self.doRandomize(attrs, mag, bias)

    # noinspection PyUnusedLocal
    def randomizeScale(self, attrs, *arg):
        mag = cmds.floatField(self.ui_FLTFLD_scaleMagnitude, q=True, value=True)
        bias = cmds.intSliderGrp(self.ui_INTSLGRP_scaleBias, q=True, value=True)
        self.doRandomize(attrs, mag, bias)

    def doRandomize(self, attrs, mag, bias):
        self.ui_saveSettings()

        random.seed(self.getSeed())
        objects = self.getSelectedTransforms()
        for obj in objects:
            for attr in attrs:

                if attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']:
                    attrValue = cmds.getAttr(obj + '.' + attr)
                    _min, _max = self.calculateMinMax(mag, bias)
                    attrValue = random.uniform(_min, _max) + attrValue
                    cmds.setAttr(obj + '.' + attr, attrValue)

                elif attr in ['sx', 'sy', 'sz']:
                    randomValue = self.calculateRandomScale(mag, bias)
                    attrValue = cmds.getAttr(obj + '.' + attr)
                    cmds.setAttr(obj + '.' + attr, attrValue * randomValue)

                elif attr in ['uniform']:
                    randomValue = self.calculateRandomScale(mag, bias)
                    for attrIn in ('sx', 'sy', 'sz'):
                        attrValue = cmds.getAttr(obj + '.' + attrIn)
                        cmds.setAttr(obj + '.' + attrIn, attrValue * randomValue)

    # noinspection PyUnusedLocal
    def ui_close(self, *args):
        self.ui_saveSettings()
        if cmds.window(self.winName, q=True, exists=True):
            cmds.deleteUI(self.winName)

    # noinspection PyUnusedLocal
    def ui_showHelp(self, tab, *args):
        self.winHelpName = "fx_transformRandomizerHelpWin"
        self.winHelpTitle = self.winTitle + " Help"

        # ################ UI Creation ################

        if cmds.window(
            self.winHelpName,
            q=True,
            exists=True
        ):
            cmds.deleteUI(self.winHelpName)

        self.window = cmds.window(
            self.winHelpName,
            title=self.winHelpTitle,
            maximizeButton=False,
            menuBar=True,
            menuBarVisible=True
        )

        self.ui_LAY_formMainHelp = cmds.formLayout()

        self.ui_LAY_tabHelp = cmds.tabLayout(
            innerMarginWidth=50,
            innerMarginHeight=50,
            childResizable=True
        )

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_LAY_formHelpMargin = cmds.formLayout()

        self.ui_LAY_scrollHelp = cmds.scrollLayout(
            childResizable=True
        )

        cmds.formLayout(self.ui_LAY_formHelpMargin, e=True, attachForm=[self.ui_LAY_scrollHelp, 'top', 2])
        cmds.formLayout(self.ui_LAY_formHelpMargin, e=True, attachForm=[self.ui_LAY_scrollHelp, 'left', 2])
        cmds.formLayout(self.ui_LAY_formHelpMargin, e=True, attachForm=[self.ui_LAY_scrollHelp, 'right', 2])
        cmds.formLayout(self.ui_LAY_formHelpMargin, e=True, attachForm=[self.ui_LAY_scrollHelp, 'bottom', 2])

        cmds.frameLayout(
            label='Help on ' + self.winTitle,
            collapsable=False,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True
        )

        cmds.rowLayout(
            columnAttach=[1, 'both', 10]
        )

        self.ui_TXT_help = cmds.text('Tab1', align='center')

        cmds.setParent(self.ui_LAY_tabHelp)

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_LAY_formAboutMargin = cmds.formLayout()

        self.ui_LAY_scrollAbout = cmds.scrollLayout(
            childResizable=True
        )

        cmds.formLayout(self.ui_LAY_formAboutMargin, e=True, attachForm=[self.ui_LAY_scrollAbout, 'top', 2])
        cmds.formLayout(self.ui_LAY_formAboutMargin, e=True, attachForm=[self.ui_LAY_scrollAbout, 'left', 2])
        cmds.formLayout(self.ui_LAY_formAboutMargin, e=True, attachForm=[self.ui_LAY_scrollAbout, 'right', 2])
        cmds.formLayout(self.ui_LAY_formAboutMargin, e=True, attachForm=[self.ui_LAY_scrollAbout, 'bottom', 2])

        cmds.frameLayout(
            label='About ' + self.winTitle,
            collapsable=False,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True
        )

        cmds.rowLayout(
            columnAttach=[1, 'both', 10]
        )

        self.ui_TXT_about = cmds.text('')

        cmds.setParent(self.ui_LAY_formMainHelp)

        # - - - - - - - - - - - - - - - - - - - -

        self.ui_BTN_closeHelp = cmds.button(
            'Close',
            command=lambda x: cmds.deleteUI(self.winHelpName)
        )

        # - - - - - Organize Main Form Layout - - - - -

        cmds.formLayout(self.ui_LAY_formMainHelp, e=True, attachForm=[self.ui_LAY_tabHelp, 'top', 2])
        cmds.formLayout(self.ui_LAY_formMainHelp, e=True, attachForm=[self.ui_LAY_tabHelp, 'left', 2])
        cmds.formLayout(self.ui_LAY_formMainHelp, e=True, attachForm=[self.ui_LAY_tabHelp, 'right', 2])
        cmds.formLayout(self.ui_LAY_formMainHelp, e=True,
                        attachControl=[self.ui_LAY_tabHelp, 'bottom', 2, self.ui_BTN_closeHelp])

        cmds.formLayout(self.ui_LAY_formMainHelp, e=True, attachNone=[self.ui_BTN_closeHelp, 'top'])
        cmds.formLayout(self.ui_LAY_formMainHelp, e=True, attachForm=[self.ui_BTN_closeHelp, 'left', 2])
        cmds.formLayout(self.ui_LAY_formMainHelp, e=True, attachForm=[self.ui_BTN_closeHelp, 'right', 2])
        cmds.formLayout(self.ui_LAY_formMainHelp, e=True, attachForm=[self.ui_BTN_closeHelp, 'bottom', 2])

        # - - - - - - - - - - - - - - - - - - - -

        cmds.tabLayout(
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

        textAbout = "\n" + self.winTitle + """
Programmed by Eugene Davydenko, 2011

This script may be freely distributed.
Modify at your own risk.

email: etchermail@gmail.com
"""

        cmds.text(self.ui_TXT_help, e = True, label = textHelp)
        cmds.text(self.ui_TXT_about, e = True, label = textAbout)

        cmds.tabLayout(self.ui_LAY_tabHelp, e = True, selectTabIndex = tab)
        cmds.showWindow()

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

def run():
    RandomizerUI()
