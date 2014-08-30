import maya.cmds as m
import pymel.core as pm


SCRIPT_NAME = 'FX Reorient'
WIN_NAME = 'fx_reorientWin'

BUTTON_WIDTH = 150
MAIN_BUTTONS_HEIGHT = 30

LOCATOR_FLY_AWAY_DISTANCE = 100

win = None

from fx_utils.watch import *


#noinspection PyAttributeOutsideInit
#noinspection PyMethodMayBeStatic
#noinspection PyUnusedLocal
class ReorientUI(object):
    def __init__(self):
        self.oriData = OriData()
        self.processor = OrientProcessor()
        self.ui_create()
        self.ui_refresh()

    def ui_create(self):

        self.ui_close()

        self.window = pm.window(
            WIN_NAME,
            title=SCRIPT_NAME,
            maximizeButton=False
        )

        with self.window:
            with pm.formLayout() as ui_LAY_mainForm:
                with pm.scrollLayout(childResizable=True) as ui_LAY_mainScroll:
                    with pm.columnLayout(adjustableColumn=True):
                        with self.ui_createFrame('Manual Orient', collapsed=True):
                            with pm.columnLayout(adjustableColumn=True, columnOffset=('both', 2)):
                                pm.separator(style='none', height=5)

                                pm.button(
                                    label='Create Tripod',
                                    height=MAIN_BUTTONS_HEIGHT,
                                    command=self.ui_onBtnCreateTripod
                                )

                                pm.separator(style='none', height=5)

                        with self.ui_createFrame('Automatic Orient'):
                            with pm.columnLayout(adjustableColumn=True, columnOffset=('both', 2)):
                                with self.ui_createButtonTextFieldRowLayout():
                                    pm.button(
                                        label='Set Object',
                                        command=pm.Callback(self.ui_onBtnSetCompClicked, OriData.OriObject)
                                    )
                                    self.ui_TXTFLD_objectName = pm.textField(editable=False)

                                with self.ui_createButtonTextFieldRowLayout():
                                    pm.button(
                                        label='Set Pivot',
                                        command=pm.Callback(self.ui_onBtnSetCompClicked, OriData.OriPivot)
                                    )
                                    self.ui_TXTFLD_pivotVtx = pm.textField(editable=False)

                                with self.ui_createButtonTextFieldRowLayout():
                                    pm.button(
                                        label='Set Aim',
                                        command=pm.Callback(self.ui_onBtnSetCompClicked, OriData.OriAim)
                                    )
                                    self.ui_TXTFLD_aimVtx = pm.textField(editable=False)

                                with self.ui_createButtonTextFieldRowLayout():
                                    pm.button(
                                        label='Set Up',
                                        command=pm.Callback(self.ui_onBtnSetCompClicked, OriData.OriUp)
                                    )
                                    self.ui_TXTFLD_upVtx = pm.textField(editable=False)

                                pm.separator(style='none', height=5)

                                with pm.formLayout() as ui_LAY_btnForm:
                                    ui_BTN_reset = pm.button(
                                        label='Reset',
                                        height=MAIN_BUTTONS_HEIGHT,
                                        command=self.ui_onBtnResetClicked
                                    )

                                    self.ui_BTN_fixOrient = pm.button(
                                        label='Fix Orientation',
                                        height=MAIN_BUTTONS_HEIGHT,
                                        command=self.ui_onBtnFixOrient
                                    )

                                    ui_LAY_btnForm.attachNone(ui_BTN_reset, 'top')
                                    ui_LAY_btnForm.attachForm(ui_BTN_reset, 'left', 2)
                                    ui_LAY_btnForm.attachPosition(ui_BTN_reset, 'right', 2, 50)
                                    ui_LAY_btnForm.attachForm(ui_BTN_reset, 'bottom', 2)

                                    ui_LAY_btnForm.attachNone(self.ui_BTN_fixOrient, 'top')
                                    ui_LAY_btnForm.attachPosition(self.ui_BTN_fixOrient, 'left', 2, 50)
                                    ui_LAY_btnForm.attachForm(self.ui_BTN_fixOrient, 'right', 2)
                                    ui_LAY_btnForm.attachForm(self.ui_BTN_fixOrient, 'bottom', 2)

                self.ui_btn_close = pm.button(
                    label='Close',
                    height=MAIN_BUTTONS_HEIGHT,
                    command=self.ui_close
                )

                ui_LAY_mainForm.attachForm(ui_LAY_mainScroll, 'top', 2)
                ui_LAY_mainForm.attachForm(ui_LAY_mainScroll, 'left', 2)
                ui_LAY_mainForm.attachForm(ui_LAY_mainScroll, 'right', 2)
                ui_LAY_mainForm.attachControl(ui_LAY_mainScroll, 'bottom', 2, self.ui_btn_close)

                ui_LAY_mainForm.attachNone(self.ui_btn_close, 'top')
                ui_LAY_mainForm.attachForm(self.ui_btn_close, 'left', 2)
                ui_LAY_mainForm.attachForm(self.ui_btn_close, 'right', 2)
                ui_LAY_mainForm.attachForm(self.ui_btn_close, 'bottom', 2)

    def ui_createButtonTextFieldRowLayout(self):
        return pm.rowLayout(
            numberOfColumns=2,
            adjustableColumn=2,
            columnWidth=(1, BUTTON_WIDTH),
            columnAttach=(1, 'both', 2)
        )

    def ui_createFrame(self, name, collapsed=False):
        return pm.frameLayout(
            label=name,
            collapsable=True,
            marginHeight=3,
            borderStyle='etchedIn',
            borderVisible=True,
            collapse=collapsed
        )

    def ui_refresh(self):
        oriDataObject, oriDataPivotVtx, oriDataAimVtx, oriDataUpVtx = self.oriData.getOriDataStrings()
        self.ui_TXTFLD_objectName.setText(oriDataObject)
        self.ui_TXTFLD_pivotVtx.setText(oriDataPivotVtx)
        self.ui_TXTFLD_aimVtx.setText(oriDataAimVtx)
        self.ui_TXTFLD_upVtx.setText(oriDataUpVtx)

        self.ui_BTN_fixOrient.setEnable(self.oriData.isSetupReady())

    def ui_onBtnSetCompClicked(self, comp):
        if self.oriData.setupOriDataComponent(comp):
            self.ui_refresh()
        else:
            if comp == OriData.OriObject:
                simpleWarning('Select one transform.')
            else:
                simpleWarning('Select one transform or polygon vertex.')

    def ui_onBtnResetClicked(self, *args):
        self.oriData.initData()
        self.ui_refresh()

    def ui_onBtnFixOrient(self, *args):
        self.processor.fixOrient(self.oriData)

    def ui_onBtnCreateTripod(self, *args):
        self.processor.createTripod()

    def ui_close(self, *args):
        if pm.window(WIN_NAME, exists=True):
            pm.deleteUI(WIN_NAME, window=True)


