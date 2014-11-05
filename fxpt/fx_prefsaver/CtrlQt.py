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


#TODO: test if there is no model connected
#TODO: test if model is empty
#TODO: test views with another selection modes (select rows, etc.)
#TODO: check for attribute in dict -> separate procedure
#TODO!: attribute composer and getter/setter as separate module and class


def keyName(*args):
    return '_'.join(args)


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
        prefDict[keyName(self.controlName, 'x')] = self.control.x()
        prefDict[keyName(self.controlName, 'y')] = self.control.y()
        prefDict[keyName(self.controlName, 'width')] = self.control.width()
        prefDict[keyName(self.controlName, 'height')] = self.control.height()

    def dict2Ctrl(self, prefDict):
        key = self.controlName + '_x'
        x = prefDict[key] if key in prefDict else self.defaultValue[0]
        key = self.controlName + '_y'
        y = prefDict[key] if key in prefDict else self.defaultValue[1]
        key = self.controlName + '_width'
        width = prefDict[key] if key in prefDict else self.defaultValue[2]
        key = self.controlName + '_height'
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

        prefDict[self.controlName + '_count'] = itemCount
        for i in range(itemCount):
            prefDict[self.controlName + '_item' + str(i)] = str(self.control.itemText(i))

        super(QtCtrlComboBoxEditable, self).ctrl2Dict(prefDict)

    def dict2Ctrl(self, prefDict):
        self.control.clear()

        if self.controlName + '_count' in prefDict:
            itemCount = prefDict[self.controlName + '_count']

            items = []
            for i in range(itemCount):
                itemDictName = self.controlName + '_item' + str(i)
                if not itemDictName in prefDict:
                    continue
                else:
                    items.append(prefDict[itemDictName])

            self.control.addItems(items)

        super(QtCtrlComboBoxEditable, self).dict2Ctrl(prefDict)


class QtCtrlSplitter(QtCtrlBase):

    #TODO: save item sizes in one string.

    def __init__(self, *args, **kwargs):
        super(QtCtrlSplitter, self).__init__(*args, **kwargs)

    def ctrl2Dict(self, prefDict):
        sizes = self.control.sizes()
        prefDict[self.controlName] = len(sizes)
        for i in range(len(sizes)):
            prefDict[self.controlName + '_item' + str(i)] = sizes[i]

    def dict2Ctrl(self, prefDict):
        if self.controlName not in prefDict:
            self.control.setSizes(self.defaultValue)
            return

        itemCount = prefDict[self.controlName]
        sizes = []
        for i in range(itemCount):
            itemDictName = self.controlName + '_item' + str(i)
            if itemDictName in prefDict:
                sizes.append(prefDict[itemDictName])
            else:
                sizes.append(200)

        self.control.setSizes(sizes)


class ColumnSorter(object):

    def __init__(self, qt, control, header):
        self.control = control
        self.controlName = str(control.objectName())
        self.header = header

        self.intToSortOrder = {
            0: qt.QtCore.Qt.AscendingOrder,
            1: qt.QtCore.Qt.DescendingOrder,
        }
        self.sortOrderToInt = dict((state, i) for i, state in self.intToSortOrder.items())

    def saveSorting(self, prefDict):
        sortedSection = self.header.sortIndicatorSection()
        sortingOrder = self.header.sortIndicatorOrder()
        prefDict[self.controlName + '_sortedSection'] = sortedSection
        prefDict[self.controlName + '_sortingOrder'] = self.sortOrderToInt[sortingOrder]

    def loadSorting(self, prefDict):
        sortedSection = prefDict[self.controlName + '_sortedSection']
        sortingOrder = prefDict[self.controlName + '_sortingOrder']
        self.control.sortByColumn(sortedSection, self.intToSortOrder[sortingOrder])


class RangeSelector(object):

    def __init__(self, qt, control):
        self.qt = qt
        self.controlName = str(control.objectName())
        self.model = control.model()
        self.selectionModel = control.selectionModel()

    def saveRanges(self, prefDict):
        selectedRanges = []
        for sr in self.selectionModel.selection():
            selectedRanges.append(','.join((str(sr.top()), str(sr.left()), str(sr.bottom()), str(sr.right()))))
        prefDict[self.controlName + '_selectedRanges'] = ' '.join(selectedRanges)

    def loadRanges(self, prefDict):
        itemSelection = self.qt.QtGui.QItemSelection()
        for rangeStr in prefDict[self.controlName + '_selectedRanges'].split():
            top, left, bottom, right = [int(x) for x in rangeStr.split(',')]
            topLeft = self.model.index(top, left)
            bottomRight = self.model.index(bottom, right)
            itemSelection.merge(self.qt.QtGui.QItemSelection(topLeft, bottomRight), self.qt.QtGui.QItemSelectionModel.SelectCurrent)
        self.selectionModel.select(itemSelection, self.qt.QtGui.QItemSelectionModel.Select)


