"""
Utility for saving Qt or Maya controls values to file or Maya optionVars and restoring from it.
Also you can use it for saving and restoring variables.
Maya controls currently not implemented.

Usage:

    1. Create instance of PrefSaver for saving to file:
        self.prefSaver = PrefSaver.PrefSaverFile('preferences.cfg')
    or to Maya optionVars:
        self.prefSaver = PrefSaver.PrefSaverOptVars('MyCoolNewToolUI_')
    in the last case always supply meanful prefix for option var in PrefSaver constructor. This will prevent
    mixing your values with the existing ones with the same name

    2. Add some controls to PrefSaver, providing control itself, UI Type and default value:
        self.prefSaver.addControl(self, PrefSaver.UIType.QtWindow, (100, 100, 500, 500))
        self.prefSaver.addControl(self.lineEdit, PrefSaver.UIType.QtLineEdit, '')
        self.prefSaver.addControl(self.checkBox, PrefSaver.UIType.QtCheckBox, 0)
        self.prefSaver.addControl(self.radioButton, PrefSaver.UIType.QtRadioButton, 0)
        self.prefSaver.addControl(self.tabWidget, PrefSaver.UIType.QtTabControl, 0)
        self.prefSaver.addControl(self.pushButton, PrefSaver.UIType.QtButton, 0)
        self.prefSaver.addControl(self.comboBox, PrefSaver.UIType.QtComboBox, 0)

    3. After that you just need to use following PrefSaver methods:
        to load values from file/optVars and apply to controls
            self.prefSaver.loadPrefs()
        to save values from controls to file/optVars
            self.prefSaver.savePrefs()
        to reset control values to their defaults
            self.prefSaver.resetPrefs()

"""

#region imports
import os

# noinspection PyBroadException
try:
    import cPickle as pickle
except:
    import pickle

PyQtAvailable = False
MayaAvailable = False

try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    PyQtAvailable = True
except ImportError:
    pass

try:
    import maya.cmds as cmds
    import pymel.core as pm
    MayaAvailable = True
except ImportError:
    cmds = None
    pm = None

#from watch import *
#endregion


#----------------------------------------------------------------------------------------------------------------------
# CLASS: PrefSaverFile
# for saving control states to preference file
#----------------------------------------------------------------------------------------------------------------------
class PrefSaverFile(object):

    def __init__(self, filename):
        super(PrefSaverFile, self).__init__()
        self.filename = filename
        self.optVarPrefix = ''
        self.controls = []
        self.prefDict = {}

    # noinspection PyCallingNonCallable
    def addControl(self, control, uiType, defaultValue):
        if uiType in UIType.Constructors:
            self.controls.append(UIType.Constructors[uiType](control, defaultValue, self.optVarPrefix))
        else:
            raise Exception('Unsupported Control Type.')

    # noinspection PyCallingNonCallable
    def addVariable(self, name, getFromVarFunc, setToVarFunc, defaultValue):
        self.controls.append(UIType.Constructors[UIType.Variable](
            name, getFromVarFunc, setToVarFunc, defaultValue, self.optVarPrefix))

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
        for ctrlDesc in self.controls:
            ctrlDesc.ctrlToDict(self.prefDict)

    def applyPrefs(self):
        for ctrlDesc in self.controls:
            ctrlDesc.dictToCtrl(self.prefDict)

    # noinspection PyMethodMayBeStatic
    def messageBox(self, title='Error', text='', textInformative='', textDetailed='', icon=QMessageBox.Critical):
        if PyQtAvailable:
            dlg = QMessageBox()
            dlg.setWindowTitle(title)
            dlg.setText(text)
            dlg.setInformativeText(textInformative)
            dlg.setDetailedText(textDetailed)
            dlg.setIcon(icon)
            dlg.setFixedSize(800, 100)
            dlg.exec_()
        else:
            txt = '\n'
            txt += title + ': '
            txt += text + '\n'
            txt += textInformative + '\n'
            txt += textDetailed + '\n\n'
            print txt

    def pickleSave(self, obj, filename):
        try:
            f = open(filename, 'wb')
            try:
                pickle.dump(obj, f, -1)
            finally:
                f.close()
        except IOError as e:
            self.messageBox(
                text='Error writing file.',
                textInformative='Filename: ' + filename,
                textDetailed='Additional exception info:\n' + str(e))
            raise
        except Exception as e:
            self.messageBox(
                text='Unknown error occurred while saving the file.',
                textInformative='Filename: ' + filename,
                textDetailed='Additional exception info:\n' + str(e))
            raise

    def pickleLoad(self, filename):
        try:
            f = open(filename, 'rb')
            try:
                obj = pickle.load(f)
            finally:
                f.close()
        except IOError as e:
            self.messageBox(
                text='Error reading file.',
                textInformative='Filename: ' + filename,
                textDetailed='Additional exception info:\n' + str(e))
            raise
        except Exception as e:
            self.messageBox(
                text='Unknown error occurred while reading the file.',
                textInformative='Filename: ' + filename,
                textDetailed='Additional exception info:\n' + str(e))
            raise

        return obj


