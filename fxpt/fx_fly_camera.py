import time

from PySide import QtCore
from PySide import QtGui
import shiboken

import maya.cmds as m
import maya.OpenMayaUI as omui
import pymel.core as pm

#from watch import *

flyer = None

OPT_VAR_PREFIX = 'fx_flyCamera_'

MOUSE_ORIGIN_X = 500
MOUSE_ORIGIN_Y = 500

MOUSE_HOR = 1
MOUSE_VER = 2

SPD_MOVE_X = 1  # x -> right, -x -> left
SPD_MOVE_Y = 2  # y -> up, -y -> down
SPD_MOVE_Z = 3  # z -> backward, -z -> forward
SPD_ROTATE_X = 4  # x -> up, -x -> down
SPD_ROTATE_Y = 5  # y -> left, -y -> right

Y_UP = True if m.upAxis(q=True, ax=True) == 'y' else False


# noinspection PyCallByClass,PyTypeChecker
def moveCursorToOrigin():
    QtGui.QCursor.setPos(MOUSE_ORIGIN_X, MOUSE_ORIGIN_Y)


def sign(x):
    return (x > 0) - (x < 0)


class Timer(object):
    def __init__(self):
        self.prevTime = 0
        self.start()

    def start(self):
        self.prevTime = time.clock()

    def delta(self):
        pTime = self.prevTime
        self.prevTime = time.clock()
        return self.prevTime - pTime


class EventCatcher(QtCore.QObject):
    def __init__(self):
        super(EventCatcher, self).__init__()

    def eventFilter(self, obj, event):

        eventType = event.type()

        if eventType == QtCore.QEvent.KeyPress:
            flyer.setControlState(event.key(), True)
            flyer.execAction(event.key())
            return True

        elif eventType == QtCore.QEvent.KeyRelease:
            flyer.setControlState(event.key(), False)
            return True

        elif eventType == QtCore.QEvent.WindowDeactivate:
            flyer.setControlState(QtCore.Qt.Key_Escape, True)
            return True

        return False


class InfoWidget(QtGui.QFrame):

    def __init__(self, parent):
        super(InfoWidget, self).__init__(parent=parent)
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.label = QtGui.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        self.label.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.label)
        self.setWindowFlags(QtCore.Qt.Popup)
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)

    def setText(self, text):
        self.label.setText(text)


