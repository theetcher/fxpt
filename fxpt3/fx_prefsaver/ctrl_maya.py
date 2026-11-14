from functools import partial

import maya.cmds as m

from fxpt3.fx_prefsaver.ctrl_base import CtrlBase
from fxpt3.fx_prefsaver.pstypes import UIType, Attr
from fxpt3.fx_prefsaver.com import message


# Controllers for maya.cmds UI controls. They work with plain control names (strings)
# and do not need PyMEL, which is an optional install in Maya 2023+.


class MCtrlBase(CtrlBase):

    def __init__(self, cmd, *args, **kwargs):
        self.cmd = cmd
        super(MCtrlBase, self).__init__(*args, **kwargs)

    def retrieveControlName(self):
        # short name, same as PyMEL's shortName(), so prefs saved by the old PyMEL-based version still match
        return str(self.control).split('|')[-1]

    def query(self, flag):
        return self.cmd(self.control, q=True, **{flag: True})

    def edit(self, flag, value):
        self.cmd(self.control, e=True, **{flag: value})


class MCtrlQueryEdit(MCtrlBase):

    def __init__(self, cmd, flag, globalDefault, *args, **kwargs):
        super(MCtrlQueryEdit, self).__init__(cmd, *args, **kwargs)
        self.defaultValueGlobal = globalDefault
        self.setupGetSetVars(Attr.Value, partial(self.query, flag), partial(self.edit, flag))


class MCtrlColorSliderGrp(MCtrlBase):

    def __init__(self, *args, **kwargs):
        super(MCtrlColorSliderGrp, self).__init__(m.colorSliderGrp, *args, **kwargs)
        self.defaultValueGlobal = (0, 0, 0)

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.Value, self.query('rgbValue'))

    def data2CtrlProcedure(self):
        self.edit('rgbValue', tuple(self.getAttr(Attr.Value)))


class MCtrlRadioButton(MCtrlBase):

    def __init__(self, *args, **kwargs):
        super(MCtrlRadioButton, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = False

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.Value, self.query('select'))

    def data2CtrlProcedure(self):
        # radio buttons can only be selected in edit mode, not deselected.
        # the other button in the collection deselects this one when it is selected.
        if self.getAttr(Attr.Value):
            self.edit('select', True)


class MCtrlOptionMenu(MCtrlBase):

    def __init__(self, *args, **kwargs):
        super(MCtrlOptionMenu, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = 1

    def getNumberOfItems(self):
        return self.query('numberOfItems')

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.CurrentIndex, self.query('select'))

    def data2CtrlProcedure(self):
        prefValue = self.getAttr(Attr.CurrentIndex)
        if 0 < prefValue <= (self.getNumberOfItems() or 0):
            self.edit('select', prefValue)


class MCtrlOptionMenuGrp(MCtrlOptionMenu):

    def getNumberOfItems(self):
        # optionMenuGrp has no numberOfItems flag. Ask its child optionMenu (same as PyMEL's OptionMenuGrp.menu()).
        return m.optionMenu(self.control + '|OptionMenu', q=True, numberOfItems=True)


class MCtrlTabLayout(MCtrlBase):

    def __init__(self, *args, **kwargs):
        super(MCtrlTabLayout, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = 1

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.Value, self.query('selectTabIndex'))

    def data2CtrlProcedure(self):
        prefValue = self.getAttr(Attr.Value)
        if 0 < prefValue <= (self.query('numberOfChildren') or 0):
            self.edit('selectTabIndex', prefValue)


class MCtrlGrp4Simple(MCtrlBase):

    def __init__(self, cmd, globalDefault, grpSize, *args, **kwargs):
        super(MCtrlGrp4Simple, self).__init__(cmd, *args, **kwargs)
        self.defaultValueGlobal = globalDefault
        self.grpSize = grpSize

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.Value, [self.query('value{0}'.format(i + 1)) for i in range(self.grpSize)])

    def data2CtrlProcedure(self):
        prefValue = self.getAttr(Attr.Value)
        for i in range(self.grpSize):
            self.edit('value{0}'.format(i + 1), prefValue[i])


class MCtrlScrollLayout(MCtrlBase):

    def __init__(self, *args, **kwargs):
        super(MCtrlScrollLayout, self).__init__(m.scrollLayout, *args, **kwargs)
        self.defaultValueGlobal = (0, 0)

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.ScrollValues, self.query('scrollAreaValue'))

    def data2CtrlProcedure(self):
        currentScrollDown, currentScrollRight = self.query('scrollAreaValue')
        prefValue = self.getAttr(Attr.ScrollValues)
        self.edit('scrollByPixel', ('up', currentScrollDown))
        self.edit('scrollByPixel', ('left', currentScrollRight))
        self.edit('scrollByPixel', ('down', prefValue[0]))
        self.edit('scrollByPixel', ('right', prefValue[1]))


class MCtrlTextScrollList(MCtrlBase):

    def __init__(self, *args, **kwargs):
        super(MCtrlTextScrollList, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = ()

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.SelectedIndexes, self.query('selectIndexedItem') or [])

    def data2CtrlProcedure(self):
        self.edit('deselectAll', True)
        selectedIndexes = self.getAttr(Attr.SelectedIndexes)
        if not selectedIndexes:
            return
        # in case of invalid index. iconTextScrollList does not have a flag for getting number of items,
        # so I cannot check a validity of index.
        try:
            self.edit('selectIndexedItem', list(selectedIndexes))
        except RuntimeError:
            pass


