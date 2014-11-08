try:
    import PyQt4 as _PyQt4
except ImportError:
    _PyQt4 = None

try:
    import PySide as _PySide
except ImportError:
    _PySide = None

from CtrlBase import CtrlBase
from PSTypes import UIType, Attr
from com import message


#TODO: test if there is no model connected
#TODO: test if model is empty
#TODO: test views with another selection modes (select rows, etc.)


# noinspection PyAttributeOutsideInit
class QtCtrlBase(CtrlBase):

    def __init__(self, qt, control, defaultValue):
        super(QtCtrlBase, self).__init__(control, defaultValue)
        self.qt = qt

    def getControlName(self):
        return str(self.control.objectName())


class QtCtrlWindow(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlWindow, self).__init__(*args, **kwargs)

    def ctrl2Data(self):
        super(QtCtrlWindow, self).ctrl2Data()

        self.setAttr(Attr.WinX, self.control.x())
        self.setAttr(Attr.WinY, self.control.y())
        self.setAttr(Attr.WinWidth, self.control.width())
        self.setAttr(Attr.WinHeight, self.control.height())

    def data2Ctrl(self, prefData):
        super(QtCtrlWindow, self).data2Ctrl(prefData)

        prefValue = self.getAttr(Attr.WinX)
        x = prefValue if prefValue else self.defaultValue[0]
        prefValue = self.getAttr(Attr.WinY)
        y = prefValue if prefValue else self.defaultValue[1]
        prefValue = self.getAttr(Attr.WinWidth)
        width = prefValue if prefValue else self.defaultValue[2]
        prefValue = self.getAttr(Attr.WinHeight)
        height = prefValue if prefValue else self.defaultValue[3]

        self.control.move(x, y)
        self.control.resize(width, height)


class QtCtrlLineEdit(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlLineEdit, self).__init__(*args, **kwargs)

    def ctrl2Data(self):
        super(QtCtrlLineEdit, self).ctrl2Data()
        self.setAttr(Attr.Text, str(self.control.text()))
        return self.prefData

    def data2Ctrl(self, prefData):
        super(QtCtrlLineEdit, self).data2Ctrl(prefData)
        prefValue = self.getAttr(Attr.Text)
        self.control.setText(prefValue if prefValue else self.defaultValue)


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

    def ctrl2Data(self):
        super(QtCtrlCheckBox, self).ctrl2Data()
        self.setAttr(Attr.CheckState, self.stateToInt[self.control.checkState()])

    def data2Ctrl(self, prefData):
        super(QtCtrlCheckBox, self).data2Ctrl(prefData)
        prefValue = self.getAttr(Attr.CheckState)
        state = prefValue if prefValue else self.defaultValue
        self.control.setCheckState(self.intToState[state])


class QtCtrlCheckButton(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlCheckButton, self).__init__(*args, **kwargs)

    def ctrl2Data(self):
        super(QtCtrlCheckButton, self).ctrl2Data()
        self.setAttr(Attr.CheckState, self.control.isChecked())

    def data2Ctrl(self, prefData):
        super(QtCtrlCheckButton, self).data2Ctrl(prefData)
        prefValue = self.getAttr(Attr.CheckState)
        state = prefValue if prefValue else self.defaultValue
        self.control.setChecked(state)


class QtCtrlComboBox(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlComboBox, self).__init__(*args, **kwargs)

    def ctrl2Data(self):
        super(QtCtrlComboBox, self).ctrl2Data()
        self.setAttr(Attr.CurrentIndex, self.control.currentIndex())

    def data2Ctrl(self, prefData):
        super(QtCtrlComboBox, self).data2Ctrl(prefData)
        self.restoreItems()
        self.restoreCurrentIndex()

    def restoreCurrentIndex(self):
        prefValue = self.getAttr(Attr.CurrentIndex)
        index = prefValue if prefValue else self.defaultValue
        self.control.setCurrentIndex(index)

    def restoreItems(self):
        pass


class QtCtrlComboBoxEditable(QtCtrlComboBox):

    def __init__(self, *args, **kwargs):
        super(QtCtrlComboBoxEditable, self).__init__(*args, **kwargs)

    def ctrl2Data(self):
        super(QtCtrlComboBoxEditable, self).ctrl2Data()

        itemCount = self.control.count()
        if itemCount == 0:
            return

        self.setAttr(Attr.ItemsCount, itemCount)
        for i in range(itemCount):
            self.setAttr(Attr.Item + str(i), str(self.control.itemText(i)))

    def data2Ctrl(self, prefData):
        super(QtCtrlComboBoxEditable, self).data2Ctrl(prefData)

    def restoreItems(self):
        self.control.clear()

        itemsCount = self.getAttr(Attr.ItemsCount)
        if itemsCount:

            items = []
            for i in range(itemsCount):

                itemValue = self.getAttr(Attr.Item + str(i))
                if itemValue is not None:
                    items.append(itemValue)

            self.control.addItems(items)