# noinspection PyAttributeOutsideInit
class FlyCamUI(QtGui.QPushButton):

    def __init__(self):
        ptr = omui.MQtUtil.mainWindow()
        if ptr is not None:
            self.mainWinQObject = shiboken.wrapInstance(long(ptr), QtGui.QWidget)  # or you can use QMainWindow
        else:
            m.error('cannot find main Maya window.')
        super(FlyCamUI, self).__init__(parent=self.mainWinQObject)

        self.createUI()
        self.createHelpWidget()
        self.createDebugInfoWidget()

    def createUI(self):
        self.setText('Fly Camera. Press "h" for help')
        self.setCheckable(True)
        self.setChecked(True)

        self.mainBtnWidth = 250
        self.mainBtnHeight = 30
        self.mainBtnLeft = 0
        self.mainBtnTop = self.mainWinQObject.geometry().height() - self.mainBtnHeight
        self.resize(self.mainBtnWidth, self.mainBtnHeight)
        self.move(self.mainBtnLeft, self.mainBtnTop)

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.setFont(font)

        # self.setStyleSheet('QPushButton:checked {color: #000000; background-color: #ffae00}')

        self.show()
        self.raise_()

    def createHelpWidget(self):
        self.helpWindow = InfoWidget(self)
        self.helpVisible = False
        text = ''
        text += '<b>"h"</b> - toggle this help<br>'
        text += '<br>'
        text += '<b>"w"</b> - move forward<br>'
        text += '<b>"s"</b> - move backward<br>'
        text += '<b>"a"</b> - move left<br>'
        text += '<b>"d"</b> - move right<br>'
        text += '<b>Right Mouse Button</b> - move up<br>'
        text += '<b>Left Mouse Button</b> - move down<br>'
        text += '<b>Shift</b> - move slowly while pressed<br>'
        text += '<b>Control</b> - move faster while pressed<br>'
        text += '<br>'
        text += '<b>"-"</b> - decrease speed<br>'
        text += '<b>"="</b> - increase speed<br>'
        text += '<b>"9"</b> - decrease mouse sensivity<br>'
        text += '<b>"0"</b> - increase mouse sensivity<br>'
        text += '<b>"i"</b> - invert mouse<br>'
        text += '<b>"o"</b> - swap mouse buttons<br>'
        text += '<br>'
        text += '<b>"Home"</b> - reset settings'
        text += '</font>'
        self.helpWindow.setText(text)

        winHeight = 280
        mainBtnTopLeftGlobal = self.mapToGlobal(QtCore.QPoint(0, 0))
        self.helpWindow.move(mainBtnTopLeftGlobal.x(), mainBtnTopLeftGlobal.y() - winHeight - 2)
        self.helpWindow.resize(self.mainBtnWidth, winHeight)

    def toggleHelp(self):
        if self.helpVisible:
            self.helpWindow.hide()
            self.helpVisible = False
        else:
            self.helpWindow.show()
            self.helpWindow.raise_()
            self.helpWindow.repaint()
            self.helpVisible = True

    def createDebugInfoWidget(self):
        self.debugInfoWindow = InfoWidget(self)
        self.debugInfoVisible = False

        winHeight = 250
        winWidth = 200
        mainBtnTopLeftGlobal = self.mapToGlobal(QtCore.QPoint(0, 0))
        self.debugInfoWindow.move(mainBtnTopLeftGlobal.x() + self.mainBtnWidth + 2, mainBtnTopLeftGlobal.y() + self.mainBtnHeight - winHeight)
        self.debugInfoWindow.resize(winWidth, winHeight)

    def toggleDebugInfo(self):
        if self.debugInfoVisible:
            self.debugInfoWindow.hide()
            self.debugInfoVisible = False
        else:
            self.debugInfoWindow.show()
            self.debugInfoWindow.raise_()
            self.debugInfoWindow.repaint()
            self.debugInfoVisible = True

    def startEventsCapture(self):
        moveCursorToOrigin()

        self.setMouseTracking(True)
        self.grabKeyboard()
        self.grabMouse(QtCore.Qt.BlankCursor)

        self.eventCatcher = EventCatcher()
        self.installEventFilter(self.eventCatcher)

    def stopEventsCapture(self):
        self.removeEventFilter(self.eventCatcher)
        del self.eventCatcher

        self.releaseKeyboard()
        self.setMouseTracking(False)
        self.releaseMouse()

    def updateDebugInfo(self):
        txt = ''
        for key, state in sorted(flyer.controls.items()):
            txt += str(key) + ' = ' + str(state) + '\n'
        for key, state in sorted(flyer.speeds.items()):
            txt += str(key) + ' = ' + str(state) + '\n'
        txt += 'delta = ' + str(flyer.delta) + '\n'
        self.debugInfoWindow.setText(txt)

    def raiseWindows(self):
        if self.helpVisible:
            self.helpWindow.show()
        if self.debugInfoVisible:
            self.debugInfoWindow.show()

    def closeEvent(self, event):
        if self.helpVisible:
            self.toggleHelp()
        if self.debugInfoVisible:
            self.toggleDebugInfo()
        event.accept()


