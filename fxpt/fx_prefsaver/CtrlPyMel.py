from functools import partial

import pymel.core as pm

from CtrlBase import CtrlBase
from PSTypes import UIType, Attr

from com import message


class PMCtrlBase(CtrlBase):

    def __init__(self, control, defaultValue):
        super(PMCtrlBase, self).__init__(control, defaultValue)

    def retrieveControlName(self):
        return self.control.getFullPathName().split('|')[-1]


class PMCtrlSimple(PMCtrlBase):
    def __init__(self, *args, **kwargs):
        super(PMCtrlSimple, self).__init__(*args, **kwargs)

    def ctrl2Data(self):
        super(PMCtrlSimple, self).ctrl2Data()
        self.setAttr(Attr.Value, self.control.getValue())

    def data2Ctrl(self, prefData):
        super(PMCtrlSimple, self).data2Ctrl(prefData)
        self.control.setValue(self.getAttr(Attr.Value))


class PMCtrlGrp4Simple(PMCtrlBase):

    def __init__(self, grpSize, *args, **kwargs):
        super(PMCtrlGrp4Simple, self).__init__(*args, **kwargs)
        self.grpSize = grpSize
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

    # noinspection PyCallingNonCallable
    def ctrl2Data(self):
        super(PMCtrlGrp4Simple, self).ctrl2Data()
        self.setAttr(Attr.Value, [self.getters[i]() for i in range(self.grpSize)])

    # noinspection PyCallingNonCallable
    def data2Ctrl(self, prefData):
        super(PMCtrlGrp4Simple, self).data2Ctrl(prefData)
        prefValue = self.getAttr(Attr.Value)
        for i in range(self.grpSize):
            self.setters[i](prefValue[i])


class PMCtrlColorSliderGrp(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlColorSliderGrp, self).__init__(*args, **kwargs)

    def ctrl2Data(self):
        super(PMCtrlColorSliderGrp, self).ctrl2Data()
        self.setAttr(Attr.ColorRGB, self.control.getRgbValue())

    def data2Ctrl(self, prefData):
        super(PMCtrlColorSliderGrp, self).data2Ctrl(prefData)
        self.control.setRgbValue(self.getAttr(Attr.ColorRGB))


class PMCtrlFloatSlider2(PMCtrlBase):
    def __init__(self, *args, **kwargs):
        super(PMCtrlFloatSlider2, self).__init__(*args, **kwargs)

    # def retrieveControlName(self):
    #     print self.control.getFullPathName()
    #     return 'aaa'

    def ctrl2Data(self):
        super(PMCtrlFloatSlider2, self).ctrl2Data()
        self.setAttr(Attr.Value, [self.control.getValue1(), self.control.getValue2()])

    def data2Ctrl(self, prefData):
        super(PMCtrlFloatSlider2, self).data2Ctrl(prefData)
        prefValue = self.getAttr(Attr.Value)
        self.control.setValue1(prefValue[0])
        self.control.setValue2(prefValue[1])


constructors = {
    # UIType.PMCheckBox: PMCtrlCheckBox,
    UIType.PMCheckBox: PMCtrlSimple,
    UIType.PMCheckBoxGrp1: partial(PMCtrlGrp4Simple, 1),
    UIType.PMCheckBoxGrp2: partial(PMCtrlGrp4Simple, 2),
    UIType.PMCheckBoxGrp3: partial(PMCtrlGrp4Simple, 3),
    UIType.PMCheckBoxGrp4: partial(PMCtrlGrp4Simple, 4),
    UIType.PMColorSliderGrp: PMCtrlColorSliderGrp,
    UIType.PMFloatField: PMCtrlSimple,
    UIType.PMFloatFieldGrp1: partial(PMCtrlGrp4Simple, 1),
    UIType.PMFloatFieldGrp2: partial(PMCtrlGrp4Simple, 2),
    UIType.PMFloatFieldGrp3: partial(PMCtrlGrp4Simple, 3),
    UIType.PMFloatFieldGrp4: partial(PMCtrlGrp4Simple, 4),
    UIType.PMFloatScrollBar: PMCtrlSimple,
    UIType.PMFloatSlider: PMCtrlSimple,
    UIType.PMFloatSliderGrp: PMCtrlBase,
    UIType.PMFrameLayout: PMCtrlBase,
    UIType.PMIconTextCheckBox: PMCtrlBase,
    UIType.PMIconTextRadioButton: PMCtrlBase,
    UIType.PMIconTextScrollList: PMCtrlBase,
    UIType.PMIntField: PMCtrlBase,
    UIType.PMIntFieldGrp1: PMCtrlBase,
    UIType.PMIntFieldGrp2: PMCtrlBase,
    UIType.PMIntFieldGrp3: PMCtrlBase,
    UIType.PMIntFieldGrp4: PMCtrlBase,
    UIType.PMIntScrollBar: PMCtrlBase,
    UIType.PMIntSlider: PMCtrlBase,
    UIType.PMIntSliderGrp: PMCtrlBase,
    UIType.PMOptionMenu: PMCtrlBase,
    UIType.PMOptionMenuGrp: PMCtrlBase,
    UIType.PMRadioButton: PMCtrlBase,
    UIType.PMRadioButtonGrp1: PMCtrlBase,
    UIType.PMRadioButtonGrp2: PMCtrlBase,
    UIType.PMRadioButtonGrp3: PMCtrlBase,
    UIType.PMRadioButtonGrp4: PMCtrlBase,
    UIType.PMSymbolCheckBox: PMCtrlBase,
    UIType.PMScriptTable: PMCtrlBase,
    UIType.PMScrollField: PMCtrlBase,
    UIType.PMScrollLayout: PMCtrlBase,
    UIType.PMShelfTabLayout: PMCtrlBase,
    UIType.PMTabLayout: PMCtrlBase,
    UIType.PMTextField: PMCtrlBase,
    UIType.PMTextFieldButtonGrp: PMCtrlBase,
    UIType.PMTextFieldGrp: PMCtrlBase,
    UIType.PMTextScrollList: PMCtrlBase
}


# noinspection PyCallingNonCallable
def getController(uiType, control, defaultValue):

    if uiType in UIType.TypesPM:
        return constructors[uiType](control, defaultValue)
    else:
        message('Cannot create controller: Unknown controller type: {}.'.format(str(uiType)))
