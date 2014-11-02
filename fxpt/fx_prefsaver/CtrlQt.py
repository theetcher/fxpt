try:
    import PyQt4 as _PyQt4
except ImportError:
    _PyQt4 = None

try:
    import PySide as _PySide
except ImportError:
    _PySide = None

from PSTypes import UITypes
from com import message


# noinspection PyAttributeOutsideInit
class QtCtrlBase(object):

    def __init__(self, qt, control, defaultValue):
        self.qt = qt
        self.control = control
        self.controlName = str(control.objectName())
        self.defaultValue = defaultValue

    def ctrl2Dict(self, prefDict):
        raise NotImplementedError('Call to abstract method.')

    def dict2Ctrl(self, prefDict):
        raise NotImplementedError('Call to abstract method.')


class QtCtrlWindow(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlWindow, self).__init__(*args, **kwargs)

    def ctrl2Dict(self, prefDict):
        prefDict[self.controlName + '_X'] = self.control.x()
        prefDict[self.controlName + '_Y'] = self.control.y()
        prefDict[self.controlName + '_Width'] = self.control.width()
        prefDict[self.controlName + '_Height'] = self.control.height()

    def dict2Ctrl(self, prefDict):
        key = self.controlName + '_X'
        x = prefDict[key] if key in prefDict else self.defaultValue[0]
        key = self.controlName + '_Y'
        y = prefDict[key] if key in prefDict else self.defaultValue[1]
        key = self.controlName + '_Width'
        width = prefDict[key] if key in prefDict else self.defaultValue[2]
        key = self.controlName + '_Height'
        height = prefDict[key] if key in prefDict else self.defaultValue[3]
        self.control.move(x, y)
        self.control.resize(width, height)


class QtCtrlLineEdit(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlLineEdit, self).__init__(*args, **kwargs)

    def ctrl2Dict(self, prefDict):
        prefDict[self.controlName] = str(self.control.text())

    def dict2Ctrl(self, prefDict):
        text = prefDict[self.controlName] if self.controlName in prefDict else self.defaultValue
        self.control.setText(text)


class QtCtrlCheckBox(QtCtrlBase):

    #TODO: ask about differences in setCheckState() arg types (PyQt int ok, PySide int -> exception)

    def __init__(self, *args, **kwargs):
        super(QtCtrlCheckBox, self).__init__(*args, **kwargs)
        self.intToState = {
            0: self.qt.QtCore.Qt.Unchecked,
            1: self.qt.QtCore.Qt.PartiallyChecked,
            2: self.qt.QtCore.Qt.Checked,
        }
        self.stateToInt = dict((state, i) for i, state in self.intToState.items())

    def ctrl2Dict(self, prefDict):
        prefDict[self.controlName] = self.stateToInt[self.control.checkState()]

    def dict2Ctrl(self, prefDict):
        state = prefDict[self.controlName] if self.controlName in prefDict else self.defaultValue
        self.control.setCheckState(self.intToState[state])


class QtCtrlCheckButton(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlCheckButton, self).__init__(*args, **kwargs)

    def ctrl2Dict(self, prefDict):
        prefDict[self.controlName] = self.control.isChecked()

    def dict2Ctrl(self, prefDict):
        state = prefDict[self.controlName] if self.controlName in prefDict else self.defaultValue
        self.control.setChecked(state)


class QtCtrlComboBox(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlComboBox, self).__init__(*args, **kwargs)

    def ctrl2Dict(self, prefDict):
        prefDict[self.controlName] = self.control.currentIndex()

    def dict2Ctrl(self, prefDict):
        index = prefDict[self.controlName] if self.controlName in prefDict else self.defaultValue
        self.control.setCurrentIndex(index)


class QtCtrlComboBoxEditable(QtCtrlComboBox):

    def __init__(self, *args, **kwargs):
        super(QtCtrlComboBoxEditable, self).__init__(*args, **kwargs)

    def ctrl2Dict(self, prefDict):
        itemCount = self.control.count()
        if itemCount == 0:
            return

        prefDict[self.controlName + '_Count'] = itemCount
        for i in range(itemCount):
            prefDict[self.controlName + '_Item' + str(i)] = str(self.control.itemText(i))

        super(QtCtrlComboBoxEditable, self).ctrl2Dict(prefDict)

    def dict2Ctrl(self, prefDict):
        self.control.clear()

        if self.controlName + '_Count' in prefDict:

            itemCount = prefDict[self.controlName + '_Count']

            items = []
            for i in range(itemCount):
                itemDictName = self.controlName + '_Item' + str(i)
                if not itemDictName in prefDict:
                    break
                else:
                    items.append(prefDict[itemDictName])

            self.control.addItems(items)

        super(QtCtrlComboBoxEditable, self).dict2Ctrl(prefDict)


