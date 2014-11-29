from functools import partial

from CtrlBase import CtrlBase
from PSTypes import UIType, Attr
from com import message


class PMCtrlBase(CtrlBase):

    def __init__(self, control, defaultValue):
        super(PMCtrlBase, self).__init__(control, defaultValue)

    def retrieveControlName(self):
        return self.control.shortName()


class PMCtrlSimple(PMCtrlBase):
    def __init__(self, globalDefault, *args, **kwargs):
        super(PMCtrlSimple, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = globalDefault
        self.setupGetSetVars(Attr.Value, self.control.getValue, self.control.setValue)


class PMCtrlColorSliderGrp(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlColorSliderGrp, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = (0, 0, 0)
        self.setupGetSetVars(Attr.Value, self.control.getRgbValue, self.control.setRgbValue)


class PMCtrlFrameLayout(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlFrameLayout, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = False
        self.setupGetSetVars(Attr.Value, self.control.getCollapse, self.control.setCollapse)


class PMCtrlRadioButton(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlRadioButton, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = False
        self.setupGetSetVars(Attr.Value, self.control.getSelect, self.control.setSelect)


class PMCtrlOptionMenu(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlOptionMenu, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = 1

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.CurrentIndex, self.control.getSelect())

    def data2CtrlProcedure(self):
        prefValue = self.getAttr(Attr.CurrentIndex)
        if 0 < prefValue <= self.control.getNumberOfItems():
            self.control.setSelect(prefValue)


class PMCtrlTabLayout(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlTabLayout, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = 1

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.Value, self.control.getSelectTabIndex())

    def data2CtrlProcedure(self):
        prefValue = self.getAttr(Attr.Value)
        if 0 < prefValue <= self.control.getNumberOfChildren():
            self.control.setSelectTabIndex(prefValue)


class PMCtrlTextField(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlTextField, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = ''
        self.setupGetSetVars(Attr.Value, self.control.getText, self.control.setText)


class PMCtrlGrp4Simple(PMCtrlBase):

    def __init__(self, globalDefault, grpSize, *args, **kwargs):
        super(PMCtrlGrp4Simple, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = globalDefault
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
        self.defaultValueGlobal = (0, 0)

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
        self.defaultValueGlobal = ()

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.SelectedIndexes, self.control.getSelectIndexedItem() or [])

    def data2CtrlProcedure(self):
        self.control.deselectAll()
        # in case of invalid index. IconTextScrollList does not have a method for getting number of items.
        # so i cannot check a validity of index.
        try:
            self.control.setSelectIndexedItem(self.getAttr(Attr.SelectedIndexes))
        except RuntimeError:
            pass


class PMCtrlScriptTable(PMCtrlBase):

    def __init__(self, *args, **kwargs):
        super(PMCtrlScriptTable, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = (0, 0)

    def ctrl2DataProcedure(self):
        controlData = self.control.getSelectedCells()
        self.setAttr(Attr.SelectedIndexes, [0, 0] if controlData is None else controlData)

    def data2CtrlProcedure(self):
        self.control.setSelectedCells(self.getAttr(Attr.SelectedIndexes))


constructors = {
    UIType.PMCheckBox: partial(PMCtrlSimple, False),
    UIType.PMCheckBoxGrp1: partial(PMCtrlGrp4Simple, [False], 1),
    UIType.PMCheckBoxGrp2: partial(PMCtrlGrp4Simple, [False, False], 2),
    UIType.PMCheckBoxGrp3: partial(PMCtrlGrp4Simple, [False, False, False], 3),
    UIType.PMCheckBoxGrp4: partial(PMCtrlGrp4Simple, [False, False, False, False], 4),
    UIType.PMColorSliderGrp: PMCtrlColorSliderGrp,
    UIType.PMFloatField: partial(PMCtrlSimple, 0),
    UIType.PMFloatFieldGrp1: partial(PMCtrlGrp4Simple, [0], 1),
    UIType.PMFloatFieldGrp2: partial(PMCtrlGrp4Simple, [0, 0], 2),
    UIType.PMFloatFieldGrp3: partial(PMCtrlGrp4Simple, [0, 0, 0], 3),
    UIType.PMFloatFieldGrp4: partial(PMCtrlGrp4Simple, [0, 0, 0, 0], 4),
    UIType.PMFloatScrollBar: partial(PMCtrlSimple, 0),
    UIType.PMFloatSlider: partial(PMCtrlSimple, 0),
    UIType.PMFloatSliderGrp: partial(PMCtrlSimple, 0),
    UIType.PMFrameLayout: PMCtrlFrameLayout,
    UIType.PMIconTextCheckBox: partial(PMCtrlSimple, False),
    UIType.PMIconTextRadioButton: PMCtrlRadioButton,
    UIType.PMIconTextScrollList: PMCtrlTextScrollList,
    UIType.PMIntField: partial(PMCtrlSimple, 0),
    UIType.PMIntFieldGrp1: partial(PMCtrlGrp4Simple, [0], 1),
    UIType.PMIntFieldGrp2: partial(PMCtrlGrp4Simple, [0, 0], 2),
    UIType.PMIntFieldGrp3: partial(PMCtrlGrp4Simple, [0, 0, 0], 3),
    UIType.PMIntFieldGrp4: partial(PMCtrlGrp4Simple, [0, 0, 0, 0], 4),
    UIType.PMIntScrollBar: partial(PMCtrlSimple, 0),
    UIType.PMIntSlider: partial(PMCtrlSimple, 0),
    UIType.PMIntSliderGrp: partial(PMCtrlSimple, 0),
    UIType.PMOptionMenu: PMCtrlOptionMenu,
    UIType.PMOptionMenuGrp: PMCtrlOptionMenu,
    UIType.PMRadioButton: PMCtrlRadioButton,
    UIType.PMRadioButtonGrp1: PMCtrlRadioButton,
    UIType.PMRadioButtonGrp2: PMCtrlRadioButton,
    UIType.PMRadioButtonGrp3: PMCtrlRadioButton,
    UIType.PMRadioButtonGrp4: PMCtrlRadioButton,
    UIType.PMSymbolCheckBox: partial(PMCtrlSimple, False),
    UIType.PMScriptTable: PMCtrlScriptTable,
    UIType.PMScrollField: PMCtrlTextField,
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

    if uiType in constructors:
        return constructors[uiType](control, defaultValue)
    else:
        message('Cannot create controller: Unknown controller type: {}.'.format(str(uiType)))
