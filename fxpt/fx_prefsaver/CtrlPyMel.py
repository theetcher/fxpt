import pymel.core as pm

from CtrlBase import CtrlBase
from PSTypes import UIType, Attr

from com import message


class PMCtrlBase(CtrlBase):

    def __init__(self, control, defaultValue):
        super(PMCtrlBase, self).__init__(control, defaultValue)

    def retrieveControlName(self):
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


class PMCtrlCheckBoxGrp1(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlCheckBoxGrp1, self).__init__(*args, **kwargs)
        self.getters = {
            0: self.control.getValue1,
            1: self.control.getValue2,
            2: self.control.getValue3,
            3: self.control.getValue4
        }
        self.setters = {
            0: self.control.setValue1,
            1: self.control.setValue2,
            2: self.control.setValue3,
            3: self.control.setValue4
        }
        self.grpSize = 1

    # noinspection PyCallingNonCallable
    def ctrl2Data(self):
        super(PMCtrlCheckBoxGrp1, self).ctrl2Data()
        self.setAttr(Attr.CheckState, [self.getters[i]() for i in range(self.grpSize)])

    # noinspection PyCallingNonCallable
    def data2Ctrl(self, prefData):
        super(PMCtrlCheckBoxGrp1, self).data2Ctrl(prefData)
        prefValue = self.getAttr(Attr.CheckState)
        for i in range(self.grpSize):
            self.setters[i](prefValue[i])


class PMCtrlCheckBoxGrp2(PMCtrlCheckBoxGrp1):

    def __init__(self, *args, **kwargs):
        super(PMCtrlCheckBoxGrp2, self).__init__(*args, **kwargs)
        self.grpSize = 2


class PMCtrlCheckBoxGrp3(PMCtrlCheckBoxGrp1):

    def __init__(self, *args, **kwargs):
        super(PMCtrlCheckBoxGrp3, self).__init__(*args, **kwargs)
        self.grpSize = 3


class PMCtrlCheckBoxGrp4(PMCtrlCheckBoxGrp1):

    def __init__(self, *args, **kwargs):
        super(PMCtrlCheckBoxGrp4, self).__init__(*args, **kwargs)
        self.grpSize = 4


constructors = {
    UIType.PMCheckBox: PMCtrlCheckBox,
    UIType.PMCheckBoxGrp1: PMCtrlCheckBoxGrp1,
    UIType.PMCheckBoxGrp2: PMCtrlCheckBoxGrp2,
    UIType.PMCheckBoxGrp3: PMCtrlCheckBoxGrp3,
    UIType.PMCheckBoxGrp4: PMCtrlCheckBoxGrp4,

}


# noinspection PyCallingNonCallable
def getController(uiType, control, defaultValue):

    if uiType in UIType.TypesPM:
        return constructors[uiType](control, defaultValue)
    else:
        message('Cannot create controller: Unknown controller type: {}.'.format(str(uiType)))
