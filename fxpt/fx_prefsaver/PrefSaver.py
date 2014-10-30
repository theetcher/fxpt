#region imports
import os

from UITypes import UITypes

import CtrlQt
try:
    import CtrlMaya
except ImportError:
    CtrlMaya = None

try:
    import CtrlPyMel
except ImportError:
    CtrlPyMel = None

from com import message

# from watch import *
#endregion


class PrefSaver(object):

    def __init__(self, serializer):
        super(PrefSaver, self).__init__()
        self.serializer = serializer
        self.controllers = []
        self.prefDict = {}

    # noinspection PyCallingNonCallable
    def addControl(self, control, uiType, defaultValue):

        if uiType not in UITypes.TypesAll:
            message('Cannot add unknown control type ({}) for {}. Skipped'.format(uiType, str(control)))
            return

        if uiType in (UITypes.TypesPYQT | UITypes.TypesPYSIDE):
            controller = CtrlQt.getController(uiType, control, defaultValue)
            if controller:
                self.controllers.append(controller)
            else:
                message('Failed to add controller (type={}) for {}'.format(uiType, str(control)))
            return

        if uiType in UITypes.TypesM:
            if CtrlMaya:
                self.controllers.append(CtrlMaya.getController(uiType, control, defaultValue))
            else:
                message('Failed to add controller (type={}) for {}'.format(uiType, str(control)))
            return

        if uiType in UITypes.TypesPM:
            if CtrlPyMel:
                self.controllers.append(CtrlPyMel.getController(uiType, control, defaultValue))
            else:
                message('Failed to add controller (type={}) for {}'.format(uiType, str(control)))
            return

        assert False, 'Failed to add a controller.'

    # noinspection PyCallingNonCallable
    # def addVariable(self, name, getFromVarFunc, setToVarFunc, defaultValue):
    #     self.controls.append(UIType.Constructors[UIType.Variable](
    #         name, getFromVarFunc, setToVarFunc, defaultValue, self.optVarPrefix))

    def savePrefs(self):
        self.gatherPrefs()
        self.pickleSave(self.prefDict, self.filename)

    def loadPrefs(self):
        if os.path.exists(self.filename):
            self.prefDict = self.pickleLoad(self.filename)
        else:
            self.prefDict = {}
        self.applyPrefs()

    def resetPrefs(self):
        self.prefDict = {}
        self.applyPrefs()

    def gatherPrefs(self):
        self.prefDict = {}
        for ctrlDesc in self.controllers:
            ctrlDesc.ctrlToDict(self.prefDict)

    def applyPrefs(self):
        for ctrlDesc in self.controllers:
            ctrlDesc.dictToCtrl(self.prefDict)


