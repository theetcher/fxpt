import random
import webbrowser

import maya.cmds as m

from fxpt3.fx_prefsaver import prefsaver, serializers

SCRIPT_NAME = 'FX Transform Randomizer'
WIN_NAME = 'fx_transformRandomizerWin'
WIN_TITLE = 'Transform Randomizer v1.1'
OPT_VAR_NAME = 'fx_randomizer_prefs'

SPACE_LOCAL = 0
SPACE_OBJECT = 1
SPACE_WORLD = 2

ATTR_LIST_TRANSLATE = ['tx', 'ty', 'tz']
ATTR_LIST_ROTATE = ['rx', 'ry', 'rz']
ATTR_LIST_SCALE = ['sx', 'sy', 'sz']
ATTR_LIST_SCALE_UNIFORM = ['uniform']
ATTR_LIST_TRANSLATE_ROTATE = ATTR_LIST_TRANSLATE + ATTR_LIST_ROTATE
ATTR_LIST_SCALE_ALL = ATTR_LIST_SCALE + ATTR_LIST_SCALE_UNIFORM

ARRAY_MAPPER = {
    'tx': 0,
    'ty': 1,
    'tz': 2,
    'rx': 0,
    'ry': 1,
    'rz': 2,
}

UI_LABEL_WIDTH = 140
UI_INPUT_WIDTH = 240


def calculateMinMax(mag, bias):
    bias = float(bias) / 100

    if bias > 0:
        _min = -mag + bias * mag
        _max = mag
    else:
        _min = -mag
        _max = mag + bias * mag

    return _min, _max


def calculateMinMaxScale(mag, bias):
    bias = float(bias) / 100

    if bias > 0:
        _min = bias + ((1 - bias) / mag)
        _max = mag
    else:
        _min = 1 / mag
        _max = (mag - 1) * bias + mag

    return _min, _max


def calculateRandomScale(rnd, mag, bias):
    _min, _max = calculateMinMax(1, bias)

    randomValue = rnd.uniform(_min, _max)

    if randomValue > 0:
        randomValue = randomValue * (mag - 1) + 1
    else:
        randomValue = randomValue * (1 - 1 / mag) + 1

    return randomValue


def getTransformArr(attr, value):
    arr = [0.0, 0.0, 0.0]
    arr[ARRAY_MAPPER[attr]] = value
    return arr


def move(obj, attr, value, space):
    arr = getTransformArr(attr, value)
    if space == SPACE_LOCAL:
        m.move(arr[0], arr[1], arr[2], obj, localSpace=True, relative=True, worldSpaceDistance=True)
    elif space == SPACE_OBJECT:
        m.move(arr[0], arr[1], arr[2], obj, objectSpace=True, relative=True, worldSpaceDistance=True)
    elif space == SPACE_WORLD:
        m.move(arr[0], arr[1], arr[2], obj, worldSpace=True, relative=True, worldSpaceDistance=True)
    else:
        assert False, 'Undefined space value during move: ' + str(space)


def rotate(obj, attr, value, space):
    arr = getTransformArr(attr, value)
    if space == SPACE_LOCAL:
        m.rotate(arr[0], arr[1], arr[2], obj, euler=True, relative=True)
    elif space == SPACE_OBJECT:
        m.rotate(arr[0], arr[1], arr[2], obj, objectSpace=True, relative=True)
    elif space == SPACE_WORLD:
        m.rotate(arr[0], arr[1], arr[2], obj, worldSpace=True, relative=True)
    else:
        assert False, 'Undefined space value during rotate: ' + str(space)


def scaleAttr(obj, attr, factor):
    plug = obj + '.' + attr
    m.setAttr(plug, m.getAttr(plug) * factor)


