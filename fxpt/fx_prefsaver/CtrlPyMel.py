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


class PMCtrlScrollLayout(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlScrollLayout, self).__init__(*args, **kwargs)

    def ctrl2Data(self):
        super(PMCtrlScrollLayout, self).ctrl2Data()
        self.setAttr(Attr.ScrollValues, self.control.getScrollAreaValue())

    def data2Ctrl(self, prefData):
        super(PMCtrlScrollLayout, self).data2Ctrl(prefData)
        currentScrollDown, currentScrollRight = self.control.getScrollAreaValue()
        prefValue = self.getAttr(Attr.ScrollValues)
        self.control.scrollByPixel(['up', currentScrollDown])
        self.control.scrollByPixel(['left', currentScrollRight])
        self.control.scrollByPixel(['down', prefValue[0]])
        self.control.scrollByPixel(['right', prefValue[1]])


class PMCtrlFrameLayout(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlFrameLayout, self).__init__(*args, **kwargs)

    def ctrl2Data(self):
        super(PMCtrlFrameLayout, self).ctrl2Data()
        self.setAttr(Attr.Collapsed, self.control.getCollapse())

    def data2Ctrl(self, prefData):
        super(PMCtrlFrameLayout, self).data2Ctrl(prefData)
        self.control.setCollapse(self.getAttr(Attr.Collapsed))


class PMCtrlRadioButton(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlRadioButton, self).__init__(*args, **kwargs)

    def ctrl2Data(self):
        super(PMCtrlRadioButton, self).ctrl2Data()
        self.setAttr(Attr.Value, self.control.getSelect())

    def data2Ctrl(self, prefData):
        super(PMCtrlRadioButton, self).data2Ctrl(prefData)
        self.control.setSelect(self.getAttr(Attr.Value))


class PMCtrlIconTextScrollList(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlIconTextScrollList, self).__init__(*args, **kwargs)

    def ctrl2Data(self):
        super(PMCtrlIconTextScrollList, self).ctrl2Data()
        self.setAttr(Attr.SelectedIndexes, self.control.getSelectIndexedItem() or [])

    def data2Ctrl(self, prefData):
        super(PMCtrlIconTextScrollList, self).data2Ctrl(prefData)
        self.control.deselectAll()
        self.control.setSelectIndexedItem(self.getAttr(Attr.SelectedIndexes))


class PMCtrlScriptTable(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlScriptTable, self).__init__(*args, **kwargs)

    def ctrl2Data(self):
        super(PMCtrlScriptTable, self).ctrl2Data()
        self.setAttr(Attr.SelectedIndexes, self.control.getSelectedCells() or [])

    def data2Ctrl(self, prefData):
        super(PMCtrlScriptTable, self).data2Ctrl(prefData)
        self.control.setSelectedCells(self.getAttr(Attr.SelectedIndexes))


constructors = {
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
    UIType.PMFloatSliderGrp: PMCtrlSimple,
    UIType.PMFrameLayout: PMCtrlFrameLayout,
    UIType.PMIconTextCheckBox: PMCtrlSimple,
    UIType.PMIconTextRadioButton: PMCtrlRadioButton,
    UIType.PMIconTextScrollList: PMCtrlIconTextScrollList,
    UIType.PMIntField: PMCtrlSimple,
    UIType.PMIntFieldGrp1: partial(PMCtrlGrp4Simple, 1),
    UIType.PMIntFieldGrp2: partial(PMCtrlGrp4Simple, 2),
    UIType.PMIntFieldGrp3: partial(PMCtrlGrp4Simple, 3),
    UIType.PMIntFieldGrp4: partial(PMCtrlGrp4Simple, 4),
    UIType.PMIntScrollBar: PMCtrlSimple,
    UIType.PMIntSlider: PMCtrlSimple,
    UIType.PMIntSliderGrp: PMCtrlSimple,
    UIType.PMOptionMenu: PMCtrlRadioButton,
    UIType.PMOptionMenuGrp: PMCtrlRadioButton,
    UIType.PMRadioButton: PMCtrlRadioButton,
    UIType.PMRadioButtonGrp1: PMCtrlRadioButton,
    UIType.PMRadioButtonGrp2: PMCtrlRadioButton,
    UIType.PMRadioButtonGrp3: PMCtrlRadioButton,
    UIType.PMRadioButtonGrp4: PMCtrlRadioButton,
    UIType.PMSymbolCheckBox: PMCtrlSimple,
    UIType.PMScriptTable: PMCtrlScriptTable,
    UIType.PMScrollField: PMCtrlBase,
    UIType.PMScrollLayout: PMCtrlScrollLayout,
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