class QtCtrlSplitter(QtCtrlComboBox):

    def __init__(self, *args, **kwargs):
        super(QtCtrlSplitter, self).__init__(*args, **kwargs)

    def ctrl2Dict(self, prefDict):
        sizes = self.control.sizes()
        prefDict[self.controlName] = len(sizes)
        for i in range(len(sizes)):
            prefDict[self.controlName + '_Item' + str(i)] = sizes[i]

    def dict2Ctrl(self, prefDict):
        if self.controlName not in prefDict:
            self.control.setSizes(self.defaultValue)
            return

        itemCount = prefDict[self.controlName]
        sizes = []
        for i in range(itemCount):
            itemDictName = self.controlName + '_Item' + str(i)
            if itemDictName in prefDict:
                sizes.append(prefDict[itemDictName])
            else:
                sizes.append(200)

        self.control.setSizes(sizes)


class QtCtrlTableWidget(QtCtrlComboBox):

    def __init__(self, *args, **kwargs):
        super(QtCtrlTableWidget, self).__init__(*args, **kwargs)
        self.intToSortOrder = {
            0: self.qt.QtCore.Qt.AscendingOrder,
            1: self.qt.QtCore.Qt.DescendingOrder,
        }
        self.sortOrderToInt = dict((state, i) for i, state in self.intToSortOrder.items())

    # noinspection PyCallingNonCallable
    def ctrl2Dict(self, prefDict):

        horizontalHeader = self.control.horizontalHeader()
        sortedSection = horizontalHeader.sortIndicatorSection()
        sortingOrder = horizontalHeader.sortIndicatorOrder()
        prefDict[self.controlName + '_SortedSection'] = sortedSection
        prefDict[self.controlName + '_SortingOrder'] = self.sortOrderToInt[sortingOrder]

        selectionRanges = self.control.selectedRanges()
        if not selectionRanges:
            return
        rangesCount = len(selectionRanges)
        prefDict[self.controlName] = rangesCount

        for i in range(rangesCount):
            borderMappings = {
                'Top': selectionRanges[i].topRow,
                'Left': selectionRanges[i].leftColumn,
                'Bottom': selectionRanges[i].bottomRow,
                'Right': selectionRanges[i].rightColumn
            }
            for borderName in borderMappings:
                prefDict[self.controlName + '_SelRange' + str(i) + borderName] = borderMappings[borderName]()

    def dict2Ctrl(self, prefDict):
        self.control.clearSelection()

        for attribute in ('', '_SortedSection', '_SortingOrder'):
            if self.controlName + attribute not in prefDict:
                return

        sortedSection = prefDict[self.controlName + '_SortedSection']
        sortingOrder = prefDict[self.controlName + '_SortingOrder']
        self.control.sortByColumn(sortedSection, self.intToSortOrder[sortingOrder])

        rangesCount = prefDict[self.controlName]

        selectionRanges = []

        for i in range(rangesCount):
            rangeValues = []
            for borderName in ('Top', 'Left', 'Bottom', 'Right'):
                rangeDictName = self.controlName + '_SelRange' + str(i) + borderName
                if not rangeDictName in prefDict:
                    return
                else:
                    rangeValues.append(prefDict[rangeDictName])

            selectionRanges.append(self.qt.QtGui.QTableWidgetSelectionRange(*rangeValues))

        for selectionRange in selectionRanges:
            self.control.setRangeSelected(selectionRange, True)


