"""
PrefSaver simplifies your process of saving UI component's various states (control values, selected items,
collapse states for Tree controls, active tabs for Tab controls and so on) and serializing them to different
destinations (binary files, json text files, Maya optionVars).
It is suitable for standalone applications and for apps run within Maya.

Currently supported UI frameworks are:
    PyQt,
    PySide,
    Maya PyMel UI,
    Maya UI

Typical usage:

1. Create a serializer:
    from fxpt.fx_prefsaver import Serializers
    mySerializer = Serializers.SerializerFileJson('path/to/pref/file/prefs.cfg')

2. Create PrefSaver instance:
    from fxpt.fx_prefsaver import PrefSaver
    myPrefSaver = PrefSaver.PrefSaver(mySerializer)

3. Add some controls to PrefSaver providing their types and OPTIONAL default value:
    myPrefSaver.addControl(myPyQtLineEdit, PrefSaver.UIType.PYQTLineEdit)
    myPrefSaver.addControl(myPySideCheckBox, PrefSaver.UIType.PYSIDECheckBox, QtCore.Qt.Unchecked)
    myPrefSaver.addControl(myPyMelFloatField, PrefSaver.UIType.PMFloatField, 4.568)
    myPrefSaver.addControl(myMayaCheckBoxGroup2, PrefSaver.UIType.MCheckBoxGrp2, [False, False])

4. Also you can add a variable instead of control.
   You will need to provide variable name, getter callable, setter callable and default value:
        def variableGetter():
            return myVariable
        def variableSetter(arg):
            myVariable = arg
        myPrefSaver.addVariable('myVariable', variableGetter, variableSetter, defaultVariableValue)

5. Use your PrefSaver:
    To save control states:
        myPrefSaver.savePrefs()
    To load control states:
        myPrefSaver.loadPrefs()
    To reset control states to defaults (even if you did not supply them - there are global defaults for each control):
        myPrefSaver.resetPrefs()

IMPORTANT NOTE #1:  When creating PyMel or Maya Controls always provide your own custom name. In that case
                    control name always be the same and will not change from run to run. For example:
                        myPyMelCheckBox = pymel.core.checkBox('myPyMelCheckBox', label='My PyMel Check Box')
                        myMelCheckBox = maya.cmds.checkBox('myMelCheckBox', label='My Mel Check Box')

                    When you create Qt controls BY CODE, also do not forget to setup control name:
                        myPyQtCheckBox = PyQt4.QtGui.QCheckBox()
                        myPyQtCheckBox.setObjectName('myPyQtCheckBox')
                        myPySideCheckBox = PySide.QtGui.QCheckBox()
                        myPySideCheckBox.setObjectName('myPySideCheckBox')

IMPORTANT NOTE #2:  Make sure that your control names are unique.


Available serializers:

    SerializerFilePickle('path/to/pref/file/prefs.cfg')
        serializes data to binary file using pickle

    SerializerFileJson('path/to/pref/file/prefs.cfg')
        serializes data to text JSON file

    SerializerOptVar('mayaOptionVarName')
        serializes data to Maya optionVar (available only within Maya)

Available control types and their acceptable defaults:

    PyQt Types:

        PYQTCheckAction -> bool
        PYQTCheckBox -> QtCore.Qt.CheckState
        PYQTCheckButton -> bool
        PYQTComboBox -> int: current item index (0-based)
        PYQTComboBoxEditable -> int: current item index (0-based)
        PYQTDateEdit -> str in format 'yyyy.MM.dd' or QDate object
        PYQTDateTimeEdit -> str in format 'yyyy.MM.dd HH:mm:ss.zzz' (24 hours) or QDateTime object
        PYQTDial -> int or float
        PYQTDoubleSpinBox -> int or float
        PYQTLineEdit -> str
        PYQTListView -> anything: no default value, ignored
        PYQTListWidget -> anything: no default value, ignored
        PYQTPlainTextEdit -> str
        PYQTRadioButton -> bool
        PYQTScrollArea -> [int, int]: tuple or list with horizontal and vertical scroll values
        PYQTScrollBar -> int
        PYQTSlider -> int or float
        PYQTSpinBox -> int or float
        PYQTSplitter -> [int, int, ...]: tuple or list with section sizes
        PYQTStackedWidget -> int: current widget index (0-based)
        PYQTTabWidget -> int: current tab index (0-based)
        PYQTTableView -> anything: no default value, ignored
        PYQTTableWidget -> anything: no default value, ignored
        PYQTTextEdit -> str
        PYQTTimeEdit -> str in format 'HH:mm:ss.zzz' (24 hours) or QTime object
        PYQTToolBox -> int: current tab index (0-based)
        PYQTTreeView -> anything: no default value, ignored
        PYQTTreeWidget -> anything: no default value, ignored
        PYQTWindow -> [int, int, int, int]: tuple or list with top and left corner coordinates, width and height

    PySide Types:

        PYSIDECheckAction -> bool
        PYSIDECheckBox -> QtCore.Qt.CheckState
        PYSIDECheckButton -> bool
        PYSIDEComboBox -> int: current item index (0-based)
        PYSIDEComboBoxEditable -> int: current item index (0-based)
        PYSIDEDateEdit -> str in format 'yyyy.MM.dd' or QDate object
        PYSIDEDateTimeEdit -> str in format 'yyyy.MM.dd HH:mm:ss.zzz' (24 hours) or QDateTime object
        PYSIDEDial -> int or float
        PYSIDEDoubleSpinBox -> int or float
        PYSIDELineEdit -> str
        PYSIDEListView -> anything: no default value, ignored
        PYSIDEListWidget -> anything: no default value, ignored
        PYSIDEPlainTextEdit -> str
        PYSIDERadioButton -> bool
        PYSIDEScrollArea -> [int, int]: tuple or list with horizontal and vertical scroll values
        PYSIDEScrollBar -> int
        PYSIDESlider -> int or float
        PYSIDESpinBox -> int or float
        PYSIDESplitter -> [int, int, ...]: tuple or list with section sizes
        PYSIDEStackedWidget -> int: current widget index (0-based)
        PYSIDETabWidget -> int: current tab index (0-based)
        PYSIDETableView -> anything: no default value, ignored
        PYSIDETableWidget -> anything: no default value, ignored
        PYSIDETextEdit -> str
        PYSIDETimeEdit -> str in format 'HH:mm:ss.zzz' (24 hours) or QTime object
        PYSIDEToolBox -> int: current tab index (0-based)
        PYSIDETreeView -> anything: no default value, ignored
        PYSIDETreeWidget -> anything: no default value, ignored
        PYSIDEWindow -> [int, int, int, int]: tuple or list with top and left corner coordinates, width and height

    Maya Types:

        MCheckBox -> bool
        MCheckBoxGrp1 -> [bool]: tuple or list
        MCheckBoxGrp2 -> [bool, bool]: tuple or list
        MCheckBoxGrp3 -> [bool, bool, bool]: tuple or list
        MCheckBoxGrp4 -> [bool, bool, bool, bool]: tuple or list
        MColorSliderGrp -> [float, float, float]: tuple or list with Red, Green and Blue values (0-1 range)
        MFloatField -> float
        MFloatFieldGrp1 -> [float]: tuple or list
        MFloatFieldGrp2 -> [float, float]: tuple or list
        MFloatFieldGrp3 -> [float, float, float]: tuple or list
        MFloatFieldGrp4 -> [float, float, float, float]: tuple or list
        MFloatScrollBar -> float
        MFloatSlider -> float
        MFloatSliderGrp -> float
        MFrameLayout -> bool: collapse state
        MIconTextCheckBox -> bool
        MIconTextRadioButton -> bool
        MIconTextScrollList -> [int, int, ...]: tuple or list with selected indexes
        MIntField -> int
        MIntFieldGrp1 -> [int]: tuple or list
        MIntFieldGrp2 -> [int, int]: tuple or list
        MIntFieldGrp3 -> [int, int, int]: tuple or list
        MIntFieldGrp4 -> [int, int, int, int]: tuple or list
        MIntScrollBar -> int
        MIntSlider -> int
        MIntSliderGrp -> int
        MOptionMenu -> int: current item index (1-based)
        MOptionMenuGrp -> int: current item index (1-based)
        MRadioButton -> bool
        MRadioButtonGrp1 -> int: current item index (1-based)
        MRadioButtonGrp2 -> int: current item index (1-based)
        MRadioButtonGrp3 -> int: current item index (1-based)
        MRadioButtonGrp4 -> int: current item index (1-based)
        MScriptTable -> anything: no default value, ignored
        MScrollField -> str
        MScrollLayout -> [int, int]: tuple or list with horizontal and vertical scroll values
        MShelfTabLayout -> int: current tab index (1-based)
        MSymbolCheckBox -> bool
        MTabLayout -> int: current tab index (1-based)
        MTextField -> str
        MTextFieldButtonGrp -> str
        MTextFieldGrp -> str
        MTextScrollList -> [int, int, ...]: tuple or list with selected indexes

    PyMel Types:

        PMCheckBox -> bool
        PMCheckBoxGrp1 -> [bool]: tuple or list
        PMCheckBoxGrp2 -> [bool, bool]: tuple or list
        PMCheckBoxGrp3 -> [bool, bool, bool]: tuple or list
        PMCheckBoxGrp4 -> [bool, bool, bool, bool]: tuple or list
        PMColorSliderGrp -> [float, float, float]: tuple or list with Red, Green and Blue values (0-1 range)
        PMFloatField -> float
        PMFloatFieldGrp1 -> [float]: tuple or list
        PMFloatFieldGrp2 -> [float, float]: tuple or list
        PMFloatFieldGrp3 -> [float, float, float]: tuple or list
        PMFloatFieldGrp4 -> [float, float, float, float]: tuple or list
        PMFloatScrollBar -> float
        PMFloatSlider -> float
        PMFloatSliderGrp -> float
        PMFrameLayout -> bool: collapse state
        PMIconTextCheckBox -> bool
        PMIconTextRadioButton -> bool
        PMIconTextScrollList -> [int, int, ...]: tuple or list with selected indexes
        PMIntField -> int
        PMIntFieldGrp1 -> [int]: tuple or list
        PMIntFieldGrp2 -> [int, int]: tuple or list
        PMIntFieldGrp3 -> [int, int, int]: tuple or list
        PMIntFieldGrp4 -> [int, int, int, int]: tuple or list
        PMIntScrollBar -> int
        PMIntSlider -> int
        PMIntSliderGrp -> int
        PMOptionMenu -> int: current item index (1-based)
        PMOptionMenuGrp -> int: current item index (1-based)
        PMRadioButton -> bool
        PMRadioButtonGrp1 -> int: current item index (1-based)
        PMRadioButtonGrp2 -> int: current item index (1-based)
        PMRadioButtonGrp3 -> int: current item index (1-based)
        PMRadioButtonGrp4 -> int: current item index (1-based)
        PMScriptTable -> anything: no default value, ignored
        PMScrollField -> str
        PMScrollLayout -> [int, int]: tuple or list with horizontal and vertical scroll values
        PMShelfTabLayout -> int: current tab index (1-based)
        PMSymbolCheckBox -> bool
        PMTabLayout -> int: current tab index (1-based)
        PMTextField -> str
        PMTextFieldButtonGrp -> str
        PMTextFieldGrp -> str
        PMTextScrollList -> [int, int, ...]: tuple or list with selected indexes
"""