#----------------------------------------------------------------------------------------------------------------------
# CLASS: PrefSaverOptVars
# for saving control states to Maya optionVars
#----------------------------------------------------------------------------------------------------------------------
class PrefSaverOptVars(PrefSaverFile):

    def __init__(self, optVarPrefix):
        if not MayaAvailable:
            raise Exception("Maya modules is not imported.")
        super(PrefSaverOptVars, self).__init__(filename='')
        self.optVarPrefix = optVarPrefix

    def savePrefs(self):
        self.gatherPrefs()
        for key, value in self.prefDict.items():
            pm.env.optionVars[key] = value

    def loadPrefs(self):
        self.prefDict = dict(pm.env.optionVars)
        self.applyPrefs()

    def resetPrefs(self):
        self.prefDict = {}
        self.applyPrefs()


###################################
#          Variable Desc          #
###################################

#----------------------------------------------------------------------------------------------------------------------
# CLASS: VarDesc
#----------------------------------------------------------------------------------------------------------------------
class VarDesc(object):

    def __init__(self, name, getFromVarFunc, setToVarFunc, defaultValue, prefix):
        self.name = prefix + name
        self.getFromVarFunc = getFromVarFunc
        self.setToVarFunc = setToVarFunc
        self.defaultValue = defaultValue

    def ctrlToDict(self, prefDict):
        prefDict[self.name] = self.getFromVarFunc()

    def dictToCtrl(self, prefDict):
        if self.name in prefDict:
            self.setToVarFunc(prefDict[self.name])
        else:
            self.setToVarFunc(self.defaultValue)


#----------------------------------------------------------------------------------------------------------------------
# CLASS: VarDescOptVar
#----------------------------------------------------------------------------------------------------------------------
class VarDescOptVar(VarDesc):
    def __init__(self, name, getFromVarFunc, setToVarFunc, defaultValue, prefix):
        super(VarDescOptVar, self).__init__(name, getFromVarFunc, setToVarFunc, defaultValue, prefix)

    def ctrlToDict(self, prefDict):
        value = self.getFromVarFunc()
        if (isinstance(value, bool) or
                isinstance(value, int) or
                isinstance(value, float) or
                isinstance(value, str)):
            super(VarDescOptVar, self).ctrlToDict(prefDict)
        else:
            raise Exception('Cannot save variable with this datatype.')


######################################
#          Qt Control Descs          #
######################################

