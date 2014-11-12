import pymel.core.uitypes as pmui

from CtrlPyMel import getController as pmGetController
from PSTypes import UIType
from com import message

IDX_PM_TYPE = 0
IDX_PM_CLASS = 1

constructors = {
    UIType.MCheckBox: [UIType.PMCheckBox, pmui.CheckBox],
    UIType.MCheckBoxGrp1: [UIType.PMCheckBoxGrp1, pmui.CheckBoxGrp],
    UIType.MCheckBoxGrp2: [UIType.PMCheckBoxGrp2, pmui.CheckBoxGrp],
    UIType.MCheckBoxGrp3: [UIType.PMCheckBoxGrp3, pmui.CheckBoxGrp],
    UIType.MCheckBoxGrp4: [UIType.PMCheckBoxGrp4, pmui.CheckBoxGrp],
    UIType.MColorSliderGrp: [UIType.PMColorSliderGrp, pmui.ColorSliderGrp],
    UIType.MFloatField: [UIType.PMFloatField, pmui.FloatField],
    UIType.MFloatFieldGrp1: [UIType.PMFloatFieldGrp1, pmui.FloatFieldGrp],
    UIType.MFloatFieldGrp2: [UIType.PMFloatFieldGrp2, pmui.FloatFieldGrp],
    UIType.MFloatFieldGrp3: [UIType.PMFloatFieldGrp3, pmui.FloatFieldGrp],
    UIType.MFloatFieldGrp4: [UIType.PMFloatFieldGrp4, pmui.FloatFieldGrp],
    UIType.MFloatScrollBar: [UIType.PMFloatScrollBar, pmui.FloatScrollBar],
    UIType.MFloatSlider: [UIType.PMFloatSlider, pmui.FloatSlider],
    UIType.MFloatSliderGrp: [UIType.PMFloatSliderGrp, pmui.FloatSliderGrp],
    UIType.MFrameLayout: [UIType.PMFrameLayout, pmui.FrameLayout],
    UIType.MIconTextCheckBox: [UIType.PMIconTextCheckBox, pmui.IconTextCheckBox],
    UIType.MIconTextRadioButton: [UIType.PMIconTextRadioButton, pmui.IconTextRadioButton],
    UIType.MIconTextScrollList: [UIType.PMIconTextScrollList, pmui.IconTextScrollList],
    UIType.MIntField: [UIType.PMIntField, pmui.IntField],
    UIType.MIntFieldGrp1: [UIType.PMIntFieldGrp1, pmui.IntFieldGrp],
    UIType.MIntFieldGrp2: [UIType.PMIntFieldGrp2, pmui.IntFieldGrp],
    UIType.MIntFieldGrp3: [UIType.PMIntFieldGrp3, pmui.IntFieldGrp],
    UIType.MIntFieldGrp4: [UIType.PMIntFieldGrp4, pmui.IntFieldGrp],
    UIType.MIntScrollBar: [UIType.PMIntScrollBar, pmui.IntScrollBar],
    UIType.MIntSlider: [UIType.PMIntSlider, pmui.IntSlider],
    UIType.MIntSliderGrp: [UIType.PMIntSliderGrp, pmui.IntSliderGrp],
    UIType.MOptionMenu: [UIType.PMOptionMenu, pmui.OptionMenu],
    UIType.MOptionMenuGrp: [UIType.PMOptionMenuGrp, pmui.OptionMenuGrp],
    UIType.MRadioButton: [UIType.PMRadioButton, pmui.RadioButton],
    UIType.MRadioButtonGrp1: [UIType.PMRadioButtonGrp1, pmui.RadioButtonGrp],
    UIType.MRadioButtonGrp2: [UIType.PMRadioButtonGrp2, pmui.RadioButtonGrp],
    UIType.MRadioButtonGrp3: [UIType.PMRadioButtonGrp3, pmui.RadioButtonGrp],
    UIType.MRadioButtonGrp4: [UIType.PMRadioButtonGrp4, pmui.RadioButtonGrp],
    UIType.MSymbolCheckBox: [UIType.PMSymbolCheckBox, pmui.SymbolCheckBox],
    UIType.MScriptTable: [UIType.PMScriptTable, pmui.ScriptTable],
    UIType.MScrollField: [UIType.PMScrollField, pmui.ScrollField],
    UIType.MScrollLayout: [UIType.PMScrollLayout, pmui.ScrollLayout],
    UIType.MShelfTabLayout: [UIType.PMShelfTabLayout, pmui.ShelfTabLayout],
    UIType.MTabLayout: [UIType.PMTabLayout, pmui.TabLayout],
    UIType.MTextField: [UIType.PMTextField, pmui.TextField],
    UIType.MTextFieldButtonGrp: [UIType.PMTextFieldButtonGrp, pmui.TextFieldButtonGrp],
    UIType.MTextFieldGrp: [UIType.PMTextFieldGrp, pmui.TextFieldGrp],
    UIType.MTextScrollList: [UIType.PMTextScrollList, pmui.TextScrollList]
    
}


def getController(uiType, control, defaultValue):
    if uiType in UIType.TypesM:
        pmUiType = constructors[uiType][IDX_PM_TYPE]
        pmClass = constructors[uiType][IDX_PM_CLASS]
        return pmGetController(pmUiType, pmClass(control), defaultValue)
    else:
        message('Cannot create controller: Unknown controller type: {}.'.format(str(uiType)))
