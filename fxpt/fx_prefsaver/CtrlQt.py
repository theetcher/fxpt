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


class QtCtrlBase(CtrlBase):

    def __init__(self, qt, control, defaultValue):
        super(QtCtrlBase, self).__init__(control, defaultValue)
        self.qt = qt

    def retrieveControlName(self):
        return str(self.control.objectName())


class QtCtrlCheckButton(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlCheckButton, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = False
        self.setupGetSetVars(Attr.CheckState, self.control.isChecked, self.control.setChecked)


class QtCtrlSpinBox(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlSpinBox, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = 0
        self.setupGetSetVars(Attr.Value, self.control.value, self.control.setValue)


class QtCtrlSplitter(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlSplitter, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = (200, 200)
        self.setupGetSetVars(Attr.Sizes, self.control.sizes, self.control.setSizes)


class QtCtrlTabWidget(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlTabWidget, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = 0
        self.setupGetSetVars(Attr.CurrentIndex, self.control.currentIndex, self.control.setCurrentIndex)


class QtCtrlStrGetter(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlStrGetter, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = ''

    def ctrl2DataProcedure(self):
        self.setAttr(self.attr, unicode(self.ctrlGetter()))


class QtCtrlLineEdit(QtCtrlStrGetter):

    def __init__(self, *args, **kwargs):
        super(QtCtrlLineEdit, self).__init__(*args, **kwargs)
        self.setupGetSetVars(Attr.Text, self.control.text, self.control.setText)


class QtCtrlTextEdit(QtCtrlStrGetter):

    def __init__(self, *args, **kwargs):
        super(QtCtrlTextEdit, self).__init__(*args, **kwargs)
        self.setupGetSetVars(Attr.Text, self.control.toHtml, self.control.setHtml)


class QtCtrlPlainTextEdit(QtCtrlStrGetter):

    def __init__(self, *args, **kwargs):
        super(QtCtrlPlainTextEdit, self).__init__(*args, **kwargs)
        self.setupGetSetVars(Attr.Text, self.control.toPlainText, self.control.setPlainText)


# noinspection PyAttributeOutsideInit
class QtCtrlDateTimeBase(QtCtrlBase):

    dateTimeFormat = None

    def __init__(self, *args, **kwargs):
        super(QtCtrlDateTimeBase, self).__init__(*args, **kwargs)

    def setupVars(self, dateTimeObjGetter, setter, dateTimeClass, globalDefault):
        self.dateTimeObjGetter = dateTimeObjGetter
        self.setter = setter
        self.dateTimeClass = dateTimeClass
        self.defaultValueGlobal = globalDefault

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.Value, str(self.dateTimeObjGetter().toString(self.__class__.dateTimeFormat)))

    def data2CtrlProcedure(self):
        dateTime = self.getAttr(Attr.Value)
        if not isinstance(dateTime, self.dateTimeClass):
            dateTime = self.dateTimeClass.fromString(dateTime, self.__class__.dateTimeFormat)
        self.setter(dateTime)


class QtCtrlTimeEdit(QtCtrlDateTimeBase):

    dateTimeFormat = 'HH:mm:ss.zzz'

    def __init__(self, *args, **kwargs):
        super(QtCtrlTimeEdit, self).__init__(*args, **kwargs)
        self.setupVars(self.control.time, self.control.setTime, self.qt.QtCore.QTime, self.qt.QtCore.QTime.currentTime())


class QtCtrlDateEdit(QtCtrlDateTimeBase):

    dateTimeFormat = 'yyyy.MM.dd'

    def __init__(self, *args, **kwargs):
        super(QtCtrlDateEdit, self).__init__(*args, **kwargs)
        self.setupVars(self.control.date, self.control.setDate, self.qt.QtCore.QDate, self.qt.QtCore.QDate.currentDate())


class QtCtrlDateTimeEdit(QtCtrlDateTimeBase):

    dateTimeFormat = '{} {}'.format(QtCtrlDateEdit.dateTimeFormat, QtCtrlTimeEdit.dateTimeFormat)

    def __init__(self, *args, **kwargs):
        super(QtCtrlDateTimeEdit, self).__init__(*args, **kwargs)
        self.setupVars(self.control.dateTime, self.control.setDateTime, self.qt.QtCore.QDateTime, self.qt.QtCore.QDateTime.currentDateTime())


class QtCtrlWindow(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlWindow, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = (200, 200, 600, 400)

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.WinGeom, [self.control.x(), self.control.y(), self.control.width(), self.control.height()])

    def data2CtrlProcedure(self):
        x, y, width, height = self.getAttr(Attr.WinGeom)
        self.control.move(x, y)
        self.control.resize(width, height)


class QtCtrlCheckBox(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlCheckBox, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = self.qt.QtCore.Qt.Unchecked

        self.intToState = {
            0: self.qt.QtCore.Qt.Unchecked,
            1: self.qt.QtCore.Qt.PartiallyChecked,
            2: self.qt.QtCore.Qt.Checked,
        }
        self.stateToInt = dict((state, i) for i, state in self.intToState.items())

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.Value, self.stateToInt[self.control.checkState()])

    def data2CtrlProcedure(self):
        self.control.setCheckState(self.intToState[self.getAttr(Attr.Value)])


class QtCtrlComboBox(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlComboBox, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = -1

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.CurrentIndex, self.control.currentIndex())

    def data2CtrlProcedure(self):
        self.restoreItems()
        self.restoreCurrentIndex()

    def restoreCurrentIndex(self):
        self.control.setCurrentIndex(self.getAttr(Attr.CurrentIndex))

    def restoreItems(self):
        pass


class QtCtrlComboBoxEditable(QtCtrlComboBox):

    def __init__(self, *args, **kwargs):
        super(QtCtrlComboBoxEditable, self).__init__(*args, **kwargs)

    def ctrl2DataProcedure(self):
        super(QtCtrlComboBoxEditable, self).ctrl2DataProcedure()
        itemCount = self.control.count()
        if itemCount == 0:
            return
        self.setAttr(Attr.Items, [unicode(self.control.itemText(i)) for i in range(itemCount)])

    def data2CtrlProcedure(self):
        super(QtCtrlComboBoxEditable, self).data2CtrlProcedure()

    def restoreItems(self):
        self.control.clear()
        items = self.getAttr(Attr.Items, noDefault=True)
        if items is not None:
            itemsCount = len(items)
            if itemsCount:
                self.control.addItems(items)


# The same problem as below. PySide in Maya deletes scrollbar c++ objects so i cannot cache them in constructor.
class QtCtrlScrollArea(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlScrollArea, self).__init__(*args, **kwargs)
        self.defaultValueGlobal = (0, 0)

    def ctrl2DataProcedure(self):
        self.setAttr(Attr.Value, (self.control.horizontalScrollBar().value(), self.control.verticalScrollBar().value()))

    def data2CtrlProcedure(self):
        horScrollValue, verScrollValue = self.getAttr(Attr.Value)
        self.control.horizontalScrollBar().setValue(horScrollValue)
        self.control.verticalScrollBar().setValue(verScrollValue)


# Explanation about headerGetter in ColumnSorter and SelectorBase.getSelectionModel()
# The problem is ONLY in PySide in Maya. PyQt (both in Maya and standalone) and PySide standalone is working fine.
# When i leave a scope of a method, underlying C++ object are deleted for QHeaderView and QItemSelectionModel classes
# EVEN if i setup an instance variable for those objects (self.header or self.selectionModel).
# looks like its a bug and seems like these guys are talking about it:
# https://groups.google.com/d/msg/pyside/yJBsDdE9ngQ/8ITbSlFkVs0J
# So the easiest workaround is just asking for these instances if you need them, and not to store them.

class ColumnSorter(object):

    def __init__(self, ctrl, headerGetter):
        self.ctrl = ctrl
        self.headerGetter = headerGetter

        self.intToSortOrder = {
            0: ctrl.qt.QtCore.Qt.AscendingOrder,
            1: ctrl.qt.QtCore.Qt.DescendingOrder,
        }
        self.sortOrderToInt = dict((state, i) for i, state in self.intToSortOrder.items())

    def saveSorting(self):
        header = self.headerGetter()
        self.ctrl.setAttr(Attr.SortedSection, header.sortIndicatorSection())
        self.ctrl.setAttr(Attr.SortingOrder, self.sortOrderToInt[header.sortIndicatorOrder()])

    def loadSorting(self):
        sortedSection = self.ctrl.getAttr(Attr.SortedSection)
        sortingOrder = self.ctrl.getAttr(Attr.SortingOrder)
        if (sortedSection is not None) and (sortingOrder is not None):
            self.ctrl.control.sortByColumn(sortedSection, self.intToSortOrder[sortingOrder])


class SelectorBase(object):

    def __init__(self, ctrl):
        self.ctrl = ctrl
        self.qt = self.ctrl.qt

    def getSelectionModel(self):
        return self.ctrl.control.selectionModel()

    def getModel(self):
        return self.ctrl.control.model()


class RangeSelector(SelectorBase):

    def __init__(self, ctrl):
        super(RangeSelector, self).__init__(ctrl)

    def saveRanges(self):
        selectionModel = self.getSelectionModel()
        if selectionModel is None:
            return

        selectedRanges = []
        for sr in selectionModel.selection():
            selectedRanges.append(','.join((str(sr.top()), str(sr.left()), str(sr.bottom()), str(sr.right()))))
        self.ctrl.setAttr(Attr.SelectedRanges, ' '.join(selectedRanges))

    def loadRanges(self):
        model = self.getModel()
        if model is None:
            return

        selectionModel = self.getSelectionModel()
        if selectionModel is None:
            return

        itemSelection = self.qt.QtGui.QItemSelection()
        rangesPrefData = self.ctrl.getAttr(Attr.SelectedRanges)

        if rangesPrefData:
            for rangeStr in rangesPrefData.split():
                top, left, bottom, right = [int(x) for x in rangeStr.split(',')]
                topLeft = model.index(top, left)
                bottomRight = model.index(bottom, right)
                itemSelection.merge(self.qt.QtGui.QItemSelection(topLeft, bottomRight), self.qt.QtGui.QItemSelectionModel.SelectCurrent)

            selectionModel.select(itemSelection, self.ctrl.qt.QtGui.QItemSelectionModel.Select)


class TreeIndexSelector(SelectorBase):

    def __init__(self, ctrl):
        super(TreeIndexSelector, self).__init__(ctrl)
        self.control = self.ctrl.control

        self.selectedItems = []
        self.expandedItems = []

    def processIndexChildren(self, parentIndex, parentPath):
        model = self.getModel()
        if model is None:
            return

        selectionModel = self.getSelectionModel()

        for r in xrange(model.rowCount(parentIndex)):
            for c in range(model.columnCount(parentIndex)):
                childIndex = model.index(r, c, parentIndex)
                childPath = parentPath + '|{},{}'.format(childIndex.row(), childIndex.column())

                if selectionModel.isSelected(childIndex):
                    self.selectedItems.append(childPath)
                if self.control.isExpanded(childIndex):
                    self.expandedItems.append(childPath)

                self.processIndexChildren(childIndex, childPath)

    def getIndexByPath(self, indexPath):
        model = self.getModel()
        if model is None:
            return

        parentIndex = self.getRootIndex()
        for indexStr in indexPath[1:].split('|'):
            row, column = [int(x) for x in indexStr.split(',')]
            childIndex = model.index(row, column, parentIndex)
            if not childIndex.isValid():
                return
            parentIndex = childIndex
        return parentIndex

    def getRootIndex(self):
        return self.control.rootIndex()

    def saveData(self):
        selectionModel = self.getSelectionModel()
        if selectionModel is None:
            return

        self.selectedItems = []
        self.expandedItems = []
        self.processIndexChildren(self.getRootIndex(), '')
        self.ctrl.setAttr(Attr.SelectedIndexes, ' '.join(self.selectedItems))
        self.ctrl.setAttr(Attr.ExpandedIndexes, ' '.join(self.expandedItems))

    def loadData(self):
        selectionModel = self.getSelectionModel()
        if selectionModel is None:
            return

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
        selectionModel.select(itemSelection, self.qt.QtGui.QItemSelectionModel.Select)

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

    def ctrl2DataProcedure(self):
        self.rangeSelector.saveRanges()

    def data2CtrlProcedure(self):
        self.control.clearSelection()
        self.rangeSelector.loadRanges()


class QtCtrlTableView(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlTableView, self).__init__(*args, **kwargs)
        self.columnSorter = ColumnSorter(self, self.control.horizontalHeader)
        self.rangeSelector = RangeSelector(self)

    def ctrl2DataProcedure(self):
        self.columnSorter.saveSorting()
        self.rangeSelector.saveRanges()

    def data2CtrlProcedure(self):
        self.control.clearSelection()
        self.columnSorter.loadSorting()
        self.rangeSelector.loadRanges()


class QtCtrlTreeView(QtCtrlBase):

    def __init__(self, *args, **kwargs):
        super(QtCtrlTreeView, self).__init__(*args, **kwargs)
        self.columnSorter = ColumnSorter(self, self.control.header)
        self.treeIndexSelector = TreeIndexSelector(self)

    def ctrl2DataProcedure(self):
        self.columnSorter.saveSorting()
        self.treeIndexSelector.saveData()

    def data2CtrlProcedure(self):
        self.control.clearSelection()
        self.control.collapseAll()
        self.columnSorter.loadSorting()
        self.treeIndexSelector.loadData()


constructors = {
    UIType.PYQTWindow: QtCtrlWindow,
    UIType.PYQTCheckBox: QtCtrlCheckBox,
    UIType.PYQTRadioButton: QtCtrlCheckButton,
    UIType.PYQTCheckButton: QtCtrlCheckButton,
    UIType.PYQTCheckAction: QtCtrlCheckButton,
    UIType.PYQTLineEdit: QtCtrlLineEdit,
    UIType.PYQTSpinBox: QtCtrlSpinBox,
    UIType.PYQTDoubleSpinBox: QtCtrlSpinBox,
    UIType.PYQTTimeEdit: QtCtrlTimeEdit,
    UIType.PYQTDateEdit: QtCtrlDateEdit,
    UIType.PYQTDateTimeEdit: QtCtrlDateTimeEdit,
    UIType.PYQTComboBox: QtCtrlComboBox,
    UIType.PYQTComboBoxEditable: QtCtrlComboBoxEditable,
    UIType.PYQTTabWidget: QtCtrlTabWidget,
    UIType.PYQTStackedWidget: QtCtrlTabWidget,
    UIType.PYQTToolBox: QtCtrlTabWidget,
    UIType.PYQTSplitter: QtCtrlSplitter,
    UIType.PYQTScrollBar: QtCtrlSpinBox,
    UIType.PYQTScrollArea: QtCtrlScrollArea,
    UIType.PYQTSlider: QtCtrlSpinBox,
    UIType.PYQTDial: QtCtrlSpinBox,
    UIType.PYQTTextEdit: QtCtrlTextEdit,
    UIType.PYQTPlainTextEdit: QtCtrlPlainTextEdit,
    UIType.PYQTListWidget: QtCtrlListView,
    UIType.PYQTTableWidget: QtCtrlTableView,
    UIType.PYQTTreeWidget: QtCtrlTreeView,
    UIType.PYQTListView: QtCtrlListView,
    UIType.PYQTTableView: QtCtrlTableView,
    UIType.PYQTTreeView: QtCtrlTreeView,

    UIType.PYSIDEWindow: QtCtrlWindow,
    UIType.PYSIDECheckBox: QtCtrlCheckBox,
    UIType.PYSIDERadioButton: QtCtrlCheckButton,
    UIType.PYSIDECheckButton: QtCtrlCheckButton,
    UIType.PYSIDECheckAction: QtCtrlCheckButton,
    UIType.PYSIDELineEdit: QtCtrlLineEdit,
    UIType.PYSIDESpinBox: QtCtrlSpinBox,
    UIType.PYSIDEDoubleSpinBox: QtCtrlSpinBox,
    UIType.PYSIDETimeEdit: QtCtrlTimeEdit,
    UIType.PYSIDEDateEdit: QtCtrlDateEdit,
    UIType.PYSIDEDateTimeEdit: QtCtrlDateTimeEdit,
    UIType.PYSIDEComboBox: QtCtrlComboBox,
    UIType.PYSIDEComboBoxEditable: QtCtrlComboBoxEditable,
    UIType.PYSIDETabWidget: QtCtrlTabWidget,
    UIType.PYSIDEStackedWidget: QtCtrlTabWidget,
    UIType.PYSIDEToolBox: QtCtrlTabWidget,
    UIType.PYSIDESplitter: QtCtrlSplitter,
    UIType.PYSIDEScrollBar: QtCtrlSpinBox,
    UIType.PYSIDEScrollArea: QtCtrlScrollArea,
    UIType.PYSIDESlider: QtCtrlSpinBox,
    UIType.PYSIDEDial: QtCtrlSpinBox,
    UIType.PYSIDETextEdit: QtCtrlTextEdit,
    UIType.PYSIDEPlainTextEdit: QtCtrlPlainTextEdit,
    UIType.PYSIDEListWidget: QtCtrlListView,
    UIType.PYSIDETableWidget: QtCtrlTableView,
    UIType.PYSIDETreeWidget: QtCtrlTreeView,
    UIType.PYSIDEListView: QtCtrlListView,
    UIType.PYSIDETableView: QtCtrlTableView,
    UIType.PYSIDETreeView: QtCtrlTreeView
}


# noinspection PyCallingNonCallable
def getController(uiType, control, defaultValue):

    if uiType in constructors:

        if UIType.isTypeOf(uiType, UIType.TypesPYQT):
            if _PyQt4:
                return constructors[uiType](_PyQt4, control, defaultValue)
            else:
                message('Cannot create controller: PyQt is not available.')
                return

        if UIType.isTypeOf(uiType, UIType.TypesPYSIDE):
            if _PySide:
                return constructors[uiType](_PySide, control, defaultValue)
            else:
                message('Cannot create controller: PySide is not available.')
                return