#----------------------------------------------------------------------------------------------------------------------
# CLASS: QtDescBase
#----------------------------------------------------------------------------------------------------------------------
class QtDescBase(object):

    def __init__(self, control, defaultValue, prefix):
        if not PyQtAvailable:
            raise Exception("PyQt is not imported.")
        self.control = control
        self.defaultValue = defaultValue
        self.name = prefix + str(control.objectName())

    def ctrlToDict(self, prefDict):
        raise NotImplementedError("Call to abstract method.")

    def dictToCtrl(self, prefDict):
        raise NotImplementedError("Call to abstract method.")


#----------------------------------------------------------------------------------------------------------------------
# CLASS: QtDescWindow
#----------------------------------------------------------------------------------------------------------------------
class QtDescWindow(QtDescBase):

    def __init__(self, control, defaultValue, prefix):
        super(QtDescWindow, self).__init__(control, defaultValue, prefix)

    def ctrlToDict(self, prefDict):
        prefDict[self.name + 'X'] = self.control.x()
        prefDict[self.name + 'Y'] = self.control.y()
        prefDict[self.name + 'Width'] = self.control.width()
        prefDict[self.name + 'Height'] = self.control.height()

    def dictToCtrl(self, prefDict):
        x = prefDict[self.name + 'X'] if self.name + 'X' in prefDict else self.defaultValue[0]
        y = prefDict[self.name + 'Y'] if self.name + 'Y' in prefDict else self.defaultValue[1]
        width = prefDict[self.name + 'Width'] if self.name + 'Width' in prefDict else self.defaultValue[2]
        height = prefDict[self.name + 'Height'] if self.name + 'Height' in prefDict else self.defaultValue[3]
        self.control.move(x, y)
        self.control.resize(width, height)


#----------------------------------------------------------------------------------------------------------------------
# CLASS: QtDescLineEdit
#----------------------------------------------------------------------------------------------------------------------
class QtDescLineEdit(QtDescBase):

    def __init__(self, control, defaultValue, prefix):
        super(QtDescLineEdit, self).__init__(control, defaultValue, prefix)

    def ctrlToDict(self, prefDict):
        prefDict[self.name] = str(self.control.text())

    def dictToCtrl(self, prefDict):
        text = prefDict[self.name] if self.name in prefDict else self.defaultValue
        self.control.setText(text)


#----------------------------------------------------------------------------------------------------------------------
# CLASS: QtDescCheckBox
#----------------------------------------------------------------------------------------------------------------------
class QtDescCheckBox(QtDescBase):

    def __init__(self, control, defaultValue, prefix):
        super(QtDescCheckBox, self).__init__(control, defaultValue, prefix)

    def ctrlToDict(self, prefDict):
        checkState = self.control.checkState()
        if checkState == Qt.Unchecked:
            state = 0
        elif checkState == Qt.Checked:
            state = 1
        else:
            state = 2
        prefDict[self.name] = state

    def dictToCtrl(self, prefDict):
        state = prefDict[self.name] if self.name in prefDict else self.defaultValue
        if state == 0:
            self.control.setCheckState(Qt.Unchecked)
        elif state == 1:
            self.control.setCheckState(Qt.Checked)
        else:
            self.control.setCheckState(Qt.PartiallyChecked)


#----------------------------------------------------------------------------------------------------------------------
# CLASS: QtDescRadioButton
#----------------------------------------------------------------------------------------------------------------------
class QtDescRadioButton(QtDescBase):

    def __init__(self, control, defaultValue, prefix):
        super(QtDescRadioButton, self).__init__(control, defaultValue, prefix)

    def ctrlToDict(self, prefDict):
        prefDict[self.name] = 1 if self.control.isChecked() else 0

    def dictToCtrl(self, prefDict):
        state = prefDict[self.name] if self.name in prefDict else self.defaultValue
        if state == 0:
            self.control.setChecked(False)
        else:
            self.control.setChecked(True)