def randomizeObject(rnd, obj, attrs, mag, bias, space):
    for attr in attrs:
        if attr in ATTR_LIST_TRANSLATE_ROTATE:
            _min, _max = calculateMinMax(mag, bias)
            randomValue = rnd.uniform(_min, _max)
            if attr in ATTR_LIST_TRANSLATE:
                move(obj, attr, randomValue, space)
            else:
                rotate(obj, attr, randomValue, space)

        elif attr in ATTR_LIST_SCALE_ALL:
            randomValue = calculateRandomScale(rnd, mag, bias)
            if attr in ATTR_LIST_SCALE:
                scaleAttr(obj, attr, randomValue)
            else:
                for attrIn in ATTR_LIST_SCALE:
                    scaleAttr(obj, attrIn, randomValue)


def randomize(objects, attrs, mag, bias, space, seed):
    """Randomize the objects in one undo chunk. Returns the objects that failed (locked or connected attributes)."""
    if any(a in ATTR_LIST_SCALE_ALL for a in attrs) and mag <= 0:
        raise ValueError('Scale magnitude must be greater than 0.')

    # own generator: seeding the global one would change random numbers for everything else in Maya's Python
    rnd = random.Random(seed)
    failed = []
    m.undoInfo(openChunk=True, chunkName='fx_transform_randomizer')
    try:
        for obj in objects:
            try:
                randomizeObject(rnd, obj, attrs, mag, bias, space)
            except RuntimeError as e:
                failed.append((obj, str(e).strip()))
    finally:
        m.undoInfo(closeChunk=True)
    return failed


