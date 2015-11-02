import os

import maya.cmds as m

from fxpt.fx_prefsaver import prefsaver
from fxpt.fx_prefsaver.serializers import SerializerOptVar, SerializerFileJson, SerializerFilePickle

WIN_NAME = 'fxpt_pstest_maya_win'
MAIN_BUTTONS_HEIGHT = 30

CFG_FILENAME = os.path.dirname(__file__) + '\\prefsM.cfg'


# noinspection PyAttributeOutsideInit
class WinMayaUI(object):
    def __init__(self, serializer):
        self.uiCreate()

        self.prefSaver = prefsaver.PrefSaver(self.createSerializer(serializer))
        self.initPrefs()

    def uiCreate(self):

        self.onCloseClicked()

        self.window = m.window(
            WIN_NAME,
            title='Maya Window',
            maximizeButton=False
        )

        uiLAY_mainForm = m.formLayout()

        self.uiLAY_mainScroll = m.scrollLayout(childResizable=True)

        mainColumn = m.columnLayout(adjustableColumn=True)  # main column layout with frames

        # --------
        self.uiLAY_frameCheckBoxes = self.uiCreateFrame('uiLAY_frameCheckBoxes', 'Check Boxes (PMCheckBox)')

        m.columnLayout()

        m.separator(style='none', height=2)

        m.rowLayout(numberOfColumns=3)

        m.separator(width=140, style='none')
        self.uiCHK_test1 = m.checkBox('uiCHK_test1', label='test1')
        self.uiCHK_test2 = m.checkBox('uiCHK_test2', label='test2')

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameCheckBoxGroups = self.uiCreateFrame('uiLAY_frameCheckBoxGroups',
                                                            'Check Box Groups (PMCheckBoxGrp#)')

        m.columnLayout()

        m.separator(style='none', height=2)
        self.uiCHKGRP_test1 = m.checkBoxGrp(
            'uiCHKGRP_test1',
            numberOfCheckBoxes=1,
            label='PMCheckBoxGrp1',
            label1='test1'
        )
        self.uiCHKGRP_test2 = m.checkBoxGrp(
            'uiCHKGRP_test2',
            numberOfCheckBoxes=2,
            label='PMCheckBoxGrp2',
            labelArray2=('test1', 'test2')
        )
        self.uiCHKGRP_test3 = m.checkBoxGrp(
            'uiCHKGRP_test3',
            numberOfCheckBoxes=3,
            label='PMCheckBoxGrp3',
            labelArray3=('test1', 'test2', 'test3')
        )
        self.uiCHKGRP_test4 = m.checkBoxGrp(
            'uiCHKGRP_test4',
            numberOfCheckBoxes=4,
            label='PMCheckBoxGrp4',
            labelArray4=('test1', 'test2', 'test3', 'test4')
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameColorSliders = self.uiCreateFrame('uiLAY_frameColorSliders',
                                                          'Color Slider Groups (PMColorSliderGrp)')

        m.columnLayout()

        m.separator(style='none', height=2)
        self.uiCLRGRP_test1 = m.colorSliderGrp(
            'uiCLRGRP_test1',
            label='test1'
        )
        self.uiCLRGRP_test2 = m.colorSliderGrp(
            'uiCLRGRP_test2',
            label='test2'
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameFloatFields = self.uiCreateFrame('uiLAY_frameFloatFields', 'Float Fields (PMFloatField)')

        m.columnLayout()

        m.separator(style='none', height=2)

        m.rowLayout(numberOfColumns=3)
        m.separator(width=140, style='none')
        self.uiFLF_test1 = m.floatField('uiFLF_test1')
        self.uiFLF_test2 = m.floatField('uiFLF_test2')

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameFloatFieldGroups = self.uiCreateFrame('uiLAY_frameFloatFieldGroups',
                                                              'Float Field Groups (PMFloatFieldGrp#)')

        m.columnLayout()

        m.separator(style='none', height=2)
        self.uiFLFGRP_test1 = m.floatFieldGrp(
            'uiFLFGRP_test1',
            numberOfFields=1,
            label='PMFloatFieldGrp1'
        )
        self.uiFLFGRP_test2 = m.floatFieldGrp(
            'uiFLFGRP_test2',
            numberOfFields=2,
            label='PMFloatFieldGrp2'
        )
        self.uiFLFGRP_test3 = m.floatFieldGrp(
            'uiFLFGRP_test3',
            numberOfFields=3,
            label='PMFloatFieldGrp3'
        )
        self.uiFLFGRP_test4 = m.floatFieldGrp(
            'uiFLFGRP_test4',
            numberOfFields=4,
            label='PMFloatFieldGrp4'
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameFloatScrollBars = self.uiCreateFrame('uiLAY_frameFloatScrollBars',
                                                             'Float Scroll Bars (PMFloatScrollBar)')

        m.columnLayout(adjustableColumn=True)

        m.separator(style='none', height=2)
        self.uiFLSCRL_test1 = m.floatScrollBar('uiFLSCRL_test1')
        self.uiFLSCRL_test2 = m.floatScrollBar('uiFLSCRL_test2')

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameFloatSliders = self.uiCreateFrame('uiLAY_frameFloatSliders', 'Float Sliders (PMFloatSlider)')

        m.columnLayout(adjustableColumn=True)

        m.separator(style='none', height=2)
        self.uiFLTSLD_test1 = m.floatSlider('uiFLTSLD_test1')
        self.uiFLTSLD_test2 = m.floatSlider('uiFLTSLD_test2')

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameFloatSliderGroups = self.uiCreateFrame('uiLAY_frameFloatSliderGroups',
                                                               'Float Slider Groups (PMFloatSliderGrp)')
        m.columnLayout()
        m.separator(style='none', height=2)
        self.uiFLSGRP_test1 = m.floatSliderGrp(
            'uiFLSGRP_test1',
            label='test1',
            field=True
        )
        self.uiFLSGRP_test2 = m.floatSliderGrp(
            'uiFLSGRP_test2',
            label='test2',
            field=True
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameIconTextCheckBoxes = self.uiCreateFrame('uiLAY_frameIconTextCheckBoxes',
                                                                'Icon Text Check Boxes (PMIconTextCheckBox)')

        m.columnLayout()

        m.rowLayout(numberOfColumns=3)

        m.separator(style='none', width=140)
        self.uiITCHK_test1 = m.iconTextCheckBox(
            'uiITCHK_test1',
            style='iconAndTextHorizontal',
            label='cube',
            image1='cube'
        )
        self.uiITCHK_test2 = m.iconTextCheckBox(
            'uiITCHK_test2',
            style='iconAndTextHorizontal',
            label='cone',
            image1='cone'
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameIconTextRadioButtons = self.uiCreateFrame('uiLAY_frameIconTextRadioButtons',
                                                                  'Icon Text Radio Buttons (PMIconTextRadioButton)')

        m.columnLayout()

        m.rowLayout(numberOfColumns=4)

        m.separator(style='none', width=140)
        m.iconTextRadioCollection()
        self.uiITRAD_test1 = m.iconTextRadioButton(
            'uiITRAD_test1',
            style='iconAndTextHorizontal',
            label='cube',
            image1='cube'
        )
        self.uiITRAD_test2 = m.iconTextRadioButton(
            'uiITRAD_test2',
            style='iconAndTextHorizontal',
            label='cone',
            image1='cone'
        )
        self.uiITRAD_test3 = m.iconTextRadioButton(
            'uiITRAD_test3',
            style='iconAndTextHorizontal',
            label='torus',
            image1='torus'
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameIconTextScrollLists = self.uiCreateFrame('uiLAY_frameIconTextScrollLists',
                                                                 'Icon Text Scroll Lists (PMIconTextScrollList)')

        m.columnLayout()

        m.rowLayout(numberOfColumns=3)

        m.separator(style='none', width=140)
        self.uiITSLST_test1 = m.iconTextScrollList(
            'uiITSLST_test1',
            allowMultiSelection=True,
            append=('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten')
        )
        self.uiITSLST_test2 = m.iconTextScrollList(
            'uiITSLST_test2',
            allowMultiSelection=True,
            append=('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten')
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameIntFields = self.uiCreateFrame('uiLAY_frameIntFields', 'Int Fields (PMIntField)')

        m.columnLayout()

        m.separator(style='none', height=2)

        m.rowLayout(numberOfColumns=3)

        m.separator(width=140, style='none')
        self.uiINF_test1 = m.intField('uiINF_test1')
        self.uiINF_test2 = m.intField('uiINF_test2')

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameIntFieldGroups = self.uiCreateFrame('uiLAY_frameIntFieldGroups',
                                                            'Int Field Groups (PMIntFieldGrp#)')

        m.columnLayout()

        m.separator(style='none', height=2)
        self.uiINFGRP_test1 = m.intFieldGrp(
            'uiINFGRP_test1',
            numberOfFields=1,
            label='PMIntFieldGrp1'
        )
        self.uiINFGRP_test2 = m.intFieldGrp(
            'uiINFGRP_test2',
            numberOfFields=2,
            label='PMIntFieldGrp2'
        )
        self.uiINFGRP_test3 = m.intFieldGrp(
            'uiINFGRP_test3',
            numberOfFields=3,
            label='PMIntFieldGrp3'
        )
        self.uiINFGRP_test4 = m.intFieldGrp(
            'uiINFGRP_test4',
            numberOfFields=4,
            label='PMIntFieldGrp4'
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameIntScrollBars = self.uiCreateFrame('uiLAY_frameIntScrollBars',
                                                           'Int Scroll Bars (PMIntScrollBar)')

        m.columnLayout(adjustableColumn=True)

        m.separator(style='none', height=2)
        self.uiINSCRL_test1 = m.intScrollBar('uiINSCRL_test1')
        self.uiINSCRL_test2 = m.intScrollBar('uiINSCRL_test2')

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameIntSliders = self.uiCreateFrame('uiLAY_frameIntSliders', 'Int Sliders (PMIntSlider)')

        m.columnLayout(adjustableColumn=True)

        m.separator(style='none', height=2)
        self.uiINTSLD_test1 = m.intSlider('uiINTSLD_test1')
        self.uiINTSLD_test2 = m.intSlider('uiINTSLD_test2')

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameIntSliderGroups = self.uiCreateFrame('uiLAY_frameIntSliderGroups',
                                                             'Int Slider Groups (PMIntSliderGrp)')

        m.columnLayout()

        m.separator(style='none', height=2)
        self.uiINSGRP_test1 = m.intSliderGrp(
            'uiINSGRP_test1',
            label='test1',
            field=True
        )
        self.uiINSGRP_test2 = m.intSliderGrp(
            'uiINSGRP_test2',
            label='test2',
            field=True
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameOptionMenus = self.uiCreateFrame('uiLAY_frameOptionMenus', 'Option Menus (PMOptionMenu)')

        m.columnLayout()

        m.separator(style='none', height=2)

        m.rowLayout(numberOfColumns=3)

        m.separator(width=110, style='none')
        self.uiOPTMNU_test1 = m.optionMenu('uiOPTMNU_test1', label='test1')
        m.menuItem(label='one')
        m.menuItem(label='two')
        m.menuItem(label='three')
        self.uiOPTMNU_test2 = m.optionMenu('uiOPTMNU_test2', label='test2')
        m.menuItem(label='four')
        m.menuItem(label='five')
        m.menuItem(label='six')

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameOptionMenuGroups = self.uiCreateFrame('uiLAY_frameOptionMenuGroups',
                                                              'Option Menus Groups (PMOptionMenuGrp)')

        m.columnLayout()

        m.separator(style='none', height=2)
        self.uiOPMGRP_test1 = m.optionMenuGrp('uiOPMGRP_test1', label='test1', extraLabel='extraLabel')
        m.menuItem(label='one')
        m.menuItem(label='two')
        m.menuItem(label='three')
        self.uiOPMGRP_test2 = m.optionMenuGrp('uiOPMGRP_test2', label='test2', extraLabel='extraLabel')
        m.menuItem(label='four')
        m.menuItem(label='five')
        m.menuItem(label='six')

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameRadioButtons = self.uiCreateFrame('uiLAY_frameRadioButtons', 'Radio Buttons (PMRadioButton)')

        m.columnLayout()

        m.rowLayout(numberOfColumns=4)

        m.separator(style='none', width=140)
        m.radioCollection()
        self.uiRAD_test1 = m.radioButton('uiRAD_test1', label='test1')
        self.uiRAD_test2 = m.radioButton('uiRAD_test2', label='test2')
        self.uiRAD_test3 = m.radioButton('uiRAD_test3', label='test3')

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameRadioButtonGroups = self.uiCreateFrame('uiLAY_frameRadioButtonGroups',
                                                               'Radio Button Groups (PMRadioButtonGrp#)')

        m.columnLayout()
        m.separator(style='none', height=2)
        self.uiRADGRP_test1 = m.radioButtonGrp(
            'uiRADGRP_test1',
            numberOfRadioButtons=1,
            label='PMRadioButtonGrp1',
            label1='test1'
        )
        self.uiRADGRP_test2 = m.radioButtonGrp(
            'uiRADGRP_test2',
            numberOfRadioButtons=2,
            label='PMRadioButtonGrp2',
            labelArray2=('test1', 'test2')
        )
        self.uiRADGRP_test3 = m.radioButtonGrp(
            'uiRADGRP_test3',
            numberOfRadioButtons=3,
            label='PMRadioButtonGrp3',
            labelArray3=('test1', 'test2', 'test3')
        )
        self.uiRADGRP_test4 = m.radioButtonGrp(
            'uiRADGRP_test4',
            numberOfRadioButtons=4,
            label='PMRadioButtonGrp4',
            labelArray4=('test1', 'test2', 'test3', 'test4')
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameSymbolCheckBoxes = self.uiCreateFrame('uiLAY_frameSymbolCheckBoxes',
                                                              'Symbol Check Boxes (PMSymbolCheckBox)')

        m.columnLayout()

        m.rowLayout(numberOfColumns=3)

        m.separator(style='none', width=140)
        self.uiSYMCHK_test1 = m.symbolCheckBox(
            'uiSYMCHK_test1',
            image='polyCube'
        )
        self.uiSYMCHK_test2 = m.symbolCheckBox(
            'uiSYMCHK_test2',
            image='polyCone'
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameScriptTables = self.uiCreateFrame('uiLAY_frameScriptTables', 'Script Tables (PMScriptTable)')

        m.columnLayout()

        m.rowLayout(numberOfColumns=3)

        m.separator(style='none', width=140)
        self.uiSCRTBL_test1 = m.scriptTable(
            'uiSCRTBL_test1',
            selectionMode=3,
            rows=4,
            columns=2
        )
        self.uiSCRTBL_test2 = m.scriptTable(
            'uiSCRTBL_test2',
            selectionMode=3,
            rows=4,
            columns=2
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameScrollField = self.uiCreateFrame('uiLAY_frameScrollField', 'Scroll Field (PMScrollField)')

        m.columnLayout()

        m.rowLayout(numberOfColumns=3)

        m.separator(style='none', width=140)
        self.uiSCRFLD_test1 = m.scrollField(
            'uiSCRFLD_test1',
            wordWrap=True
        )
        self.uiSCRFLD_test2 = m.scrollField(
            'uiSCRFLD_test2',
            wordWrap=True
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameShelfTabLayout = self.uiCreateFrame('uiLAY_frameShelfTabLayout',
                                                            'Shelf Tab Layout (PMShelfTabLayout)')

        m.columnLayout(adjustableColumn=True)

        self.uiSHLTAB_test1 = m.shelfTabLayout()

        m.shelfLayout('test1')
        m.setParent('..')
        m.shelfLayout('test2')
        m.setParent('..')
        m.shelfLayout('test3')
        m.setParent('..')

        m.setParent('..')

        self.uiSHLTAB_test2 = m.shelfTabLayout()

        m.shelfLayout('test4')
        m.setParent('..')
        m.shelfLayout('test5')
        m.setParent('..')
        m.shelfLayout('test6')
        m.setParent('..')

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameTabLayout = self.uiCreateFrame('uiLAY_frameTabLayout', 'Tab Layout (PMTabLayout)')

        m.columnLayout(adjustableColumn=True)

        self.uiTAB_test1 = m.tabLayout()

        uiLAY_tabRow1 = m.rowLayout(numberOfColumns=1)
        m.setParent('..')
        uiLAY_tabRow2 = m.rowLayout(numberOfColumns=1)
        m.setParent('..')
        uiLAY_tabRow3 = m.rowLayout(numberOfColumns=1)
        m.setParent('..')

        m.setParent('..')

        m.tabLayout(
            self.uiTAB_test1,
            edit=True,
            tabLabel=((uiLAY_tabRow1, 'test1'), (uiLAY_tabRow2, 'test2'), (uiLAY_tabRow3, 'test3'),)
        )

        self.uiTAB_test2 = m.tabLayout()

        uiLAY_tabRow4 = m.rowLayout(numberOfColumns=1)
        m.setParent('..')
        uiLAY_tabRow5 = m.rowLayout(numberOfColumns=1)
        m.setParent('..')
        uiLAY_tabRow6 = m.rowLayout(numberOfColumns=1)
        m.setParent('..')

        m.setParent('..')

        m.tabLayout(
            self.uiTAB_test2,
            edit=True,
            tabLabel=((uiLAY_tabRow4, 'test4'), (uiLAY_tabRow5, 'test5'), (uiLAY_tabRow6, 'test6'),)
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameTextFields = self.uiCreateFrame('uiLAY_frameTextFields', 'Text Fields (PMTextField)')

        m.columnLayout()

        m.separator(style='none', height=2)

        m.rowLayout(numberOfColumns=3)

        m.separator(width=140, style='none')
        self.uiTXT_test1 = m.textField('uiTXT_test1')
        self.uiTXT_test2 = m.textField('uiTXT_test2')

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameTextFieldButtonGroups = self.uiCreateFrame('uiLAY_frameTextFieldButtonGroups',
                                                                   'Text Field Button Groups (PMTextFieldButtonGrp)')

        m.columnLayout()

        m.separator(style='none', height=2)
        self.uiTXBTGR_test1 = m.textFieldButtonGrp(
            'uiTXBTGR_test1',
            label='test1',
            buttonLabel='button1'
        )
        self.uiTXBTGR_test2 = m.textFieldButtonGrp(
            'uiTXBTGR_test2',
            label='test2',
            buttonLabel='button2'
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameTextFieldGroups = self.uiCreateFrame('uiLAY_frameTextFieldGroups',
                                                             'Text Field Groups (PMTextFieldGrp)')

        m.columnLayout()

        m.separator(style='none', height=2)
        self.uiTXTGRP_test1 = m.textFieldGrp(
            'uiTXTGRP_test1',
            label='test1'
        )
        self.uiTXTGRP_test2 = m.textFieldGrp(
            'uiTXTGRP_test2',
            label='test2'
        )

        m.setParent(mainColumn)

        # --------
        self.uiLAY_frameTextScrollLists = self.uiCreateFrame('uiLAY_frameTextScrollLists',
                                                             'Text Scroll Lists (PMTextScrollList)')

        m.columnLayout()

        m.rowLayout(numberOfColumns=3)

        m.separator(style='none', width=140)
        self.uiTXTLST_test1 = m.textScrollList(
            'uiTXTLST_test1',
            allowMultiSelection=True,
            append=('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten')
        )
        self.uiTXTLST_test2 = m.textScrollList(
            'uiTXTLST_test2',
            allowMultiSelection=True,
            append=('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten')
        )

        # --------
        m.setParent(uiLAY_mainForm)

        self.uiBTN_savePrefs = m.button(
            label='Save Prefs',
            height=MAIN_BUTTONS_HEIGHT,
            command=self.onSavePrefsClicked
        )

        self.uiBTN_loadPrefs = m.button(
            label='Load Prefs',
            height=MAIN_BUTTONS_HEIGHT,
            command=self.onLoadPrefsClicked
        )

        self.uiBTN_resetPrefs = m.button(
            label='Reset Prefs',
            height=MAIN_BUTTONS_HEIGHT,
            command=self.onResetPrefsClicked
        )

        m.setParent('..')  # -> window

        m.formLayout(uiLAY_mainForm, e=True, attachForm=[(self.uiLAY_mainScroll, 'top', 2)])
        m.formLayout(uiLAY_mainForm, e=True, attachForm=[(self.uiLAY_mainScroll, 'left', 2)])
        m.formLayout(uiLAY_mainForm, e=True, attachForm=[(self.uiLAY_mainScroll, 'right', 2)])
        m.formLayout(uiLAY_mainForm, e=True, attachControl=[(self.uiLAY_mainScroll, 'bottom', 2, self.uiBTN_savePrefs)])

        m.formLayout(uiLAY_mainForm, e=True, attachNone=[(self.uiBTN_savePrefs, 'top')])
        m.formLayout(uiLAY_mainForm, e=True, attachForm=[(self.uiBTN_savePrefs, 'left', 2)])
        m.formLayout(uiLAY_mainForm, e=True, attachPosition=[(self.uiBTN_savePrefs, 'right', 2, 33)])
        m.formLayout(uiLAY_mainForm, e=True, attachForm=[(self.uiBTN_savePrefs, 'bottom', 2)])

        m.formLayout(uiLAY_mainForm, e=True, attachNone=[(self.uiBTN_loadPrefs, 'top')])
        m.formLayout(uiLAY_mainForm, e=True, attachPosition=[(self.uiBTN_loadPrefs, 'left', 2, 33)])
        m.formLayout(uiLAY_mainForm, e=True, attachPosition=[(self.uiBTN_loadPrefs, 'right', 2, 66)])
        m.formLayout(uiLAY_mainForm, e=True, attachForm=[(self.uiBTN_loadPrefs, 'bottom', 2)])

        m.formLayout(uiLAY_mainForm, e=True, attachNone=[(self.uiBTN_resetPrefs, 'top')])
        m.formLayout(uiLAY_mainForm, e=True, attachPosition=[(self.uiBTN_resetPrefs, 'left', 2, 66)])
        m.formLayout(uiLAY_mainForm, e=True, attachForm=[(self.uiBTN_resetPrefs, 'right', 2)])
        m.formLayout(uiLAY_mainForm, e=True, attachForm=[(self.uiBTN_resetPrefs, 'bottom', 2)])

        m.showWindow(self.window)

    # noinspection PyMethodMayBeStatic
    def uiCreateFrame(self, controlName, name, collapsed=False):
        return m.frameLayout(
            controlName,
            label=name,
            collapsable=True,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True,
            collapse=collapsed
        )

    # noinspection PyMethodMayBeStatic
    def createSerializer(self, ser):
        if ser == 'SerializerFilePickle':
            return SerializerFilePickle(CFG_FILENAME)
        if ser == 'SerializerFileJson':
            return SerializerFileJson(CFG_FILENAME)
        elif ser == 'SerializerOptVar':
            return SerializerOptVar('TestMayaWindow')
        else:
            assert False, 'Unknown serializer type'

    # noinspection PyUnresolvedReferences
    def initPrefs(self, defaults=False):

        controlList = [
            (self.uiLAY_frameCheckBoxes, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameCheckBoxGroups, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameColorSliders, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameFloatFields, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameFloatFieldGroups, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameFloatScrollBars, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameFloatSliders, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameFloatSliderGroups, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameIconTextCheckBoxes, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameIconTextRadioButtons, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameIconTextScrollLists, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameIntFields, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameIntFieldGroups, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameIntScrollBars, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameIntSliders, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameIntSliderGroups, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameOptionMenus, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameOptionMenuGroups, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameRadioButtons, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameRadioButtonGroups, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameSymbolCheckBoxes, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameScriptTables, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameScrollField, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameShelfTabLayout, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameTabLayout, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameTextFields, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameTextFieldButtonGroups, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameTextFieldGroups, prefsaver.UIType.MFrameLayout, False),
            (self.uiLAY_frameTextScrollLists, prefsaver.UIType.MFrameLayout, False),

            (self.uiCHK_test1, prefsaver.UIType.MCheckBox, False),
            (self.uiCHK_test2, prefsaver.UIType.MCheckBox, False),
            (self.uiCHKGRP_test1, prefsaver.UIType.MCheckBoxGrp1, [False]),
            (self.uiCHKGRP_test2, prefsaver.UIType.MCheckBoxGrp2, [False, False]),
            (self.uiCHKGRP_test3, prefsaver.UIType.MCheckBoxGrp3, [False, False, False]),
            (self.uiCHKGRP_test4, prefsaver.UIType.MCheckBoxGrp4, [False, False, False, False]),
            (self.uiCLRGRP_test1, prefsaver.UIType.MColorSliderGrp, [1, 0.5, 0.5]),
            (self.uiCLRGRP_test2, prefsaver.UIType.MColorSliderGrp, [0.5, 1, 0.5]),
            (self.uiFLF_test1, prefsaver.UIType.MFloatField, 4.568),
            (self.uiFLF_test2, prefsaver.UIType.MFloatField, 15.5),
            (self.uiFLFGRP_test1, prefsaver.UIType.MFloatFieldGrp1, [1.1]),
            (self.uiFLFGRP_test2, prefsaver.UIType.MFloatFieldGrp2, [1.1, 2.2]),
            (self.uiFLFGRP_test3, prefsaver.UIType.MFloatFieldGrp3, [1.1, 2.2, 3.3]),
            (self.uiFLFGRP_test4, prefsaver.UIType.MFloatFieldGrp4, [1.1, 2.2, 3.3, 4.4]),
            (self.uiFLSCRL_test1, prefsaver.UIType.MFloatScrollBar, 40),
            (self.uiFLSCRL_test2, prefsaver.UIType.MFloatScrollBar, 60),
            (self.uiFLTSLD_test1, prefsaver.UIType.MFloatSlider, 40),
            (self.uiFLTSLD_test2, prefsaver.UIType.MFloatSlider, 60),
            (self.uiFLSGRP_test1, prefsaver.UIType.MFloatSliderGrp, 40),
            (self.uiFLSGRP_test2, prefsaver.UIType.MFloatSliderGrp, 60),
            (self.uiLAY_mainScroll, prefsaver.UIType.MScrollLayout, [0, 0]),
            (self.uiITCHK_test1, prefsaver.UIType.MIconTextCheckBox, False),
            (self.uiITCHK_test2, prefsaver.UIType.MIconTextCheckBox, False),
            (self.uiITRAD_test1, prefsaver.UIType.MIconTextRadioButton, False),
            (self.uiITRAD_test2, prefsaver.UIType.MIconTextRadioButton, False),
            (self.uiITRAD_test3, prefsaver.UIType.MIconTextRadioButton, True),
            (self.uiITSLST_test1, prefsaver.UIType.MIconTextScrollList, []),
            (self.uiITSLST_test2, prefsaver.UIType.MIconTextScrollList, []),
            (self.uiINF_test1, prefsaver.UIType.MIntField, 1),
            (self.uiINF_test2, prefsaver.UIType.MIntField, 2),
            (self.uiINFGRP_test1, prefsaver.UIType.MIntFieldGrp1, [1]),
            (self.uiINFGRP_test2, prefsaver.UIType.MIntFieldGrp2, [2, 2]),
            (self.uiINFGRP_test3, prefsaver.UIType.MIntFieldGrp3, [3, 3, 3]),
            (self.uiINFGRP_test4, prefsaver.UIType.MIntFieldGrp4, [4, 4, 4, 4]),
            (self.uiINSCRL_test1, prefsaver.UIType.MIntScrollBar, 40),
            (self.uiINSCRL_test2, prefsaver.UIType.MIntScrollBar, 60),
            (self.uiINTSLD_test1, prefsaver.UIType.MIntSlider, 40),
            (self.uiINTSLD_test2, prefsaver.UIType.MIntSlider, 60),
            (self.uiINSGRP_test1, prefsaver.UIType.MIntSliderGrp, 40),
            (self.uiINSGRP_test2, prefsaver.UIType.MIntSliderGrp, 60),
            (self.uiOPTMNU_test1, prefsaver.UIType.MOptionMenu, 1),
            (self.uiOPTMNU_test2, prefsaver.UIType.MOptionMenu, 2),
            (self.uiOPMGRP_test1, prefsaver.UIType.MOptionMenuGrp, 1),
            (self.uiOPMGRP_test2, prefsaver.UIType.MOptionMenuGrp, 2),
            (self.uiRAD_test1, prefsaver.UIType.MRadioButton, False),
            (self.uiRAD_test2, prefsaver.UIType.MRadioButton, False),
            (self.uiRAD_test3, prefsaver.UIType.MRadioButton, True),
            (self.uiRADGRP_test1, prefsaver.UIType.MRadioButtonGrp1, 1),
            (self.uiRADGRP_test2, prefsaver.UIType.MRadioButtonGrp2, 2),
            (self.uiRADGRP_test3, prefsaver.UIType.MRadioButtonGrp3, 3),
            (self.uiRADGRP_test4, prefsaver.UIType.MRadioButtonGrp4, 4),
            (self.uiSYMCHK_test1, prefsaver.UIType.MSymbolCheckBox, False),
            (self.uiSYMCHK_test2, prefsaver.UIType.MSymbolCheckBox, True),
            (self.uiSCRTBL_test1, prefsaver.UIType.MScriptTable, [0, 0]),  # [0, 0] equals to "select nothing"
            (self.uiSCRTBL_test2, prefsaver.UIType.MScriptTable, [0, 0]),
            (self.uiSCRFLD_test1, prefsaver.UIType.MScrollField, 'default text'),
            (self.uiSCRFLD_test2, prefsaver.UIType.MScrollField, 'default text'),
            (self.uiSHLTAB_test1, prefsaver.UIType.MShelfTabLayout, 1),
            (self.uiSHLTAB_test2, prefsaver.UIType.MShelfTabLayout, 1),
            (self.uiTAB_test1, prefsaver.UIType.MTabLayout, 1),
            (self.uiTAB_test2, prefsaver.UIType.MTabLayout, 1),
            (self.uiTXT_test1, prefsaver.UIType.MTextField, 'default text'),
            (self.uiTXT_test2, prefsaver.UIType.MTextField, 'default text'),
            (self.uiTXBTGR_test1, prefsaver.UIType.MTextFieldButtonGrp, 'default text'),
            (self.uiTXBTGR_test2, prefsaver.UIType.MTextFieldButtonGrp, 'default text'),
            (self.uiTXTGRP_test1, prefsaver.UIType.MTextFieldGrp, 'default text'),
            (self.uiTXTGRP_test2, prefsaver.UIType.MTextFieldGrp, 'default text'),
            (self.uiTXTLST_test1, prefsaver.UIType.MTextScrollList, []),
            (self.uiTXTLST_test2, prefsaver.UIType.MTextScrollList, [])
        ]

        for control, cType, default in controlList:
            if defaults:
                self.prefSaver.addControl(control, cType, default)
            else:
                self.prefSaver.addControl(control, cType)

    # noinspection PyUnusedLocal
    def onSavePrefsClicked(self, *args):
        self.prefSaver.savePrefs()

    # noinspection PyUnusedLocal
    def onLoadPrefsClicked(self, *args):
        self.prefSaver.loadPrefs()

    # noinspection PyUnusedLocal
    def onResetPrefsClicked(self, *args):
        self.prefSaver.resetPrefs()

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    def onCloseClicked(self, *args):
        if m.window(WIN_NAME, exists=True):
            m.deleteUI(WIN_NAME, window=True)


def run(serializer):
    WinMayaUI(serializer)