#----------------------------------------------------------------------------------------------------------------------
# CLASS: QtDescButton
#----------------------------------------------------------------------------------------------------------------------
class QtDescButton(QtDescBase):

    def __init__(self, control, defaultValue, prefix):
        super(QtDescButton, self).__init__(control, defaultValue, prefix)

    def ctrlToDict(self, prefDict):
        prefDict[self.name] = 1 if self.control.isChecked() else 0

    def dictToCtrl(self, prefDict):
        state = prefDict[self.name] if self.name in prefDict else self.defaultValue
        if state == 0:
            self.control.setChecked(False)
        else:
            self.control.setChecked(True)


#----------------------------------------------------------------------------------------------------------------------
# CLASS: QtDescComboBox
#----------------------------------------------------------------------------------------------------------------------
class QtDescComboBox(QtDescBase):

    def __init__(self, control, defaultValue, prefix):
        super(QtDescComboBox, self).__init__(control, defaultValue, prefix)

    def ctrlToDict(self, prefDict):
        itemCount = self.control.count()
        if itemCount == 0:
            return
        prefDict[self.name + 'Count'] = itemCount
        prefDict[self.name + 'CurrentIndex'] = self.control.currentIndex()
        for i in range(itemCount):
            prefDict[self.name + 'Item' + str(i)] = str(self.control.itemText(i))

    def dictToCtrl(self, prefDict):
        if not ((self.name + 'Count' in prefDict) and (self.name + 'CurrentIndex' in prefDict)):
            return
        itemCount = prefDict[self.name + 'Count']
        currentIndex = prefDict[self.name + 'CurrentIndex']

        items = []
        for i in range(itemCount):
            itemDictName = self.name + 'Item' + str(i)
            if not itemDictName in prefDict:
                break
            else:
                items.append(prefDict[itemDictName])

        self.control.clear()
        self.control.addItems(items)
        self.control.setCurrentIndex(currentIndex)


#----------------------------------------------------------------------------------------------------------------------
# CLASS: QtDescComboBoxNoEdit
#----------------------------------------------------------------------------------------------------------------------
class QtDescComboBoxNoEdit(QtDescBase):

    def __init__(self, control, defaultValue, prefix):
        super(QtDescComboBoxNoEdit, self).__init__(control, defaultValue, prefix)

    def ctrlToDict(self, prefDict):
        prefDict[self.name + 'CurrentIndex'] = self.control.currentIndex()

    def dictToCtrl(self, prefDict):
        if (self.name + 'CurrentIndex') in prefDict:
            currentIndex = prefDict[self.name + 'CurrentIndex']
        else:
            currentIndex = self.defaultValue

        self.control.setCurrentIndex(currentIndex)


#----------------------------------------------------------------------------------------------------------------------
# CLASS: QtDescTabControl
#----------------------------------------------------------------------------------------------------------------------
class QtDescTabControl(QtDescBase):

    def __init__(self, control, defaultValue, prefix):
        super(QtDescTabControl, self).__init__(control, defaultValue, prefix)

    def ctrlToDict(self, prefDict):
        prefDict[self.name] = self.control.currentIndex()

    def dictToCtrl(self, prefDict):
        index = prefDict[self.name] if self.name in prefDict else self.defaultValue
        self.control.setCurrentIndex(index)


#----------------------------------------------------------------------------------------------------------------------
# CLASS: QtDescSplitter
#----------------------------------------------------------------------------------------------------------------------
class QtDescSplitter(QtDescBase):

    def __init__(self, control, defaultValue, prefix):
        super(QtDescSplitter, self).__init__(control, defaultValue, prefix)

    def ctrlToDict(self, prefDict):
        sizes = self.control.sizes()
        prefDict[self.name + 'SplitterElements'] = len(sizes)
        for i in range(len(sizes)):
            prefDict[self.name + 'SplitterItem' + str(i)] = sizes[i]

    def dictToCtrl(self, prefDict):
        if not (self.name + 'SplitterElements' in prefDict):
            self.control.setSizes(self.defaultValue)
            return

        itemCount = prefDict[self.name + 'SplitterElements']
        sizes = []
        for i in range(itemCount):
            itemDictName = self.name + 'SplitterItem' + str(i)
            if itemDictName in prefDict:
                sizes.append(prefDict[itemDictName])
            else:
                sizes.append(200)

        self.control.setSizes(sizes)