# noinspection PyAttributeOutsideInit,PyMethodMayBeStatic
class Flyer(object):

    def __init__(self):

        self.camera, self.cameraShape = self.getCamera()
        if not self.camera:
            return

        self.m3dView = omui.M3dView.active3dView()

        self.timer = None
        self.delta = 0

        self.maxSpeed = None
        self.rotateSpeed = None
        self.invertMouse = None
        self.swapMouseButtons = None
        self.useGameView = None

        self.setupOptionVars()

        self.stopThreshold = 0.01
        self.shiftSpeedMultiplier = 0.2
        self.controlSpeedMultiplier = 5
        self.accelerationTime = 0.2

        self.acceleration = None
        self.maxSpeedModified = None

        self.controls = {
            QtCore.Qt.Key_Escape: False,
            QtCore.Qt.Key_W: False,
            QtCore.Qt.Key_S: False,
            QtCore.Qt.Key_A: False,
            QtCore.Qt.Key_D: False,
            QtCore.Qt.LeftButton: False,
            QtCore.Qt.RightButton: False,
            QtCore.Qt.Key_Shift: False,
            QtCore.Qt.Key_Control: False
        }

        self.mouseData = {
            MOUSE_HOR: 0,
            MOUSE_VER: 0
        }

        self.actions = {
            QtCore.Qt.Key_H: self.onShowHelp,  # help
            QtCore.Qt.Key_Minus: lambda: self.onChangeSpeed(False),  # speed-
            QtCore.Qt.Key_Equal: lambda: self.onChangeSpeed(True),  # speed+
            QtCore.Qt.Key_9: lambda: self.onChangeRotationSpeed(False),  # rotation speed-
            QtCore.Qt.Key_0: lambda: self.onChangeRotationSpeed(True),  # rotation speed+
            QtCore.Qt.Key_I: self.onInvertMouse,  # invert mouse
            QtCore.Qt.Key_O: self.onSwapMouseButtons,  # swap mouse buttons
            QtCore.Qt.Key_G: self.onGameViewToggle,  # swap mouse buttons
            QtCore.Qt.Key_QuoteLeft: self.onShowDebug,
            QtCore.Qt.Key_Home: self.settingsReset
        }

        self.speeds = {
            SPD_MOVE_X: 0.0,  # x -> right, -x -> left
            SPD_MOVE_Y: 0.0,  # y -> up, -y -> down
            SPD_MOVE_Z: 0.0,  # z -> backward, -z -> forward
            SPD_ROTATE_X: 0.0,  # x -> up, -x -> down
            SPD_ROTATE_Y: 0.0  # y -> left, -y -> right
        }

        if self.useGameView:
            self.modifyCameraToGameView()

        self.ui = FlyCamUI()

    def getCamera(self):
        panelWithFocus = m.getPanel(withFocus=True)
        panelType = m.getPanel(typeOf=panelWithFocus)
        if panelType != 'modelPanel':
            self.showError('Cannot find camera.' + (' ' * 100),
                           'Select perspective viewport with camera without animation or locked channels.')
            return None, None
        else:
            camera = m.modelPanel(panelWithFocus, q=True, camera=True)
            cameraShape = m.listRelatives(camera, shapes=True, fullPath=True)

            if m.getAttr(cameraShape[0] + '.orthographic'):
                self.showError('Cannot use orthographic camera.' + (' ' * 100),
                               'Select perspective viewport with camera without animation or locked channels.')
                return None, None

            attrsToCheck = ('.tx', '.ty', '.tz', '.rx', '.ry', '.rz')
            for attr in attrsToCheck:
                if m.getAttr(camera + attr, lock=True) or m.listConnections(camera + attr, s=True, d=False):
                    self.showError('Cannot use this camera.' + (' ' * 50), 'This camera is locked or animated.')
                    return None, None

        return camera, cameraShape[0]

    def modifyCameraToGameView(self):
        print 'modifyCameraToGameView()'

        self.savedCameraSettings = {}
        attributes = {
            self.cameraShape + '.focalLength': 40,
            self.cameraShape + '.displayResolution': 1,
            self.cameraShape + '.overscan': 1.3,
            self.cameraShape + '.filmFit': 3,
            self.cameraShape + '.horizontalFilmAperture': 1.417,
            self.cameraShape + '.verticalFilmAperture': 0.945,
            self.cameraShape + '.lensSqueezeRatio': 1,
            'defaultResolution.lockDeviceAspectRatio': 0,
            'defaultResolution.aspectLock': 0,
            'defaultResolution.width': 1280,
            'defaultResolution.height': 720,
            'defaultResolution.deviceAspectRatio': 1.778
        }

        for attr in attributes:
            self.savedCameraSettings[attr] = m.getAttr(attr)
            m.setAttr(attr, attributes[attr])

    def restoreCamera(self):
        for attr in self.savedCameraSettings:
            m.setAttr(attr, self.savedCameraSettings[attr])

    def showError(self, txt, itxt):
        msgBox = QtGui.QMessageBox()
        msgBox.setWindowTitle('Error')
        msgBox.setText(txt)
        msgBox.setInformativeText(itxt)
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
        msgBox.setIcon(QtGui.QMessageBox.Critical)
        msgBox.exec_()

    def fly(self):

        if not self.camera:
            return

        undoState = m.undoInfo(q=True, state=True)
        m.undoInfo(state=False)

        try:

            self.ui.startEventsCapture()
            self.timer = Timer()
            while not self.getControlState(QtCore.Qt.Key_Escape):
                QtGui.qApp.processEvents()
                self.getMouseData()
                self.delta = self.timer.delta()
                self.calculateSpeeds()
                self.transformCamera()
                self.m3dView.refresh(True, True)
                self.ui.updateDebugInfo()
                self.raiseWindows()

        finally:

            self.ui.stopEventsCapture()
            self.ui.close()

            m.undoInfo(state=undoState)

            if self.useGameView:
                self.restoreCamera()

            self.settingsSave()

            global flyer
            flyer = None

    def getMouseData(self):
        pos = QtGui.QCursor.pos()
        self.mouseData[MOUSE_HOR] = pos.x() - MOUSE_ORIGIN_X
        self.mouseData[MOUSE_VER] = pos.y() - MOUSE_ORIGIN_Y
        moveCursorToOrigin()

        pressedButtons = QtGui.qApp.mouseButtons()
        if pressedButtons & QtCore.Qt.LeftButton:
            self.setControlState(QtCore.Qt.LeftButton, True)
        else:
            self.setControlState(QtCore.Qt.LeftButton, False)

        if pressedButtons & QtCore.Qt.RightButton:
            self.setControlState(QtCore.Qt.RightButton, True)
        else:
            self.setControlState(QtCore.Qt.RightButton, False)

    def transformCamera(self):
        tx = self.speeds[SPD_MOVE_X] * self.delta
        ty = self.speeds[SPD_MOVE_Y] * self.delta
        tz = self.speeds[SPD_MOVE_Z] * self.delta
        rx = self.speeds[SPD_ROTATE_X]  # up/down
        ry = self.speeds[SPD_ROTATE_Y]  # left/right

        m.xform(self.camera, relative=True, objectSpace=True, translation=(tx, ty, tz))
        m.xform(self.camera, relative=True, objectSpace=True, rotation=(self.invertMouse * rx, 0, 0))
        m.xform(self.camera, relative=True, worldSpace=True, rotation=(0, ry, 0) if Y_UP else (0, 0, ry))

    def calculateSpeeds(self):

        # speed modificators
        if self.controls[QtCore.Qt.Key_Shift] and not self.controls[QtCore.Qt.Key_Control]:
            self.maxSpeedModified = self.maxSpeed * self.shiftSpeedMultiplier
        elif not self.controls[QtCore.Qt.Key_Shift] and self.controls[QtCore.Qt.Key_Control]:
            self.maxSpeedModified = self.maxSpeed * self.controlSpeedMultiplier
        else:
            self.maxSpeedModified = self.maxSpeed

        self.acceleration = self.maxSpeedModified / self.accelerationTime

        # forward/backward
        if self.controls[QtCore.Qt.Key_W] and not self.controls[QtCore.Qt.Key_S]:
            self.speeds[SPD_MOVE_Z] = self.calculateNewSpeed(self.speeds[SPD_MOVE_Z], -self.acceleration)
        elif not self.controls[QtCore.Qt.Key_W] and self.controls[QtCore.Qt.Key_S]:
            self.speeds[SPD_MOVE_Z] = self.calculateNewSpeed(self.speeds[SPD_MOVE_Z], self.acceleration)
        else:
            self.speeds[SPD_MOVE_Z] = self.calculateNewSpeed(self.speeds[SPD_MOVE_Z], 0.0)

        # left/right
        if self.controls[QtCore.Qt.Key_D] and not self.controls[QtCore.Qt.Key_A]:
            self.speeds[SPD_MOVE_X] = self.calculateNewSpeed(self.speeds[SPD_MOVE_X], self.acceleration)
        elif not self.controls[QtCore.Qt.Key_D] and self.controls[QtCore.Qt.Key_A]:
            self.speeds[SPD_MOVE_X] = self.calculateNewSpeed(self.speeds[SPD_MOVE_X], -self.acceleration)
        else:
            self.speeds[SPD_MOVE_X] = self.calculateNewSpeed(self.speeds[SPD_MOVE_X], 0.0)

        # up/down
        if self.controls[QtCore.Qt.LeftButton] and not self.controls[QtCore.Qt.RightButton]:
            self.speeds[SPD_MOVE_Y] = self.calculateNewSpeed(self.speeds[SPD_MOVE_Y], -self.acceleration * self.swapMouseButtons)
        elif not self.controls[QtCore.Qt.LeftButton] and self.controls[QtCore.Qt.RightButton]:
            self.speeds[SPD_MOVE_Y] = self.calculateNewSpeed(self.speeds[SPD_MOVE_Y], self.acceleration * self.swapMouseButtons)
        else:
            self.speeds[SPD_MOVE_Y] = self.calculateNewSpeed(self.speeds[SPD_MOVE_Y], 0.0)

        # rotation
        self.speeds[SPD_ROTATE_X] = -self.mouseData[MOUSE_VER] * self.rotateSpeed
        self.speeds[SPD_ROTATE_Y] = -self.mouseData[MOUSE_HOR] * self.rotateSpeed

    def calculateNewSpeed(self, speed, acc):
        absSpeed = abs(speed)
        if (acc == 0.0) and (absSpeed / self.maxSpeedModified < self.stopThreshold):
            return 0

        return speed + (acc + self.getDragAcceleration(speed)) * self.delta

    def getDragAcceleration(self, speed):
        return -1 * (speed / self.maxSpeedModified) * self.acceleration

    def setControlState(self, control, state):
        if control in self.controls:
            self.controls[control] = state

    def execAction(self, key):
        if key in self.actions:
            self.actions[key]()

    def raiseWindows(self):
        self.ui.raiseWindows()

    def onShowHelp(self):
        self.ui.toggleHelp()

    def onChangeSpeed(self, inc):
        self.maxSpeed = self.maxSpeed * 2 if inc else self.maxSpeed / 2

    def onChangeRotationSpeed(self, inc):
        self.rotateSpeed = self.rotateSpeed * 1.2 if inc else self.rotateSpeed / 1.2

    def onInvertMouse(self):
        if self.invertMouse == 1:
            self.invertMouse = -1
        else:
            self.invertMouse = 1

    def onSwapMouseButtons(self):
        if self.swapMouseButtons == 1:
            self.swapMouseButtons = -1
        else:
            self.swapMouseButtons = 1

    def onGameViewToggle(self):
        self.useGameView = not self.useGameView
        if self.useGameView:
            self.modifyCameraToGameView()
        else:
            self.restoreCamera()

    def onShowDebug(self):
        self.ui.toggleDebugInfo()

    def getControlState(self, control):
        return self.controls[control]

    def setupOptionVars(self):
        self.optionVarLinks = []
        self.optionVarLinks.extend([
            OptionVarLink(OPT_VAR_PREFIX + 'maxSpeed', 10.0, lambda: self.maxSpeed,
                          lambda a: setattr(self, 'maxSpeed', a)),
            OptionVarLink(OPT_VAR_PREFIX + 'rotateSpeed', 0.1, lambda: self.rotateSpeed,
                          lambda a: setattr(self, 'rotateSpeed', a)),
            OptionVarLink(OPT_VAR_PREFIX + 'invertMouse', 1, lambda: self.invertMouse,
                          lambda a: setattr(self, 'invertMouse', a)),
            OptionVarLink(OPT_VAR_PREFIX + 'swapMouseButtons', 1, lambda: self.swapMouseButtons,
                          lambda a: setattr(self, 'swapMouseButtons', a)),
            OptionVarLink(OPT_VAR_PREFIX + 'useGameView', 0, lambda: self.useGameView,
                          lambda a: setattr(self, 'useGameView', a))
        ])

        self.settingsInit()
        self.settingsLoad()

    def settingsInit(self):
        for ov in self.optionVarLinks:
            ov.init()

    def settingsLoad(self):
        for ov in self.optionVarLinks:
            ov.applyToControl()

    def settingsSave(self):
        for ov in self.optionVarLinks:
            ov.getFromControl()

    def settingsReset(self):
        for ov in self.optionVarLinks:
            ov.reset()


class OptionVarLink(object):

    def __init__(self, ovName, defaultValue, getFromControlFunc, setToControlFunc):
        self.ovName = ovName
        self.defaultValue = defaultValue
        self.getFromControlFunc = getFromControlFunc
        self.setToControlFunc = setToControlFunc

    def init(self):
        optVars = pm.env.optionVars
        if self.ovName not in optVars:
            optVars[self.ovName] = self.defaultValue

    def applyToControl(self):
        optVars = pm.env.optionVars
        self.setToControlFunc(optVars[self.ovName])

    def getFromControl(self):
        optVars = pm.env.optionVars
        optVars[self.ovName] = self.getFromControlFunc()

    def reset(self):
        optVars = pm.env.optionVars
        optVars.pop(self.ovName)
        self.init()
        self.applyToControl()


def run():

#    from pydev import pydevd
#    pydevd.settrace('localhost', port=62882, stdoutToServer=True, stderrToServer=True)

    global flyer
    flyer = Flyer()

    flyer.fly()