class QtCtrlListView(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlListView, self).__init__(*args, **kwargs)
        self.rangeSelector = RangeSelector(self.qt, self.control)

    def ctrl2Dict(self, prefDict):
        self.rangeSelector.saveRanges(prefDict)

    def dict2Ctrl(self, prefDict):
        self.control.clearSelection()

        for attribute in ('_selectedRanges',):
            if self.controlName + attribute not in prefDict:
                return

        self.rangeSelector.loadRanges(prefDict)


class QtCtrlTableView(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlTableView, self).__init__(*args, **kwargs)
        self.columnSorter = ColumnSorter(self.qt, self.control, self.control.horizontalHeader())
        self.rangeSelector = RangeSelector(self.qt, self.control)

    def ctrl2Dict(self, prefDict):
        self.columnSorter.saveSorting(prefDict)
        self.rangeSelector.saveRanges(prefDict)

    def dict2Ctrl(self, prefDict):
        self.control.clearSelection()

        for attribute in ('_sortedSection', '_sortingOrder', '_selectedRanges'):
            if self.controlName + attribute not in prefDict:
                return

        self.columnSorter.loadSorting(prefDict)
        self.rangeSelector.loadRanges(prefDict)


class QtCtrlTreeView(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlTreeView, self).__init__(*args, **kwargs)
        self.intToSortOrder = {
            0: self.qt.QtCore.Qt.AscendingOrder,
            1: self.qt.QtCore.Qt.DescendingOrder,
        }
        self.sortOrderToInt = dict((state, i) for i, state in self.intToSortOrder.items())

        self.model = self.control.model()
        self.itemSelectionModel = self.control.selectionModel()
        self.columnSorter = ColumnSorter(self.qt, self.control, self.control.header())

        self.selectedItems = []
        self.expandedItems = []

    def processIndexChildren(self, parentIndex, parentPath):
        for r in xrange(self.model.rowCount(parentIndex)):
            for c in range(self.model.columnCount(parentIndex)):
                childIndex = self.model.index(r, c, parentIndex)
                childPath = parentPath + '|{},{}'.format(childIndex.row(), childIndex.column())

                if self.itemSelectionModel.isSelected(childIndex):
                    self.selectedItems.append(childPath)
                if self.control.isExpanded(childIndex):
                    self.expandedItems.append(childPath)

                self.processIndexChildren(childIndex, childPath)

    def getIndexByPath(self, indexPath):
        parentIndex = self.getRootIndex()
        for indexStr in indexPath[1:].split('|'):
            row, column = [int(x) for x in indexStr.split(',')]
            childIndex = self.model.index(row, column, parentIndex)
            if not childIndex.isValid():
                return
            parentIndex = childIndex
        return parentIndex

    def getRootIndex(self):
        return self.control.rootIndex()

    def ctrl2Dict(self, prefDict):
        self.columnSorter.saveSorting(prefDict)

        self.selectedItems = []
        self.expandedItems = []
        self.processIndexChildren(self.getRootIndex(), '')

        prefDict[self.controlName + '_selectedItems'] = ' '.join(self.selectedItems)
        prefDict[self.controlName + '_expandedItems'] = ' '.join(self.expandedItems)

    def dict2Ctrl(self, prefDict):
        self.control.clearSelection()
        self.control.collapseAll()

        for attribute in ('_sortedSection', '_sortingOrder', '_selectedItems', '_expandedItems'):
            if self.controlName + attribute not in prefDict:
                return

        self.columnSorter.loadSorting(prefDict)

        # Simple select() with QItemSelectionModel.SelectCurrent for each of indexes does not work.
        # It only selects the last index (like QItemSelectionModel.Select).
        # So i need to construct QItemSelection and merge all indexes to it.
        # When i pass QItemSelection to select(), it works fine.
        indexesToSelect = []
        for indexPath in prefDict[self.controlName + '_selectedItems'].split():
            index = self.getIndexByPath(indexPath)
            if not index:
                continue
            indexesToSelect.append(index)

        itemSelection = self.qt.QtGui.QItemSelection()
        for index in indexesToSelect:
            itemSelection.merge(self.qt.QtGui.QItemSelection(index, index), self.qt.QtGui.QItemSelectionModel.SelectCurrent)
        self.itemSelectionModel.select(itemSelection, self.qt.QtGui.QItemSelectionModel.Select)

        for indexPath in prefDict[self.controlName + '_expandedItems'].split():
            index = self.getIndexByPath(indexPath)
            if not index:
                continue
            self.control.expand(self.getIndexByPath(indexPath))


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
    UITypes.PYQTListWidget: QtCtrlListView,
    UITypes.PYQTTableWidget: QtCtrlTableView,
    UITypes.PYQTTreeWidget: QtCtrlTreeView,
    UITypes.PYQTListView: QtCtrlListView,
    UITypes.PYQTTableView: QtCtrlTableView,
    UITypes.PYQTTreeView: QtCtrlTreeView,
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
    UITypes.PYSIDEListWidget: QtCtrlListView,
    UITypes.PYSIDETableWidget: QtCtrlTableView,
    UITypes.PYSIDETreeWidget: QtCtrlTreeView,
    UITypes.PYSIDEListView: QtCtrlListView,
    UITypes.PYSIDETableView: QtCtrlTableView,
    UITypes.PYSIDETreeView: QtCtrlTreeView,
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