#----------------------------------------------------------------------------------------------------------------------
# CLASS: QtDescTableWidget
#----------------------------------------------------------------------------------------------------------------------
class QtDescTableWidget(QtDescBase):

    def __init__(self, control, defaultValue, prefix):
        super(QtDescTableWidget, self).__init__(control, defaultValue, prefix)

    # noinspection PyCallingNonCallable
    def ctrlToDict(self, prefDict):
        selectionRanges = self.control.selectedRanges()
        if not selectionRanges:
            return
        rangesCount = len(selectionRanges)
        prefDict[self.name + 'RangesCount'] = rangesCount

        for i in range(rangesCount):
            borderMappings = {
                'Top': selectionRanges[i].topRow,
                'Left': selectionRanges[i].leftColumn,
                'Bottom': selectionRanges[i].bottomRow,
                'Right': selectionRanges[i].rightColumn
            }
            for borderName in borderMappings:
                prefDict[self.name + 'SelRange' + str(i) + borderName] = borderMappings[borderName]()

    def dictToCtrl(self, prefDict):
        rangesCountName = self.name + 'RangesCount'
        if not (rangesCountName in prefDict):
            return
        else:
            rangesCount = prefDict[rangesCountName]

        selectionRanges = []

        for i in range(rangesCount):
            rangeValues = []
            for borderName in ('Top', 'Left', 'Bottom', 'Right'):
                rangeDictName = self.name + 'SelRange' + str(i) + borderName
                if not rangeDictName in prefDict:
                    return
                else:
                    rangeValues.append(prefDict[rangeDictName])

            selectionRanges.append(QTableWidgetSelectionRange(*rangeValues))

        # self.control.clearSelection()
        for selectionRange in selectionRanges:
            self.control.setRangeSelected(selectionRange, True)


#----------------------------------------------------------------------------------------------------------------------
# CLASS: UIType
#----------------------------------------------------------------------------------------------------------------------
class UIType(object):

    # Qt Types
    QtWindow = 1
    QtLineEdit = 2
    QtCheckBox = 3
    QtRadioButton = 4
    QtButton = 5
    QtComboBox = 6
    QtComboBoxNoEdit = 7
    QtTabControl = 8
    QtSplitter = 9
    QtTableWidget = 10

    # Maya Types
    MCheckBox = 101
    MCheckBoxGrp = 102
    MColorSliderGrp = 103
    MFloatField = 104
    MFloatFieldGrp = 105
    MFloatSlider = 106
    MFloatSliderGrp = 107
    MIconTextCheckBox = 108
    MIconTextRadioButton = 109
    MIconTextScrollList = 110
    MIntField = 111
    MIntFieldGrp = 112
    MIntSlider = 113
    MIntSliderGrp = 114
    MRadioButton = 115
    MRadioButtonGrp = 116
    MSymbolCheckBox = 117
    MTextField = 118
    MTextFieldButtonGrp = 119
    MTextFieldGrp = 120
    MTextScrollList = 121

    # Misc
    Variable = 201
    VariableOptVar = 202

    Constructors = {
        QtWindow: QtDescWindow,
        QtLineEdit: QtDescLineEdit,
        QtCheckBox: QtDescCheckBox,
        QtRadioButton: QtDescRadioButton,
        QtButton: QtDescButton,
        QtComboBox: QtDescComboBox,
        QtComboBoxNoEdit: QtDescComboBoxNoEdit,
        QtTabControl: QtDescTabControl,
        QtSplitter: QtDescSplitter,
        QtTableWidget: QtDescTableWidget,
        Variable: VarDesc,
        VariableOptVar: VarDescOptVar
    }

