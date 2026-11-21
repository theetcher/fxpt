from functools import partial

import maya.cmds as m

SCRIPT_NAME = 'FX Reorient'
WIN_NAME = 'fx_reorientWin'

BUTTON_WIDTH = 150
MAIN_BUTTONS_HEIGHT = 30

LOCATOR_FLY_AWAY_DISTANCE = 100

win = None


# noinspection PyAttributeOutsideInit
# noinspection PyMethodMayBeStatic
# noinspection PyUnusedLocal
class ReorientUI(object):
    def __init__(self):
        self.oriData = OriData()
        self.processor = OrientProcessor()
        self.ui_create()
        self.ui_refresh()

    def ui_create(self):

        self.ui_close()

        self.window = m.window(
            WIN_NAME,
            title=SCRIPT_NAME,
            maximizeButton=False
        )

        m.setUITemplate('DefaultTemplate', pushTemplate=True)
        try:
            self.ui_LAY_mainForm = m.formLayout()

            self.ui_TAB_top = m.tabLayout(tabsVisible=False)
            m.tabLayout(self.ui_TAB_top, e=True, height=1)

            self.ui_LAY_attachForm = m.formLayout()

            self.ui_TAB_inner = m.tabLayout(tabsVisible=False, scrollable=True, innerMarginWidth=4)

            self.ui_LAY_mainColumn = m.columnLayout(adjustableColumn=True)

            # Manual Orient
            self.ui_createFrame('Manual Orient', collapsed=True)
            m.columnLayout(adjustableColumn=True, columnOffset=('both', 2))
            m.button(
                label='Create Tripod',
                height=MAIN_BUTTONS_HEIGHT,
                command=self.ui_onBtnCreateTripod
            )
            m.setParent('..')  # columnLayout
            m.setParent('..')  # frameLayout

            # Automatic Orient
            self.ui_createFrame('Automatic Orient')
            m.columnLayout(adjustableColumn=True, columnOffset=('both', 2))

            self.ui_TXTFLD_objectName = self.ui_createButtonTextFieldRow('Set Object', OriData.OriObject)
            self.ui_TXTFLD_pivotVtx = self.ui_createButtonTextFieldRow('Set Pivot', OriData.OriPivot)
            self.ui_TXTFLD_aimVtx = self.ui_createButtonTextFieldRow('Set Aim', OriData.OriAim)
            self.ui_TXTFLD_upVtx = self.ui_createButtonTextFieldRow('Set Up', OriData.OriUp)

            ui_LAY_btnForm = m.formLayout()
            ui_BTN_reset = m.button(
                label='Reset',
                height=MAIN_BUTTONS_HEIGHT,
                command=self.ui_onBtnResetClicked
            )
            self.ui_BTN_fixOrient = m.button(
                label='Fix Orientation',
                height=MAIN_BUTTONS_HEIGHT,
                command=self.ui_onBtnFixOrient
            )
            m.formLayout(
                ui_LAY_btnForm,
                e=True,
                attachForm=[
                    (ui_BTN_reset, 'top', 5),
                    (ui_BTN_reset, 'left', 2),
                    (ui_BTN_reset, 'bottom', 2),
                    (self.ui_BTN_fixOrient, 'top', 5),
                    (self.ui_BTN_fixOrient, 'right', 2),
                    (self.ui_BTN_fixOrient, 'bottom', 2),
                ],
                attachPosition=[
                    (ui_BTN_reset, 'right', 2, 50),
                    (self.ui_BTN_fixOrient, 'left', 2, 50),
                ]
            )

            m.setParent(self.ui_LAY_mainForm)

            self.ui_btn_close = m.button(
                label='Close',
                height=MAIN_BUTTONS_HEIGHT,
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
                (self.ui_btn_close, 'left', 5),
                (self.ui_btn_close, 'bottom', 5),
                (self.ui_btn_close, 'right', 5),
            ],
            attachControl=[
                (self.ui_TAB_top, 'bottom', 5, self.ui_btn_close),
            ],
            attachNone=[
                (self.ui_btn_close, 'top'),
            ]
        )

        m.showWindow(self.window)

    def ui_createButtonTextFieldRow(self, label, comp):
        m.rowLayout(
            numberOfColumns=2,
            adjustableColumn=2,
            columnWidth=(1, BUTTON_WIDTH),
            columnAttach=(1, 'both', 2)
        )
        m.button(
            label=label,
            command=partial(self.ui_onBtnSetCompClicked, comp)
        )
        textField = m.textField(editable=False)
        m.setParent('..')
        return textField

    def ui_createFrame(self, name, collapsed=False):
        return m.frameLayout(
            label=name,
            collapsable=True,
            collapse=collapsed,
            marginHeight=3
        )

    def ui_refresh(self):
        oriDataObject, oriDataPivotVtx, oriDataAimVtx, oriDataUpVtx = self.oriData.getOriDataStrings()
        m.textField(self.ui_TXTFLD_objectName, e=True, text=oriDataObject)
        m.textField(self.ui_TXTFLD_pivotVtx, e=True, text=oriDataPivotVtx)
        m.textField(self.ui_TXTFLD_aimVtx, e=True, text=oriDataAimVtx)
        m.textField(self.ui_TXTFLD_upVtx, e=True, text=oriDataUpVtx)

        m.button(self.ui_BTN_fixOrient, e=True, enable=self.oriData.isSetupReady())

    def ui_onBtnSetCompClicked(self, comp, *args):
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
        if m.window(WIN_NAME, exists=True):
            m.deleteUI(WIN_NAME, window=True)


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
        return tuple(
            self.oriData[comp] or ''
            for comp in (OriData.OriObject, OriData.OriPivot, OriData.OriAim, OriData.OriUp)
        )

    def setOriData(self, comp, objName):
        self.oriData[comp] = objName

    def getOriData(self, comp):
        return self.oriData[comp]

    def setupOriDataComponent(self, comp):
        forceTransform = comp == OriData.OriObject
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
            elif '.vtx[' in selection:
                return selection
            else:
                return None

        if m.nodeType(node) == 'transform':
            return node
        else:
            return None

    def isMeshTransform(self, node):
        if m.nodeType(node) != 'transform':
            return False
        for child in m.listRelatives(node, fullPath=True, children=True) or []:
            if m.nodeType(child) == 'mesh':
                return True
        return False

    def isSetupReady(self):
        return all(oriCompName is not None for oriCompName in self.oriData.values())

    def getMissing(self):
        return [name for name in self.oriData.values() if not m.objExists(name)]