class MCtrlScriptTable(MCtrlBase):

    def __init__(self, *args, **kwargs):
        super(MCtrlScriptTable, self).__init__(m.scriptTable, *args, **kwargs)
        self.defaultValueGlobal = (0, 0)

    def ctrl2DataProcedure(self):
        controlData = self.query('selectedCells')
        self.setAttr(Attr.SelectedIndexes, [0, 0] if controlData is None else controlData)

    def data2CtrlProcedure(self):
        self.edit('selectedCells', list(self.getAttr(Attr.SelectedIndexes)))


def _simple(cmd, flag, globalDefault):
    return partial(MCtrlQueryEdit, cmd, flag, globalDefault)


constructors = {
    UIType.MCheckBox: _simple(m.checkBox, 'value', False),
    UIType.MCheckBoxGrp1: partial(MCtrlGrp4Simple, m.checkBoxGrp, [False], 1),
    UIType.MCheckBoxGrp2: partial(MCtrlGrp4Simple, m.checkBoxGrp, [False, False], 2),
    UIType.MCheckBoxGrp3: partial(MCtrlGrp4Simple, m.checkBoxGrp, [False, False, False], 3),
    UIType.MCheckBoxGrp4: partial(MCtrlGrp4Simple, m.checkBoxGrp, [False, False, False, False], 4),
    UIType.MColorSliderGrp: MCtrlColorSliderGrp,
    UIType.MFloatField: _simple(m.floatField, 'value', 0),
    UIType.MFloatFieldGrp1: partial(MCtrlGrp4Simple, m.floatFieldGrp, [0], 1),
    UIType.MFloatFieldGrp2: partial(MCtrlGrp4Simple, m.floatFieldGrp, [0, 0], 2),
    UIType.MFloatFieldGrp3: partial(MCtrlGrp4Simple, m.floatFieldGrp, [0, 0, 0], 3),
    UIType.MFloatFieldGrp4: partial(MCtrlGrp4Simple, m.floatFieldGrp, [0, 0, 0, 0], 4),
    UIType.MFloatScrollBar: _simple(m.floatScrollBar, 'value', 0),
    UIType.MFloatSlider: _simple(m.floatSlider, 'value', 0),
    UIType.MFloatSliderGrp: _simple(m.floatSliderGrp, 'value', 0),
    UIType.MFrameLayout: _simple(m.frameLayout, 'collapse', False),
    UIType.MIconTextCheckBox: _simple(m.iconTextCheckBox, 'value', False),
    UIType.MIconTextRadioButton: partial(MCtrlRadioButton, m.iconTextRadioButton),
    UIType.MIconTextScrollList: partial(MCtrlTextScrollList, m.iconTextScrollList),
    UIType.MIntField: _simple(m.intField, 'value', 0),
    UIType.MIntFieldGrp1: partial(MCtrlGrp4Simple, m.intFieldGrp, [0], 1),
    UIType.MIntFieldGrp2: partial(MCtrlGrp4Simple, m.intFieldGrp, [0, 0], 2),
    UIType.MIntFieldGrp3: partial(MCtrlGrp4Simple, m.intFieldGrp, [0, 0, 0], 3),
    UIType.MIntFieldGrp4: partial(MCtrlGrp4Simple, m.intFieldGrp, [0, 0, 0, 0], 4),
    UIType.MIntScrollBar: _simple(m.intScrollBar, 'value', 0),
    UIType.MIntSlider: _simple(m.intSlider, 'value', 0),
    UIType.MIntSliderGrp: _simple(m.intSliderGrp, 'value', 0),
    UIType.MOptionMenu: partial(MCtrlOptionMenu, m.optionMenu),
    UIType.MOptionMenuGrp: partial(MCtrlOptionMenuGrp, m.optionMenuGrp),
    UIType.MRadioButton: partial(MCtrlRadioButton, m.radioButton),
    UIType.MRadioButtonGrp1: _simple(m.radioButtonGrp, 'select', 1),
    UIType.MRadioButtonGrp2: _simple(m.radioButtonGrp, 'select', 1),
    UIType.MRadioButtonGrp3: _simple(m.radioButtonGrp, 'select', 1),
    UIType.MRadioButtonGrp4: _simple(m.radioButtonGrp, 'select', 1),
    UIType.MSymbolCheckBox: _simple(m.symbolCheckBox, 'value', False),
    UIType.MScriptTable: MCtrlScriptTable,
    UIType.MScrollField: _simple(m.scrollField, 'text', ''),
    UIType.MScrollLayout: MCtrlScrollLayout,
    UIType.MShelfTabLayout: partial(MCtrlTabLayout, m.shelfTabLayout),
    UIType.MTabLayout: partial(MCtrlTabLayout, m.tabLayout),
    UIType.MTextField: _simple(m.textField, 'text', ''),
    UIType.MTextFieldButtonGrp: _simple(m.textFieldButtonGrp, 'text', ''),
    UIType.MTextFieldGrp: _simple(m.textFieldGrp, 'text', ''),
    UIType.MTextScrollList: partial(MCtrlTextScrollList, m.textScrollList)
}


def getController(uiType, control, defaultValue):
    if uiType in constructors:
        return constructors[uiType](control, defaultValue)
    else:
        message('Cannot create controller: Unknown controller type: {0}.'.format(str(uiType)))
        return None