# noinspection PyMethodMayBeStatic,PyAttributeOutsideInit
class OriData(object):

    OriObject = 0
    OriPivot = 1
    OriAim = 2
    OriUp = 3

    def __init__(self):
        self.initData()

    def initData(self):
        self.oriData = {
            OriData.OriObject: None,
            OriData.OriPivot: None,
            OriData.OriAim: None,
            OriData.OriUp: None
        }
        self.setupOriDataComponent(OriData.OriObject)
        self.setupOriDataComponent(OriData.OriPivot)

    def getOriDataStrings(self):
        return (
            str(self.oriData[OriData.OriObject]),
            str(self.oriData[OriData.OriPivot]),
            str(self.oriData[OriData.OriAim]),
            str(self.oriData[OriData.OriUp])
        )

    def setOriData(self, comp, objName):
        self.oriData[comp] = objName

    def getOriData(self, comp):
        return self.oriData[comp]

    def setupOriDataComponent(self, comp):
        forceTransform = True if comp == OriData.OriObject else False
        res = self.getWorkingObjectFromSelection(forceTransform=forceTransform)
        if res:
            self.setOriData(comp, res)
            return True
        else:
            return False

    def getWorkingObjectFromSelection(self, forceTransform=False):

        selection = m.ls(selection=True, long=True, flatten=True)

        if len(selection) != 1:
            return None

        selection = selection[0]
        componentSelected = '.' in selection
        node = selection.split('.')[0]

        if componentSelected and self.isMeshTransform(node):
            if forceTransform:
                return node
            else:
                return selection

        if m.nodeType(node) == 'transform':
            return node
        else:
            return None

    def isMeshTransform(self, node):
        for child in m.listRelatives(node, fullPath=True, children=True):
            if m.nodeType(child) == 'mesh':
                return True
        return False

    def isSetupReady(self):
        return any([oriCompName is not None for oriCompName in self.oriData.values()])


#noinspection PyAttributeOutsideInit
#noinspection PyMethodMayBeStatic
class OrientProcessor(object):

    def __init__(self):
        pass

    def fixOrient(self, oriData):
        # selectedObjects = m.ls(sl=True, l=True, fl=True)

        triPivot, triAim, triUp, aimConstraint = self.createTripod()

        x, y, z = self.getWorldSpaceCoords(oriData.getOriData(OriData.OriPivot))
        m.move(x, y, z, triPivot, absolute=True)
        x, y, z = self.getWorldSpaceCoords(oriData.getOriData(OriData.OriAim))
        m.move(x, y, z, triAim, absolute=True)
        x, y, z = self.getWorldSpaceCoords(oriData.getOriData(OriData.OriUp))
        m.move(x, y, z, triUp, absolute=True)

        origParent = m.listRelatives(oriData.getOriData(OriData.OriObject), parent=True, fullPath=True)
        origParent = origParent[0] if origParent else None

        newPath = m.parent(oriData.getOriData(OriData.OriObject), triPivot)[0]

        try:
            m.makeIdentity(newPath, apply=True, rotate=True)
        except RuntimeError as e:
            simpleWarning('Reorient failed.\n' + str(e), icon='critical')
        finally:
            if origParent:
                m.parent(newPath, origParent)
            else:
                m.parent(newPath, world=True)

        m.delete((aimConstraint, triPivot, triAim, triUp))

        m.select(oriData.getOriData(OriData.OriObject))
        # if selectedObjects:
        #     m.select(selectedObjects)
        # else:
        #     m.select(cl=True)

    def createTripod(self):
        triPivot = m.spaceLocator(name='triPivot')[0]
        triAim = m.spaceLocator(name='triAim')[0]
        m.move(0, 0, 1, triAim, absolute=True)
        triUp = m.spaceLocator(name='triUp')[0]
        m.move(0, 1, 0, triUp, absolute=True)

        constraint = m.aimConstraint(
            triAim,
            triPivot,
            worldUpType='object',
            worldUpObject=triUp
        )[0]

        return triPivot, triAim, triUp, constraint

    def getWorldSpaceCoords(self, oriObj):
        if '.' in oriObj:
            return m.pointPosition(oriObj, world=True)
        else:
            return m.xform(oriObj, q=True, rp=True, ws=True)


def run():
    global win
    win = ReorientUI()


#----------------------------------------------------------------------------------------------------------------------
# Helper Functions
#----------------------------------------------------------------------------------------------------------------------

def simpleWarning(message, icon='information'):
    pm.confirmDialog(
        icon=icon,
        title=SCRIPT_NAME,
        message=message,
        button=['Ok']
    )