# noinspection PyAttributeOutsideInit
# noinspection PyMethodMayBeStatic
class OrientProcessor(object):
    def __init__(self):
        pass

    def fixOrient(self, oriData):
        if not oriData.isSetupReady():
            simpleWarning('Set the object, pivot, aim and up first.')
            return

        missing = oriData.getMissing()
        if missing:
            simpleWarning('These no longer exist:\n' + '\n'.join(missing))
            return

        oriObject = oriData.getOriData(OriData.OriObject)

        m.undoInfo(openChunk=True, chunkName=SCRIPT_NAME)
        try:
            # read positions before the object moves in the hierarchy
            pivotPos = self.getWorldSpaceCoords(oriData.getOriData(OriData.OriPivot))
            aimPos = self.getWorldSpaceCoords(oriData.getOriData(OriData.OriAim))
            upPos = self.getWorldSpaceCoords(oriData.getOriData(OriData.OriUp))

            triPivot, triAim, triUp, aimConstraint = self.createTripod()

            m.move(pivotPos[0], pivotPos[1], pivotPos[2], triPivot, absolute=True)
            m.move(aimPos[0], aimPos[1], aimPos[2], triAim, absolute=True)
            m.move(upPos[0], upPos[1], upPos[2], triUp, absolute=True)

            origParent = m.listRelatives(oriObject, parent=True, fullPath=True)
            origParent = origParent[0] if origParent else None

            newPath = m.parent(oriObject, triPivot)[0]

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

            m.select(oriObject)
        finally:
            m.undoInfo(closeChunk=True)

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


# ----------------------------------------------------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------------------------------------------------

def simpleWarning(message, icon='information'):
    m.confirmDialog(
        icon=icon,
        title=SCRIPT_NAME,
        message=message,
        button=['Ok']
    )
