import pymel.core as pm


WIN_NAME = 'fxpt_pstest_pymel_win'
MAIN_BUTTONS_HEIGHT = 30


# noinspection PyAttributeOutsideInit
class WinPyMelUI(object):

    def __init__(self):
        self.uiCreate()

    def uiCreate(self):

        self.onCloseClicked()

        self.window = pm.window(
            WIN_NAME,
            title='PyMel Window',
            maximizeButton=False
        )

        with self.window:
            with pm.formLayout() as uiLAY_mainForm:
                with pm.scrollLayout(childResizable=True) as self.uiLAY_mainScroll:
                    with pm.columnLayout(adjustableColumn=True):

                        with self.uiCreateFrame('uiFRM_checkBoxes', 'Check Boxes (PMCheckBox)'):
                            with pm.columnLayout():
                                pm.separator(style='none', height=2)
                                with pm.rowLayout(numberOfColumns=3):
                                    pm.separator(width=140, style='none')
                                    self.uiCHK_test1 = pm.checkBox('uiCHK_test1', label='test1')
                                    self.uiCHK_test2 = pm.checkBox('uiCHK_test2', label='test2')

                        with self.uiCreateFrame('uiFRM_checkBoxGroups', 'Check Box Groups (PMCheckBoxGrp#)'):
                            with pm.columnLayout():
                                pm.separator(style='none', height=2)
                                self.uiCHKGRP_test1 = pm.checkBoxGrp(
                                    'uiCHKGRP_test1',
                                    numberOfCheckBoxes=1,
                                    label='PMCheckBoxGrp1',
                                    label1='test1'
                                )
                                self.uiCHKGRP_test2 = pm.checkBoxGrp(
                                    'uiCHKGRP_test2',
                                    numberOfCheckBoxes=2,
                                    label='PMCheckBoxGrp2',
                                    labelArray2=('test1', 'test2')
                                )
                                self.uiCHKGRP_test3 = pm.checkBoxGrp(
                                    'uiCHKGRP_test3',
                                    numberOfCheckBoxes=3,
                                    label='PMCheckBoxGrp3',
                                    labelArray3=('test1', 'test2', 'test3')
                                )
                                self.uiCHKGRP_test4 = pm.checkBoxGrp(
                                    'uiCHKGRP_test4',
                                    numberOfCheckBoxes=4,
                                    label='PMCheckBoxGrp4',
                                    labelArray4=('test1', 'test2', 'test3', 'test4')
                                )

                        with self.uiCreateFrame('uiFRM_colorSliders', 'Color Slider Groups (PMColorSliderGrp)'):
                            with pm.columnLayout():
                                pm.separator(style='none', height=2)
                                self.uiCLRGRP_test1 = pm.colorSliderGrp(
                                    'uiCLRGRP_test1',
                                    label='test1'
                                )
                                self.uiCLRGRP_test2 = pm.colorSliderGrp(
                                    'uiCLRGRP_test2',
                                    label='test2'
                                )

                        with self.uiCreateFrame('uiFRM_floatFields', 'Float Fields (PMFloatField)'):
                            with pm.columnLayout():
                                pm.separator(style='none', height=2)
                                with pm.rowLayout(numberOfColumns=3):
                                    pm.separator(width=140, style='none')
                                    self.uiFLF_test1 = pm.floatField('uiFLF_test1')
                                    self.uiFLF_test2 = pm.floatField('uiFLF_test2')

                        with self.uiCreateFrame('uiFRM_floatFieldGroups', 'Float Field Groups (PMFloatFieldGrp#)'):
                            with pm.columnLayout():
                                pm.separator(style='none', height=2)
                                self.uiFLFGRP_test1 = pm.floatFieldGrp(
                                    'uiFLFGRP_test1',
                                    numberOfFields=1,
                                    label='PMFloatFieldGrp1'
                                )
                                self.uiFLFGRP_test2 = pm.floatFieldGrp(
                                    'uiFLFGRP_test2',
                                    numberOfFields=2,
                                    label='PMFloatFieldGrp2'
                                )
                                self.uiFLFGRP_test3 = pm.floatFieldGrp(
                                    'uiFLFGRP_test3',
                                    numberOfFields=3,
                                    label='PMFloatFieldGrp3'
                                )
                                self.uiFLFGRP_test4 = pm.floatFieldGrp(
                                    'uiFLFGRP_test4',
                                    numberOfFields=4,
                                    label='PMFloatFieldGrp4'
                                )

                        with self.uiCreateFrame('uiFRM_floatScrollBars', 'Float Scroll Bars (PMFloatScrollBar)'):
                            with pm.columnLayout(adjustableColumn=True):
                                pm.separator(style='none', height=2)
                                self.uiFLSCRL_test1 = pm.floatScrollBar('uiFLSCRL_test1')
                                self.uiFLSCRL_test2 = pm.floatScrollBar('uiFLSCRL_test2')

                        with self.uiCreateFrame('uiFRM_floatSliders', 'Float Sliders (PMFloatSlider)'):
                            with pm.columnLayout(adjustableColumn=True):
                                pm.separator(style='none', height=2)
                                self.uiFLTSLD_test1 = pm.floatSlider('uiFLTSLD_test1')
                                self.uiFLTSLD_test2 = pm.floatSlider('uiFLTSLD_test2')

                        with self.uiCreateFrame('uiFRM_floatSliders2', 'Float Sliders2 (PMFloatSlider2)'):
                            with pm.columnLayout():
                                with pm.rowLayout(numberOfColumns=4):
                                    pm.separator(style='none', width=140)
                                    self.uiFLSLD2_test1 = pm.floatSlider2('uiFLSLD2_test1')
                                    pm.separator(style='none', width=50)
                                    self.uiFLSLD2_test2 = pm.floatSlider2('uiFLSLD2_test2')

                        with self.uiCreateFrame('uiFRM_floatSliderGroups', 'Float Slider Groups (PMFloatSliderGrp)'):
                            with pm.columnLayout():
                                pm.separator(style='none', height=2)
                                self.uiFLSGRP_test1 = pm.floatSliderGrp(
                                    'uiFLSGRP_test1',
                                    label='test1',
                                    field=True
                                )
                                self.uiFLSGRP_test2 = pm.floatSliderGrp(
                                    'uiFLSGRP_test2',
                                    label='test2',
                                    field=True
                                )

                        with self.uiCreateFrame('uiFRM_iconTextCheckBoxes', 'Icon Text Check Boxes (PMIconTextCheckBox)'):
                            with pm.columnLayout():
                                with pm.rowLayout(numberOfColumns=3):
                                    pm.separator(style='none', width=140)
                                    self.uiITCHK_test1 = pm.iconTextCheckBox(
                                        'uiITCHK_test1',
                                        style='iconAndTextHorizontal',
                                        label='cube',
                                        image1='cube'
                                    )
                                    self.uiITCHK_test2 = pm.iconTextCheckBox(
                                        'uiITCHK_test2',
                                        style='iconAndTextHorizontal',
                                        label='cone',
                                        image1='cone'
                                    )

                        with self.uiCreateFrame('uiFRM_iconTextRadioButtons', 'Icon Text Radio Buttons (PMIconTextRadioButton)'):
                            with pm.columnLayout():
                                with pm.rowLayout(numberOfColumns=4):
                                    pm.separator(style='none', width=140)
                                    pm.iconTextRadioCollection()
                                    self.uiITRAD_test1 = pm.iconTextRadioButton(
                                        'uiITRAD_test1',
                                        style='iconAndTextHorizontal',
                                        label='cube',
                                        image1='cube'
                                    )
                                    self.uiITRAD_test2 = pm.iconTextRadioButton(
                                        'uiITRAD_test2',
                                        style='iconAndTextHorizontal',
                                        label='cone',
                                        image1='cone'
                                    )
                                    self.uiITRAD_test3 = pm.iconTextRadioButton(
                                        'uiITRAD_test3',
                                        style='iconAndTextHorizontal',
                                        label='torus',
                                        image1='torus'
                                    )

                        with self.uiCreateFrame('uiFRM_iconTextScrollLists', 'Icon Text Scroll Lists (PMIconTextScrollList)'):
                            with pm.columnLayout():
                                with pm.rowLayout(numberOfColumns=3):
                                    pm.separator(style='none', width=140)
                                    self.uiITSLST_test1 = pm.iconTextScrollList(
                                        'uiITSLST_test1',
                                        allowMultiSelection=True,
                                        append=('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten')
                                    )
                                    self.uiITSLST_test2 = pm.iconTextScrollList(
                                        'uiITSLST_test2',
                                        allowMultiSelection=True,
                                        append=('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten')
                                    )

                        with self.uiCreateFrame('uiFRM_intFields', 'Int Fields (PMIntField)'):
                            with pm.columnLayout():
                                pm.separator(style='none', height=2)
                                with pm.rowLayout(numberOfColumns=3):
                                    pm.separator(width=140, style='none')
                                    self.uiINF_test1 = pm.floatField('uiINF_test1')
                                    self.uiINF_test2 = pm.floatField('uiINF_test2')

                        with self.uiCreateFrame('uiFRM_intFieldGroups', 'Int Field Groups (PMIntFieldGrp#)'):
                            with pm.columnLayout():
                                pm.separator(style='none', height=2)
                                self.uiINFGRP_test1 = pm.intFieldGrp(
                                    'uiINFGRP_test1',
                                    numberOfFields=1,
                                    label='PMIntFieldGrp1'
                                )
                                self.uiINFGRP_test2 = pm.intFieldGrp(
                                    'uiINFGRP_test2',
                                    numberOfFields=2,
                                    label='PMIntFieldGrp2'
                                )
                                self.uiINFGRP_test3 = pm.intFieldGrp(
                                    'uiINFGRP_test3',
                                    numberOfFields=3,
                                    label='PMIntFieldGrp3'
                                )
                                self.uiINFGRP_test4 = pm.intFieldGrp(
                                    'uiINFGRP_test4',
                                    numberOfFields=4,
                                    label='PMIntFieldGrp4'
                                )

                        with self.uiCreateFrame('uiFRM_intScrollBars', 'Int Scroll Bars (PMIntScrollBar)'):
                            with pm.columnLayout(adjustableColumn=True):
                                pm.separator(style='none', height=2)
                                self.uiINSCRL_test1 = pm.intScrollBar('uiINSCRL_test1')
                                self.uiINSCRL_test2 = pm.intScrollBar('uiINSCRL_test2')

                        with self.uiCreateFrame('uiFRM_intSliders', 'Int Sliders (PMIntSlider)'):
                            with pm.columnLayout(adjustableColumn=True):
                                pm.separator(style='none', height=2)
                                self.uiINTSLD_test1 = pm.intSlider('uiINTSLD_test1')
                                self.uiINTSLD_test2 = pm.intSlider('uiINTSLD_test2')

                        with self.uiCreateFrame('uiFRM_intSliderGroups', 'Int Slider Groups (PMIntSliderGrp)'):
                            with pm.columnLayout():
                                pm.separator(style='none', height=2)
                                self.uiINSGRP_test1 = pm.intSliderGrp(
                                    'uiINSGRP_test1',
                                    label='test1',
                                    field=True
                                )
                                self.uiINSGRP_test2 = pm.intSliderGrp(
                                    'uiINSGRP_test2',
                                    label='test2',
                                    field=True
                                )

                        with self.uiCreateFrame('uiFRM_radioButtons', 'Radio Buttons (PMRadioButton)'):
                            with pm.columnLayout():
                                with pm.rowLayout(numberOfColumns=4):
                                    pm.separator(style='none', width=140)
                                    pm.radioCollection()
                                    self.uiRAD_test1 = pm.radioButton('uiRAD_test1', label='test1')
                                    self.uiRAD_test2 = pm.radioButton('uiRAD_test2', label='test2')
                                    self.uiRAD_test3 = pm.radioButton('uiRAD_test3', label='test3')

                        with self.uiCreateFrame('uiFRM_symbolCheckBoxes', 'Symbol Check Boxes (PMSymbolCheckBox)'):
                            with pm.columnLayout():
                                with pm.rowLayout(numberOfColumns=3):
                                    pm.separator(style='none', width=140)
                                    self.uiSYMCHK_test1 = pm.symbolCheckBox(
                                        'uiSYMCHK_test1',
                                        image='polyCube'
                                    )
                                    self.uiSYMCHK_test2 = pm.symbolCheckBox(
                                        'uiSYMCHK_test2',
                                        image='polyCone'
                                    )

                        with self.uiCreateFrame('uiFRM_scriptTables', 'Script Tables (PMScriptTable)'):
                            with pm.columnLayout():
                                with pm.rowLayout(numberOfColumns=3):
                                    pm.separator(style='none', width=140)
                                    self.uiSCRTBL_test1 = pm.scriptTable(
                                        'uiSCRTBL_test1',
                                        selectionMode=3,
                                        rows=4,
                                        columns=2
                                    )
                                    self.uiSCRTBL_test2 = pm.scriptTable(
                                        'uiSCRTBL_test2',
                                        selectionMode=3,
                                        rows=4,
                                        columns=2
                                    )

                        with self.uiCreateFrame('uiFRM_scrollField', 'Scroll Field (PMScrollField)'):
                            with pm.columnLayout():
                                with pm.rowLayout(numberOfColumns=3):
                                    pm.separator(style='none', width=140)
                                    self.uiSCRFLD_test1 = pm.scrollField(
                                        'uiSCRFLD_test1',
                                        wordWrap=True
                                    )
                                    self.uiSCRFLD_test2 = pm.scrollField(
                                        'uiSCRFLD_test2',
                                        wordWrap=True
                                    )

                        with self.uiCreateFrame('uiFRM_shelfTabLayout', 'Shelf Tab Layout (PMShelfTabLayout)'):
                            with pm.columnLayout(adjustableColumn=True):
                                with pm.shelfTabLayout() as self.uiSHLTAB_test1:
                                    with pm.shelfLayout('test1'):
                                        pass
                                    with pm.shelfLayout('test2'):
                                        pass
                                    with pm.shelfLayout('test3'):
                                        pass
                                with pm.shelfTabLayout() as self.uiSHLTAB_test2:
                                    with pm.shelfLayout('test4'):
                                        pass
                                    with pm.shelfLayout('test5'):
                                        pass
                                    with pm.shelfLayout('test6'):
                                        pass

                        with self.uiCreateFrame('uiFRM_tabLayout', 'Tab Layout (PMTabLayout)'):
                            with pm.columnLayout(adjustableColumn=True):
                                with pm.tabLayout() as self.uiTAB_test1:

                                    with pm.rowLayout(numberOfColumns=1) as uiLAY_tabRow1:
                                        pass
                                    with pm.rowLayout(numberOfColumns=1) as uiLAY_tabRow2:
                                        pass
                                    with pm.rowLayout(numberOfColumns=1) as uiLAY_tabRow3:
                                        pass

                                pm.tabLayout(
                                    self.uiTAB_test1,
                                    edit=True,
                                    tabLabel=((uiLAY_tabRow1, 'test1'), (uiLAY_tabRow2, 'test2'), (uiLAY_tabRow3, 'test3'),)
                                )

                                with pm.tabLayout() as self.uiTAB_test2:

                                    with pm.rowLayout(numberOfColumns=1) as uiLAY_tabRow4:
                                        pass
                                    with pm.rowLayout(numberOfColumns=1) as uiLAY_tabRow5:
                                        pass
                                    with pm.rowLayout(numberOfColumns=1) as uiLAY_tabRow6:
                                        pass

                                pm.tabLayout(
                                    self.uiTAB_test2,
                                    edit=True,
                                    tabLabel=((uiLAY_tabRow4, 'test4'), (uiLAY_tabRow5, 'test5'), (uiLAY_tabRow6, 'test6'),)
                                )

                        with self.uiCreateFrame('uiFRM_textFields', 'Text Fields (PMTextField)'):
                            with pm.columnLayout():
                                pm.separator(style='none', height=2)
                                with pm.rowLayout(numberOfColumns=3):
                                    pm.separator(width=140, style='none')
                                    self.uiTXT_test1 = pm.textField('uiTXT_test1')
                                    self.uiTXT_test2 = pm.textField('uiTXT_test2')

                        with self.uiCreateFrame('uiFRM_textFieldButtonGroups', 'Text Field Button Groups (PMTextFieldButtonGrp)'):
                            with pm.columnLayout():
                                pm.separator(style='none', height=2)
                                self.uiTXBTGR_test1 = pm.textFieldButtonGrp(
                                    'uiTXBTGR_test1',
                                    label='test1',
                                    buttonLabel='button1'
                                )
                                self.uiTXBTGR_test2 = pm.textFieldButtonGrp(
                                    'uiTXBTGR_test2',
                                    label='test2',
                                    buttonLabel='button2'
                                )

                        with self.uiCreateFrame('uiFRM_textFieldGroups', 'Text Field Groups (PMTextFieldGrp)'):
                            with pm.columnLayout():
                                pm.separator(style='none', height=2)
                                self.uiTXTGRP_test1 = pm.textFieldGrp(
                                    'uiTXTGRP_test1',
                                    label='test1'
                                )
                                self.uiTXTGRP_test2 = pm.textFieldGrp(
                                    'uiTXTGRP_test2',
                                    label='test2'
                                )

                        with self.uiCreateFrame('uiFRM_textScrollLists', 'Text Scroll Lists (PMTextScrollList)'):
                            with pm.columnLayout():
                                with pm.rowLayout(numberOfColumns=3):
                                    pm.separator(style='none', width=140)
                                    self.uiTXTLST_test1 = pm.textScrollList(
                                        'uiTXTLST_test1',
                                        allowMultiSelection=True,
                                        append=('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten')
                                    )
                                    self.uiTXTLST_test2 = pm.textScrollList(
                                        'uiTXTLST_test2',
                                        allowMultiSelection=True,
                                        append=('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten')
                                    )


                self.uiBTN_savePrefs = pm.button(
                    label='Save Prefs',
                    height=MAIN_BUTTONS_HEIGHT,
                    command=self.onCloseClicked
                )

                self.uiBTN_loadPrefs = pm.button(
                    label='Load Prefs',
                    height=MAIN_BUTTONS_HEIGHT,
                    command=self.onCloseClicked
                )

                self.uiBTN_resetPrefs = pm.button(
                    label='Reset Prefs',
                    height=MAIN_BUTTONS_HEIGHT,
                    command=self.onCloseClicked
                )

                uiLAY_mainForm.attachForm(self.uiLAY_mainScroll, 'top', 2)
                uiLAY_mainForm.attachForm(self.uiLAY_mainScroll, 'left', 2)
                uiLAY_mainForm.attachForm(self.uiLAY_mainScroll, 'right', 2)
                uiLAY_mainForm.attachControl(self.uiLAY_mainScroll, 'bottom', 2, self.uiBTN_savePrefs)

                uiLAY_mainForm.attachNone(self.uiBTN_savePrefs, 'top')
                uiLAY_mainForm.attachForm(self.uiBTN_savePrefs, 'left', 2)
                uiLAY_mainForm.attachPosition(self.uiBTN_savePrefs, 'right', 2, 33)
                uiLAY_mainForm.attachForm(self.uiBTN_savePrefs, 'bottom', 2)

                uiLAY_mainForm.attachNone(self.uiBTN_loadPrefs, 'top')
                uiLAY_mainForm.attachPosition(self.uiBTN_loadPrefs, 'left', 2, 33)
                uiLAY_mainForm.attachPosition(self.uiBTN_loadPrefs, 'right', 2, 66)
                uiLAY_mainForm.attachForm(self.uiBTN_loadPrefs, 'bottom', 2)

                uiLAY_mainForm.attachNone(self.uiBTN_resetPrefs, 'top')
                uiLAY_mainForm.attachPosition(self.uiBTN_resetPrefs, 'left', 2, 66)
                uiLAY_mainForm.attachForm(self.uiBTN_resetPrefs, 'right', 2)
                uiLAY_mainForm.attachForm(self.uiBTN_resetPrefs, 'bottom', 2)

    # noinspection PyMethodMayBeStatic
    def uiCreateFrame(self, controlName, name, collapsed=False):
        return pm.frameLayout(
            controlName,
            label=name,
            collapsable=True,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True,
            collapse=collapsed
        )

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def onCloseClicked(self, *args):
        if pm.window(WIN_NAME, exists=True):
            pm.deleteUI(WIN_NAME, window=True)


def run():
    WinPyMelUI()