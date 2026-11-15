import maya.cmds as m

SCRIPT_NAME = 'FX Create Box'
WIN_NAME = 'fx_createBBoxWin'

MAIN_BUTTONS_HEIGHT = 30

BBOX_NAME = 'bbox'

ui = None

faceMapping = {
    'xPos': '.f[4]',
    'xNeg': '.f[5]',
    'yPos': '.f[1]',
    'yNeg': '.f[3]',
    'zPos': '.f[0]',
    'zNeg': '.f[2]',
}

FIELDS = (
    ('xPos', '+X', 1),
    ('xNeg', '-X', -1),
    ('yPos', '+Y', 1),
    ('yNeg', '-Y', -1),
    ('zPos', '+Z', 1),
    ('zNeg', '-Z', -1),
)


# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic
class CreateBBoxUI(object):
    def __init__(self):
        self.fields = {}
        self.uiCreate()

    def uiCreate(self):

        self.uiClose()

        self.window = m.window(
            WIN_NAME,
            title=SCRIPT_NAME,
            maximizeButton=False
        )

        m.setUITemplate('DefaultTemplate', pushTemplate=True)

        self.ui_LAY_mainForm = m.formLayout()

        self.ui_TAB_top = m.tabLayout(tabsVisible=False)
        m.tabLayout(self.ui_TAB_top, e=True, height=1)

        self.ui_LAY_attachForm = m.formLayout()

        self.ui_TAB_inner = m.tabLayout(tabsVisible=False, scrollable=True, innerMarginWidth=4)

        self.ui_LAY_mainColumn = m.columnLayout(adjustableColumn=True)

        m.frameLayout(
            label='Parameters',
            collapsable=True,
            collapse=False,
            marginHeight=3
        )
        m.columnLayout(adjustableColumn=True, columnOffset=('both', 2))
        for key, label, default in FIELDS:
            self.fields[key] = m.floatFieldGrp(numberOfFields=1, label=label, precision=6, value1=default)
        m.setParent('..')  # columnLayout
        m.setParent('..')  # frameLayout

        m.setParent('..')  # ui_LAY_mainColumn
        m.setParent('..')  # ui_TAB_inner
        m.setParent('..')  # ui_LAY_attachForm
        m.setParent('..')  # ui_TAB_top

        self.ui_BTN_create = m.button(
            label='Create',
            height=MAIN_BUTTONS_HEIGHT,
            command=self.ui_on_BTN_create_clicked
        )

        self.ui_BTN_close = m.button(
            label='Close',
            height=MAIN_BUTTONS_HEIGHT,
            command=self.uiClose
        )

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
                (self.ui_BTN_create, 'left', 5),
                (self.ui_BTN_create, 'bottom', 5),
                (self.ui_BTN_close, 'right', 5),
                (self.ui_BTN_close, 'bottom', 5),
            ],
            attachControl=[
                (self.ui_TAB_top, 'bottom', 5, self.ui_BTN_close),
            ],
            attachPosition=[
                (self.ui_BTN_create, 'right', 2, 50),
                (self.ui_BTN_close, 'left', 2, 50),
            ],
            attachNone=[
                (self.ui_BTN_create, 'top'),
                (self.ui_BTN_close, 'top'),
            ]
        )

        m.showWindow(self.window)

    def getFieldValue(self, key):
        return m.floatFieldGrp(self.fields[key], q=True, value1=True)

    # noinspection PyUnusedLocal
    def ui_on_BTN_create_clicked(self, *args):
        xPosUI = self.getFieldValue('xPos')
        xNegUI = self.getFieldValue('xNeg')
        yPosUI = self.getFieldValue('yPos')
        yNegUI = self.getFieldValue('yNeg')
        zPosUI = self.getFieldValue('zPos')
        zNegUI = self.getFieldValue('zNeg')

        xPos = max(xPosUI, xNegUI)
        xNeg = min(xPosUI, xNegUI)
        yPos = max(yPosUI, yNegUI)
        yNeg = min(yPosUI, yNegUI)
        zPos = max(zPosUI, zNegUI)
        zNeg = min(zPosUI, zNegUI)

        m.undoInfo(openChunk=True, chunkName='fxCreateAABB')
        try:
            cube = m.polyCube(ch=False)[0]

            m.move(xPos, cube + faceMapping['xPos'], worldSpaceDistance=True, x=True)
            m.move(xNeg, cube + faceMapping['xNeg'], worldSpaceDistance=True, x=True)
            m.move(yPos, cube + faceMapping['yPos'], worldSpaceDistance=True, y=True)
            m.move(yNeg, cube + faceMapping['yNeg'], worldSpaceDistance=True, y=True)
            m.move(zPos, cube + faceMapping['zPos'], worldSpaceDistance=True, z=True)
            m.move(zNeg, cube + faceMapping['zNeg'], worldSpaceDistance=True, z=True)

            m.xform(cube, cp=True)
            m.rename(cube, BBOX_NAME)
        finally:
            m.undoInfo(closeChunk=True)

    # noinspection PyUnusedLocal
    def uiClose(self, *args):
        if m.window(WIN_NAME, exists=True):
            m.deleteUI(WIN_NAME, window=True)


def run():
    global ui
    ui = CreateBBoxUI()
