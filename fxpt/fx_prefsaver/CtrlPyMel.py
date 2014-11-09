import pymel.core as pm

from CtrlBase import CtrlBase
from PSTypes import UIType, Attr

from com import message


class PMCtrlBase(CtrlBase):

    def __init__(self, control, defaultValue):
        super(PMCtrlBase, self).__init__(control, defaultValue)

    def getControlName(self):
        return self.control.getFullPathName().split('|')[-1]


class PMCtrlCheckBox(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlCheckBox, self).__init__(*args, **kwargs)

    def ctrl2Data(self):
        super(PMCtrlCheckBox, self).ctrl2Data()
        self.setAttr(Attr.CheckState, self.control.getValue())

    def data2Ctrl(self, prefData):
        super(PMCtrlCheckBox, self).data2Ctrl(prefData)
        prefValue = self.getAttr(Attr.CheckState)
        self.control.setValue(prefValue if prefValue else self.defaultValue)


constructors = {
    UIType.PMCheckBox: PMCtrlCheckBox
}


# noinspection PyCallingNonCallable
def getController(uiType, control, defaultValue):

    if uiType in UIType.TypesPM:
        return constructors[uiType](control, defaultValue)
    else:
        message('Cannot create controller: Unknown controller type: {}.'.format(str(uiType)))