class QtCtrlSplitter(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlSplitter, self).__init__(*args, **kwargs)

    def ctrl2Data(self):
        super(QtCtrlSplitter, self).ctrl2Data()
        self.setAttr(Attr.Sizes, ','.join([str(s) for s in self.control.sizes()]))

    def data2Ctrl(self, prefData):
        super(QtCtrlSplitter, self).data2Ctrl(prefData)
        prefValue = self.getAttr(Attr.Sizes)
        if prefValue:
            sizes = [int(s) for s in prefValue.split(',')]
            self.control.setSizes(sizes)
        else:
            self.control.setSizes(self.defaultValue)


class ColumnSorter(object):

    def __init__(self, ctrl, header):
        self.ctrl = ctrl
        self.header = header

        self.intToSortOrder = {
            0: ctrl.qt.QtCore.Qt.AscendingOrder,
            1: ctrl.qt.QtCore.Qt.DescendingOrder,
        }
        self.sortOrderToInt = dict((state, i) for i, state in self.intToSortOrder.items())

    def saveSorting(self):
        self.ctrl.setAttr(Attr.SortedSection, self.header.sortIndicatorSection())
        self.ctrl.setAttr(Attr.SortingOrder, self.sortOrderToInt[self.header.sortIndicatorOrder()])

    def loadSorting(self):
        sortedSection = self.ctrl.getAttr(Attr.SortedSection)
        sortingOrder = self.ctrl.getAttr(Attr.SortingOrder)
        if (sortedSection is not None) and (sortingOrder is not None):
            self.ctrl.control.sortByColumn(sortedSection, self.intToSortOrder[sortingOrder])


class RangeSelector(object):

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.selectionModel = self.ctrl.control.selectionModel()
        self.qt = self.ctrl.qt
        self.model = self.ctrl.control.model()

    def saveRanges(self):
        selectedRanges = []
        for sr in self.selectionModel.selection():
            selectedRanges.append(','.join((str(sr.top()), str(sr.left()), str(sr.bottom()), str(sr.right()))))
        self.ctrl.setAttr(Attr.SelectedRanges, ' '.join(selectedRanges))

    def loadRanges(self):
        itemSelection = self.qt.QtGui.QItemSelection()
        rangesPrefData = self.ctrl.getAttr(Attr.SelectedRanges)

        if rangesPrefData:
            for rangeStr in rangesPrefData.split():
                top, left, bottom, right = [int(x) for x in rangeStr.split(',')]
                topLeft = self.model.index(top, left)
                bottomRight = self.model.index(bottom, right)
                itemSelection.merge(self.qt.QtGui.QItemSelection(topLeft, bottomRight), self.qt.QtGui.QItemSelectionModel.SelectCurrent)

            self.selectionModel.select(itemSelection, self.ctrl.qt.QtGui.QItemSelectionModel.Select)


class TreeIndexSelector(object):

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.qt = self.ctrl.qt
        self.control = self.ctrl.control
        self.model = self.ctrl.control.model()
        self.selectionModel = self.ctrl.control.selectionModel()

        self.selectedItems = []
        self.expandedItems = []

    def processIndexChildren(self, parentIndex, parentPath):
        for r in xrange(self.model.rowCount(parentIndex)):
            for c in range(self.model.columnCount(parentIndex)):
                childIndex = self.model.index(r, c, parentIndex)
                childPath = parentPath + '|{},{}'.format(childIndex.row(), childIndex.column())

                if self.selectionModel.isSelected(childIndex):
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

    def saveData(self):
        self.selectedItems = []
        self.expandedItems = []
        self.processIndexChildren(self.getRootIndex(), '')
        self.ctrl.setAttr(Attr.SelectedIndexes, ' '.join(self.selectedItems))
        self.ctrl.setAttr(Attr.ExpandedIndexes, ' '.join(self.expandedItems))

    def loadData(self):
        self.control.clearSelection()
        self.control.collapseAll()

        # Simple select() for each of indexes with QItemSelectionModel.SelectCurrent does not work.
        # It only selects the last index (like QItemSelectionModel.Select).
        # So i need to construct QItemSelection and merge all indexes to it.
        # When i pass QItemSelection to select(), it works fine.
        indexesToSelect = []

        selectedIndexesPathsPrefValue = self.ctrl.getAttr(Attr.SelectedIndexes)
        if selectedIndexesPathsPrefValue:
            for indexPath in selectedIndexesPathsPrefValue.split():
                index = self.getIndexByPath(indexPath)
                if not index:
                    continue
                indexesToSelect.append(index)

        itemSelection = self.qt.QtGui.QItemSelection()
        for index in indexesToSelect:
            itemSelection.merge(self.qt.QtGui.QItemSelection(index, index), self.qt.QtGui.QItemSelectionModel.SelectCurrent)
        self.selectionModel.select(itemSelection, self.qt.QtGui.QItemSelectionModel.Select)

        expandedIndexesPathsPrefValue = self.ctrl.getAttr(Attr.ExpandedIndexes)
        if expandedIndexesPathsPrefValue:
            for indexPath in expandedIndexesPathsPrefValue.split():
                index = self.getIndexByPath(indexPath)
                if not index:
                    continue
                self.control.expand(self.getIndexByPath(indexPath))


