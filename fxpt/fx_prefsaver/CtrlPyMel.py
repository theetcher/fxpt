from functools import partial

from CtrlBase import CtrlBase
from PSTypes import UIType, Attr

from com import message


class PMCtrlBase(CtrlBase):

    def __init__(self, control, defaultValue):
        super(PMCtrlBase, self).__init__(control, defaultValue)

        self.attr = None
        self.ctrlGetter = None
        self.ctrlSetter = None

    def ctrl2Data(self):
        super(PMCtrlBase, self).ctrl2Data()
        self.ctrl2DataProcedure()

    def data2Ctrl(self, prefDataGlobal):
        super(PMCtrlBase, self).data2Ctrl(prefDataGlobal)
        self.data2CtrlProcedure()

    def ctrl2DataProcedure(self):
        self.setAttr(self.attr, self.ctrlGetter())

    def data2CtrlProcedure(self):
        self.ctrlSetter(self.getAttr(self.attr))

    def setupGetSetVars(self, attr, getter, setter):
        self.attr = attr
        self.ctrlGetter = getter
        self.ctrlSetter = setter

    def retrieveControlName(self):
        return self.control.shortName()


class PMCtrlSimple(PMCtrlBase):
    def __init__(self, *args, **kwargs):
        super(PMCtrlSimple, self).__init__(*args, **kwargs)
        self.setupGetSetVars(Attr.Value, self.control.getValue, self.control.setValue)


class PMCtrlColorSliderGrp(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlColorSliderGrp, self).__init__(*args, **kwargs)
        self.setupGetSetVars(Attr.Value, self.control.getRgbValue, self.control.setRgbValue)


class PMCtrlFrameLayout(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlFrameLayout, self).__init__(*args, **kwargs)
        self.setupGetSetVars(Attr.Value, self.control.getCollapse, self.control.setCollapse)


class PMCtrlRadioButton(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlRadioButton, self).__init__(*args, **kwargs)
        self.setupGetSetVars(Attr.Value, self.control.getSelect, self.control.setSelect)


class PMCtrlScrollField(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlScrollField, self).__init__(*args, **kwargs)
        self.setupGetSetVars(Attr.Value, self.control.getText, self.control.setText)


class PMCtrlTabLayout(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlTabLayout, self).__init__(*args, **kwargs)
        self.setupGetSetVars(Attr.Value, self.control.getSelectTabIndex, self.control.setSelectTabIndex)


class PMCtrlTextField(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlTextField, self).__init__(*args, **kwargs)
        self.setupGetSetVars(Attr.Value, self.control.getText, self.control.setText)


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
    def ctrl2DataProcedure(self):
        self.setAttr(Attr.Value, [self.getters[i]() for i in range(self.grpSize)])

    # noinspection PyCallingNonCallable
    def data2CtrlProcedure(self):
        prefValue = self.getAttr(Attr.Value)
        for i in range(self.grpSize):
            self.setters[i](prefValue[i])


class PMCtrlScrollLayout(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlScrollLayout, self).__init__(*args, **kwargs)

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.ScrollValues, self.control.getScrollAreaValue())

    def data2CtrlProcedure(self):
        currentScrollDown, currentScrollRight = self.control.getScrollAreaValue()
        prefValue = self.getAttr(Attr.ScrollValues)
        self.control.scrollByPixel(['up', currentScrollDown])
        self.control.scrollByPixel(['left', currentScrollRight])
        self.control.scrollByPixel(['down', prefValue[0]])
        self.control.scrollByPixel(['right', prefValue[1]])


class PMCtrlTextScrollList(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlTextScrollList, self).__init__(*args, **kwargs)

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.SelectedIndexes, self.control.getSelectIndexedItem() or [])

    def data2CtrlProcedure(self):
        self.control.deselectAll()
        self.control.setSelectIndexedItem(self.getAttr(Attr.SelectedIndexes))


class PMCtrlScriptTable(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlScriptTable, self).__init__(*args, **kwargs)

    def ctrl2DataProcedure(self):
        controlData = self.control.getSelectedCells()
        self.setAttr(Attr.SelectedIndexes, [0, 0] if controlData is None else controlData)

    def data2CtrlProcedure(self):
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
    UIType.PMIconTextScrollList: PMCtrlTextScrollList,
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
    UIType.PMScrollField: PMCtrlScrollField,
    UIType.PMScrollLayout: PMCtrlScrollLayout,
    UIType.PMShelfTabLayout: PMCtrlTabLayout,
    UIType.PMTabLayout: PMCtrlTabLayout,
    UIType.PMTextField: PMCtrlTextField,
    UIType.PMTextFieldButtonGrp: PMCtrlTextField,
    UIType.PMTextFieldGrp: PMCtrlTextField,
    UIType.PMTextScrollList: PMCtrlTextScrollList
}


# noinspection PyCallingNonCallable
def getController(uiType, control, defaultValue):

    if uiType in UIType.TypesPM:
        return constructors[uiType](control, defaultValue)
    else:
        message('Cannot create controller: Unknown controller type: {}.'.format(str(uiType)))