#region imports

from PSTypes import UIType

import CtrlVar
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

#endregion


class PrefSaver(object):

    def __init__(self, serializer):
        super(PrefSaver, self).__init__()
        self.serializer = serializer
        self.controllers = []

    def addControl(self, control, uiType, defaultValue=None):

        if not UIType.isTypeOf(uiType, UIType.TypesAll):
            message('Cannot add unknown control type ({}) for {}. Skipped'.format(uiType, str(control)))
            return

        if UIType.isTypeOf(uiType, UIType.TypesPYQT | UIType.TypesPYSIDE):
            controller = CtrlQt.getController(uiType, control, defaultValue)
            if controller:
                self.controllers.append(controller)
            else:
                message('Failed to add controller (type={}) for {}'.format(uiType, str(control)))
            return

        if UIType.isTypeOf(uiType, UIType.TypesM):
            if CtrlMaya:
                self.controllers.append(CtrlMaya.getController(uiType, control, defaultValue))
            else:
                message('Failed to add controller (type={}) for {}'.format(uiType, str(control)))
            return

        if UIType.isTypeOf(uiType, UIType.TypesPM):
            if CtrlPyMel:
                self.controllers.append(CtrlPyMel.getController(uiType, control, defaultValue))
            else:
                message('Failed to add controller (type={}) for {}'.format(uiType, str(control)))
            return

        assert False, 'Failed to add a controller.'

    def addVariable(self, name, getter, setter, defaultValue):
        self.controllers.append(CtrlVar.CtrlVar(name, getter, setter, defaultValue))

    def savePrefs(self):
        self.serializer.save(self.gatherPrefs())

    def loadPrefs(self, control=None):
        self.applyPrefs(self.serializer.load(), control=control)

    def resetPrefs(self):
        self.applyPrefs({})

    def gatherPrefs(self):
        prefDataGlobal = {}
        for controller in self.controllers:
            controller.ctrl2Data()
            prefDataGlobal[controller.getControlName()] = controller.getPrefData()
        return prefDataGlobal

    def applyPrefs(self, prefDataGlobal, control=None):
        for controller in self.controllers:
            if control is None:
                controller.data2Ctrl(prefDataGlobal.get(controller.getControlName(), None))
            else:
                if controller.control == control:
                    controller.data2Ctrl(prefDataGlobal.get(controller.getControlName(), None))