class QtCtrlListView(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlListView, self).__init__(*args, **kwargs)
        self.rangeSelector = RangeSelector(self)

    def ctrl2Data(self):
        super(QtCtrlListView, self).ctrl2Data()
        self.rangeSelector.saveRanges()

    def data2Ctrl(self, prefData):
        super(QtCtrlListView, self).data2Ctrl(prefData)
        self.control.clearSelection()
        self.rangeSelector.loadRanges()


class QtCtrlTableView(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlTableView, self).__init__(*args, **kwargs)
        self.columnSorter = ColumnSorter(self, self.control.horizontalHeader())
        self.rangeSelector = RangeSelector(self)

    def ctrl2Data(self):
        super(QtCtrlTableView, self).ctrl2Data()
        self.columnSorter.saveSorting()
        self.rangeSelector.saveRanges()

    def data2Ctrl(self, prefData):
        super(QtCtrlTableView, self).data2Ctrl(prefData)
        self.control.clearSelection()
        self.columnSorter.loadSorting()
        self.rangeSelector.loadRanges()


class QtCtrlTreeView(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlTreeView, self).__init__(*args, **kwargs)
        self.columnSorter = ColumnSorter(self, self.control.header())
        self.treeIndexSelector = TreeIndexSelector(self)

    def ctrl2Data(self):
        super(QtCtrlTreeView, self).ctrl2Data()
        self.columnSorter.saveSorting()
        self.treeIndexSelector.saveData()

    def data2Ctrl(self, prefData):
        super(QtCtrlTreeView, self).data2Ctrl(prefData)
        self.control.clearSelection()
        self.control.collapseAll()
        self.columnSorter.loadSorting()
        self.treeIndexSelector.loadData()


constructors = {
    UIType.PYQTWindow: QtCtrlWindow,
    UIType.PYQTLineEdit: QtCtrlLineEdit,
    UIType.PYQTCheckBox: QtCtrlCheckBox,
    UIType.PYQTRadioButton: QtCtrlCheckButton,
    UIType.PYQTCheckButton: QtCtrlCheckButton,
    UIType.PYQTComboBox: QtCtrlComboBox,
    UIType.PYQTComboBoxEditable: QtCtrlComboBoxEditable,
    UIType.PYQTTabControl: QtCtrlComboBox,
    UIType.PYQTSplitter: QtCtrlSplitter,
    UIType.PYQTListWidget: QtCtrlListView,
    UIType.PYQTTableWidget: QtCtrlTableView,
    UIType.PYQTTreeWidget: QtCtrlTreeView,
    UIType.PYQTListView: QtCtrlListView,
    UIType.PYQTTableView: QtCtrlTableView,
    UIType.PYQTTreeView: QtCtrlTreeView,

    UIType.PYSIDEWindow: QtCtrlWindow,
    UIType.PYSIDELineEdit: QtCtrlLineEdit,
    UIType.PYSIDECheckBox: QtCtrlCheckBox,
    UIType.PYSIDERadioButton: QtCtrlCheckButton,
    UIType.PYSIDECheckButton: QtCtrlCheckButton,
    UIType.PYSIDEComboBox: QtCtrlComboBox,
    UIType.PYSIDEComboBoxEditable: QtCtrlComboBoxEditable,
    UIType.PYSIDETabControl: QtCtrlComboBox,
    UIType.PYSIDESplitter: QtCtrlSplitter,
    UIType.PYSIDEListWidget: QtCtrlListView,
    UIType.PYSIDETableWidget: QtCtrlTableView,
    UIType.PYSIDETreeWidget: QtCtrlTreeView,
    UIType.PYSIDEListView: QtCtrlListView,
    UIType.PYSIDETableView: QtCtrlTableView,
    UIType.PYSIDETreeView: QtCtrlTreeView
}


# noinspection PyCallingNonCallable
def getController(uiType, control, defaultValue):

    if uiType in UIType.TypesPYQT:
        if _PyQt4:
            return constructors[uiType](_PyQt4, control, defaultValue)
        else:
            message('Cannot create controller: PyQt is not available.')
            return

    if uiType in UIType.TypesPYSIDE:
        if _PySide:
            return constructors[uiType](_PySide, control, defaultValue)
        else:
            message('Cannot create controller: PySide is not available.')
            return

