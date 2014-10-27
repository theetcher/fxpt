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
                                with pm.rowLayout(numberOfColumns=2):
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