class QtCtrlTreeWidget(QtCtrlComboBox):

    def __init__(self, *args, **kwargs):
        super(QtCtrlTreeWidget, self).__init__(*args, **kwargs)
        self.intToSortOrder = {
            0: self.qt.QtCore.Qt.AscendingOrder,
            1: self.qt.QtCore.Qt.DescendingOrder,
        }
        self.sortOrderToInt = dict((state, i) for i, state in self.intToSortOrder.items())

    # noinspection PyCallingNonCallable
    def ctrl2Dict(self, prefDict):

        horizontalHeader = self.control.header()
        sortedSection = horizontalHeader.sortIndicatorSection()
        sortingOrder = horizontalHeader.sortIndicatorOrder()
        prefDict[self.controlName + '_SortedSection'] = sortedSection
        prefDict[self.controlName + '_SortingOrder'] = self.sortOrderToInt[sortingOrder]

        selectionRanges = self.control.selectedRanges()
        if not selectionRanges:
            return
        rangesCount = len(selectionRanges)
        prefDict[self.controlName] = rangesCount

        for i in range(rangesCount):
            borderMappings = {
                'Top': selectionRanges[i].topRow,
                'Left': selectionRanges[i].leftColumn,
                'Bottom': selectionRanges[i].bottomRow,
                'Right': selectionRanges[i].rightColumn
            }
            for borderName in borderMappings:
                prefDict[self.controlName + '_SelRange' + str(i) + borderName] = borderMappings[borderName]()

    def dict2Ctrl(self, prefDict):
        self.control.clearSelection()

        for attribute in ('', '_SortedSection', '_SortingOrder'):
            if self.controlName + attribute not in prefDict:
                return

        sortedSection = prefDict[self.controlName + '_SortedSection']
        sortingOrder = prefDict[self.controlName + '_SortingOrder']
        self.control.sortByColumn(sortedSection, self.intToSortOrder[sortingOrder])

        rangesCount = prefDict[self.controlName]

        selectionRanges = []

        for i in range(rangesCount):
            rangeValues = []
            for borderName in ('Top', 'Left', 'Bottom', 'Right'):
                rangeDictName = self.controlName + '_SelRange' + str(i) + borderName
                if not rangeDictName in prefDict:
                    return
                else:
                    rangeValues.append(prefDict[rangeDictName])

            selectionRanges.append(self.qt.QtGui.QTableWidgetSelectionRange(*rangeValues))

        for selectionRange in selectionRanges:
            self.control.setRangeSelected(selectionRange, True)


constructors = {
    UITypes.PYQTWindow: QtCtrlWindow,
    UITypes.PYQTLineEdit: QtCtrlLineEdit,
    UITypes.PYQTCheckBox: QtCtrlCheckBox,
    UITypes.PYQTRadioButton: QtCtrlCheckButton,
    UITypes.PYQTCheckButton: QtCtrlCheckButton,
    UITypes.PYQTComboBox: QtCtrlComboBox,
    UITypes.PYQTComboBoxEditable: QtCtrlComboBoxEditable,
    UITypes.PYQTTabControl: QtCtrlComboBox,
    UITypes.PYQTSplitter: QtCtrlSplitter,
    UITypes.PYQTListWidget: QtCtrlBase,
    UITypes.PYQTTreeWidget: QtCtrlTreeWidget,
    UITypes.PYQTTableWidget: QtCtrlTableWidget,
    UITypes.PYQTListView: QtCtrlBase,
    UITypes.PYQTTreeView: QtCtrlBase,
    UITypes.PYQTTableView: QtCtrlBase,
    UITypes.PYQTColumnView: QtCtrlBase,

    UITypes.PYSIDEWindow: QtCtrlWindow,
    UITypes.PYSIDELineEdit: QtCtrlLineEdit,
    UITypes.PYSIDECheckBox: QtCtrlCheckBox,
    UITypes.PYSIDERadioButton: QtCtrlCheckButton,
    UITypes.PYSIDECheckButton: QtCtrlCheckButton,
    UITypes.PYSIDEComboBox: QtCtrlComboBox,
    UITypes.PYSIDEComboBoxEditable: QtCtrlComboBoxEditable,
    UITypes.PYSIDETabControl: QtCtrlComboBox,
    UITypes.PYSIDESplitter: QtCtrlSplitter,
    UITypes.PYSIDEListWidget: QtCtrlBase,
    UITypes.PYSIDETreeWidget: QtCtrlTreeWidget,
    UITypes.PYSIDETableWidget: QtCtrlTableWidget,
    UITypes.PYSIDEListView: QtCtrlBase,
    UITypes.PYSIDETreeView: QtCtrlBase,
    UITypes.PYSIDETableView: QtCtrlBase,
    UITypes.PYSIDEColumnView: QtCtrlBase,
}


# noinspection PyCallingNonCallable
def getController(uiType, control, defaultValue):

    if uiType in UITypes.TypesPYQT:
        if _PyQt4:
            return constructors[uiType](_PyQt4, control, defaultValue)
        else:
            message('Cannot create controller: PyQt is not available.')
            return

    if uiType in UITypes.TypesPYSIDE:
        if _PySide:
            return constructors[uiType](_PySide, control, defaultValue)
        else:
            message('Cannot create controller: PySide is not available.')
            return