# noinspection PyMethodMayBeStatic,PyAttributeOutsideInit,PyUnusedLocal
class RandomizerUI(object):
    def __init__(self):
        self.ui_createUI()

        self.prefSaver = prefsaver.PrefSaver(serializers.SerializerOptVar(OPT_VAR_NAME))
        self.ui_initSettings()
        self.ui_loadSettings()

        m.showWindow(self.window)

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
            m.menu(label='Options', tearOff=False)
            m.radioMenuItemCollection()
            self.spaceMenuItems = {
                SPACE_LOCAL: m.menuItem(label='Use Local Space', radioButton=True, command=self.ui_saveSettings),
                SPACE_OBJECT: m.menuItem(label='Use Object Space', radioButton=False, command=self.ui_saveSettings),
                SPACE_WORLD: m.menuItem(label='Use World Space', radioButton=False, command=self.ui_saveSettings),
            }
            self.ui_setSpace(SPACE_OBJECT)
            m.menu(label='Help', tearOff=False)
            m.menuItem(label='Help on ' + WIN_TITLE, command=self.ui_showHelp)

            self.ui_LAY_mainForm = m.formLayout()

            self.ui_TAB_top = m.tabLayout(tabsVisible=False)
            m.tabLayout(self.ui_TAB_top, e=True, height=1)

            self.ui_LAY_attachForm = m.formLayout()

            self.ui_TAB_inner = m.tabLayout(tabsVisible=False, scrollable=True, innerMarginWidth=4)

            self.ui_LAY_mainColumn = m.columnLayout(adjustableColumn=True)

            self.ui_LAY_frameControlPanel = m.frameLayout(
                label='Control Panel',
                collapsable=True,
                collapse=False,
                marginHeight=3
            )

            self.ui_LAY_mainRowColumn = m.rowColumnLayout(
                numberOfColumns=12,
                columnSpacing=[(3, 2), (4, 2), (5, 2), (6, 2)],
                rowSpacing=(1, 5),
                #              Label      X        Y        Z        XYZ      Mag      Sep      Reset    Bias      Sep       Min       Max
                columnWidth=[(1, 60), (2, 20), (3, 20), (4, 20), (5, 80), (6, 60), (7, 20), (8, 20), (9, 120), (10, 20), (11, 60), (12, 60)]
            )

            # ----- Header Row -----
            for label in ('', '', '', '', '', 'Magnitude', '', '', 'Bias', '', 'Min', 'Max'):
                m.text(label=label)

            # ----- Translate Row -----
            m.text(label='Translate ', align='right')
            self.ui_createAxisButton('X', self.randomizeTranslate, ['tx'])
            self.ui_createAxisButton('Y', self.randomizeTranslate, ['ty'])
            self.ui_createAxisButton('Z', self.randomizeTranslate, ['tz'])
            self.ui_createAxisButton('XYZ', self.randomizeTranslate, ['tx', 'ty', 'tz'])
            self.ui_FLTFLD_translateMagnitude, self.ui_INTSLGRP_translateBias, self.ui_FLTFLD_translateMin, self.ui_FLTFLD_translateMax = \
                self.ui_createRowControls('translate', 10)

            # ----- Rotate Row -----
            m.text(label='Rotate ', align='right')
            self.ui_createAxisButton('X', self.randomizeRotate, ['rx'])
            self.ui_createAxisButton('Y', self.randomizeRotate, ['ry'])
            self.ui_createAxisButton('Z', self.randomizeRotate, ['rz'])
            self.ui_createAxisButton('XYZ', self.randomizeRotate, ['rx', 'ry', 'rz'])
            self.ui_FLTFLD_rotateMagnitude, self.ui_INTSLGRP_rotateBias, self.ui_FLTFLD_rotateMin, self.ui_FLTFLD_rotateMax = \
                self.ui_createRowControls('rotate', 90)

            # ----- Scale Row -----
            m.text(label='Scale ', align='right')
            self.ui_createAxisButton('X', self.randomizeScale, ['sx'])
            self.ui_createAxisButton('Y', self.randomizeScale, ['sy'])
            self.ui_createAxisButton('Z', self.randomizeScale, ['sz'])
            m.flowLayout(columnSpacing=2)
            self.ui_createAxisButton('XYZ', self.randomizeScale, ['sx', 'sy', 'sz'])
            self.ui_createAxisButton('Uniform', self.randomizeScale, ['uniform'])
            m.setParent('..')
            self.ui_FLTFLD_scaleMagnitude, self.ui_INTSLGRP_scaleBias, self.ui_FLTFLD_scaleMin, self.ui_FLTFLD_scaleMax = \
                self.ui_createRowControls('scale', 2)

            m.setParent(self.ui_LAY_mainColumn)

            self.ui_LAY_frameSeedControl = m.frameLayout(
                label='Seed Control',
                collapsable=True,
                collapse=False,
                marginHeight=3
            )
            m.columnLayout(adjustableColumn=False)

            m.rowLayout(
                numberOfColumns=2,
                columnWidth2=(UI_LABEL_WIDTH, UI_INPUT_WIDTH),
                columnAttach=(1, 'right', 5)
            )
            m.text(label='Use Seed')
            self.ui_CHK_useSeed = m.checkBox(
                'ui_CHK_useSeed',
                value=True,
                label='',
                changeCommand=self.ui_onChange
            )
            m.setParent('..')

            m.rowLayout(
                numberOfColumns=2,
                columnWidth2=(UI_LABEL_WIDTH, UI_INPUT_WIDTH),
                columnAttach=(1, 'right', 5)
            )
            m.text(label='Seed')
            m.setUITemplate('DefaultTemplate', popTemplate=True)  # strange slider group visual with default template
            self.ui_INTSLGRP_seedValue = m.intSliderGrp(
                'ui_INTSLGRP_seedValue',
                field=True,
                minValue=1,
                maxValue=10000,
                fieldMinValue=1,
                fieldMaxValue=10000,
                value=1234,
                step=1,
                fieldStep=1,
                sliderStep=1,
                changeCommand=self.ui_saveSettings
            )
            m.setUITemplate('DefaultTemplate', pushTemplate=True)
            m.setParent('..')

            m.setParent(self.ui_LAY_mainForm)

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
                (self.ui_BTN_close, 'left', 5),
                (self.ui_BTN_close, 'bottom', 5),
                (self.ui_BTN_close, 'right', 5),
            ],
            attachControl=[
                (self.ui_TAB_top, 'bottom', 5, self.ui_BTN_close),
            ],
            attachNone=[
                (self.ui_BTN_close, 'top'),
            ]
        )

    def ui_createAxisButton(self, label, func, attrs):
        return m.button(label=label, command=lambda *args: func(attrs))

    def ui_createRowControls(self, rowName, magnitude):
        """Creates Magnitude, Sep, Reset, Bias, Sep, Min, Max columns of a row. Returns (magnitude, bias, min, max) controls."""
        # control names are the same as in the legacy PyMEL version, so prefs saved by it still match
        magnitudeField = m.floatField(
            'ui_FLTFLD_{0}Magnitude'.format(rowName),
            changeCommand=self.ui_onChange,
            value=magnitude
        )
        m.text(label='')
        resetButton = m.button(label='0')
        m.setUITemplate('DefaultTemplate', popTemplate=True)  # strange slider group visual with default template
        try:
            biasSlider = m.intSliderGrp(
                'ui_INTSLGRP_{0}Bias'.format(rowName),
                columnWidth=(1, 30),
                field=True,
                minValue=-100,
                maxValue=100,
                fieldMinValue=-100,
                fieldMaxValue=100,
                value=0,
                step=1,
                fieldStep=1,
                sliderStep=1,
                changeCommand=self.ui_onChange,
                dragCommand=self.ui_refresh
            )
        finally:
            m.setUITemplate('DefaultTemplate', pushTemplate=True)
        m.button(resetButton, edit=True, command=lambda *args: self.ui_resetBias(biasSlider))
        m.text(label='=')
        minField = m.floatField(enable=False, value=-5)
        maxField = m.floatField(enable=False, value=95)
        return magnitudeField, biasSlider, minField, maxField

    def ui_getSpace(self):
        for space, menuItem in self.spaceMenuItems.items():
            if m.menuItem(menuItem, q=True, radioButton=True):
                return space
        return SPACE_LOCAL

    def ui_setSpace(self, value):
        if value not in self.spaceMenuItems:
            value = SPACE_LOCAL
        # selecting one radio menu item deselects the others in the collection
        m.menuItem(self.spaceMenuItems[value], e=True, radioButton=True)

    def ui_initSettings(self):
        self.prefSaver.addControl(self.ui_FLTFLD_translateMagnitude, prefsaver.UIType.MFloatField, 1)
        self.prefSaver.addControl(self.ui_FLTFLD_rotateMagnitude, prefsaver.UIType.MFloatField, 180)
        self.prefSaver.addControl(self.ui_FLTFLD_scaleMagnitude, prefsaver.UIType.MFloatField, 2)
        self.prefSaver.addControl(self.ui_INTSLGRP_translateBias, prefsaver.UIType.MIntSliderGrp, 0)
        self.prefSaver.addControl(self.ui_INTSLGRP_rotateBias, prefsaver.UIType.MIntSliderGrp, 0)
        self.prefSaver.addControl(self.ui_INTSLGRP_scaleBias, prefsaver.UIType.MIntSliderGrp, 0)
        self.prefSaver.addControl(self.ui_CHK_useSeed, prefsaver.UIType.MCheckBox, False)
        self.prefSaver.addControl(self.ui_INTSLGRP_seedValue, prefsaver.UIType.MIntSliderGrp, 1234)
        self.prefSaver.addVariable('space', self.ui_getSpace, self.ui_setSpace, SPACE_LOCAL)

    def ui_loadSettings(self):
        self.prefSaver.loadPrefs()
        self.ui_refresh()

    def ui_saveSettings(self, *args):
        # prefs are saved on every change, so closing the window with [X] loses nothing
        if m.window(WIN_NAME, exists=True):
            self.prefSaver.savePrefs()

    def ui_onChange(self, *args):
        self.ui_refresh()
        self.ui_saveSettings()

    def ui_resetSettings(self, *args):
        self.prefSaver.resetPrefs()
        self.ui_onChange()

    def ui_refresh(self, *args):
        for magField, biasSlider, minField, maxField, calc in (
            (self.ui_FLTFLD_translateMagnitude, self.ui_INTSLGRP_translateBias, self.ui_FLTFLD_translateMin, self.ui_FLTFLD_translateMax, calculateMinMax),
            (self.ui_FLTFLD_rotateMagnitude, self.ui_INTSLGRP_rotateBias, self.ui_FLTFLD_rotateMin, self.ui_FLTFLD_rotateMax, calculateMinMax),
            (self.ui_FLTFLD_scaleMagnitude, self.ui_INTSLGRP_scaleBias, self.ui_FLTFLD_scaleMin, self.ui_FLTFLD_scaleMax, calculateMinMaxScale),
        ):
            magnitude = m.floatField(magField, q=True, value=True)
            bias = m.intSliderGrp(biasSlider, q=True, value=True)
            if calc is calculateMinMaxScale and magnitude <= 0:
                _min, _max = 0, 0  # invalid, randomizeScale shows a warning
            else:
                _min, _max = calc(magnitude, bias)
            m.floatField(minField, e=True, value=_min)
            m.floatField(maxField, e=True, value=_max)

        useSeed = m.checkBox(self.ui_CHK_useSeed, q=True, value=True)
        m.intSliderGrp(self.ui_INTSLGRP_seedValue, e=True, enable=useSeed)

    def getSeed(self):
        if not m.checkBox(self.ui_CHK_useSeed, q=True, value=True):
            return None
        return m.intSliderGrp(self.ui_INTSLGRP_seedValue, q=True, value=True)

    def getSelectedTransforms(self):
        return m.ls(sl=True, transforms=True, long=True)

    def ui_resetBias(self, biasSlider):
        m.intSliderGrp(biasSlider, edit=True, value=0)
        self.ui_onChange()

    def randomizeTranslate(self, attrs):
        self.doRandomize(attrs, self.ui_FLTFLD_translateMagnitude, self.ui_INTSLGRP_translateBias)

    def randomizeRotate(self, attrs):
        self.doRandomize(attrs, self.ui_FLTFLD_rotateMagnitude, self.ui_INTSLGRP_rotateBias)

    def randomizeScale(self, attrs):
        self.doRandomize(attrs, self.ui_FLTFLD_scaleMagnitude, self.ui_INTSLGRP_scaleBias)

    def doRandomize(self, attrs, magField, biasSlider):
        self.ui_saveSettings()

        mag = m.floatField(magField, q=True, value=True)
        bias = m.intSliderGrp(biasSlider, q=True, value=True)
        objects = self.getSelectedTransforms()
        if not objects:
            m.warning('{0}: select transforms to randomize.'.format(SCRIPT_NAME))
            return

        try:
            failed = randomize(objects, attrs, mag, bias, self.ui_getSpace(), self.getSeed())
        except ValueError as e:
            m.warning('{0}: {1}'.format(SCRIPT_NAME, e))
            return

        for obj, error in failed:
            print('{0}: {1}: {2}'.format(SCRIPT_NAME, obj, error))
        if failed:
            m.warning('{0}: {1} of {2} object(s) could not be fully randomized (locked or connected attributes?), see the Script Editor.'.format(
                SCRIPT_NAME, len(failed), len(objects)))

    def ui_close(self, *args):
        if m.window(WIN_NAME, exists=True):
            self.ui_saveSettings()
            m.deleteUI(WIN_NAME, window=True)

    def ui_showHelp(self, *args):
        webbrowser.open('http://davydenko.info/transform_randomizer/', new=0, autoraise=True)


def run():
    RandomizerUI()
