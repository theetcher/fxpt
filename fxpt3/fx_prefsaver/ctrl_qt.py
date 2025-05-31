from fxpt3.qt.pyside import *
from fxpt3.fx_prefsaver.ctrl_base import CtrlBase
from fxpt3.fx_prefsaver.pstypes import UIType, Attr
# from fxpt3.fx_prefsaver.com import message


class QtCtrlBase(CtrlBase):

    def __init__(self, control, defaultValue):
        super(QtCtrlBase, self).__init__(control, defaultValue)

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
        self.setAttr(self.attr, self.ctrlGetter())


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
        self.setupVars(self.control.time, self.control.setTime, QtCore.QTime, QtCore.QTime.currentTime())


class QtCtrlDateEdit(QtCtrlDateTimeBase):

    dateTimeFormat = 'yyyy.MM.dd'

    def __init__(self, *args, **kwargs):
        super(QtCtrlDateEdit, self).__init__(*args, **kwargs)
        self.setupVars(self.control.date, self.control.setDate, QtCore.QDate, QtCore.QDate.currentDate())


class QtCtrlDateTimeEdit(QtCtrlDateTimeBase):

    dateTimeFormat = '{0} {1}'.format(QtCtrlDateEdit.dateTimeFormat, QtCtrlTimeEdit.dateTimeFormat)

    def __init__(self, *args, **kwargs):
        super(QtCtrlDateTimeEdit, self).__init__(*args, **kwargs)
        self.setupVars(self.control.dateTime, self.control.setDateTime, QtCore.QDateTime, QtCore.QDateTime.currentDateTime())


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
        self.defaultValueGlobal = QtCore.Qt.CheckState.Unchecked

    def ctrl2DataProcedure(self):
        state = self.control.checkState()
        try:  # PySide6
            intValue = state.value
        except AttributeError:  # PySide2
            intValue = int(state)
        self.setAttr(Attr.Value, intValue)

    def data2CtrlProcedure(self):
        self.control.setCheckState(QtCore.Qt.CheckState(self.getAttr(Attr.Value)))


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
        self.setAttr(Attr.Items, [self.control.itemText(i) for i in range(itemCount)])

    def data2CtrlProcedure(self):
        super(QtCtrlComboBoxEditable, self).data2CtrlProcedure()

    def restoreItems(self):
        self.control.clear()
        items = self.getAttr(Attr.Items, noDefault=True)
        if items is not None:
            itemsCount = len(items)
            if itemsCount:
                self.control.addItems(items)


# The same problem as below. PySide in Maya deletes scrollbar c++ objects, so I cannot cache them in constructor.
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
# When I leave a scope of a method, underlying C++ object are deleted for QHeaderView and QItemSelectionModel classes
# EVEN if I set up an instance variable for those objects (self.header or self.selectionModel).
# looks like it's a bug and seems like these guys are talking about it:
# https://groups.google.com/d/msg/pyside/yJBsDdE9ngQ/8ITbSlFkVs0J
# So the easiest workaround is just asking for these instances if you need them, and not to store them.

class ColumnSorter(object):

    def __init__(self, ctrl, headerGetter):
        self.ctrl = ctrl
        self.headerGetter = headerGetter

        self.intToSortOrder = {
            0: QtCore.Qt.SortOrder.AscendingOrder,
            1: QtCore.Qt.SortOrder.DescendingOrder,
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

        itemSelection = QtCore.QItemSelection()
        rangesPrefData = self.ctrl.getAttr(Attr.SelectedRanges)

        if rangesPrefData:
            for rangeStr in rangesPrefData.split():
                top, left, bottom, right = [int(x) for x in rangeStr.split(',')]
                topLeft = model.index(top, left)
                bottomRight = model.index(bottom, right)
                itemSelection.merge(QtCore.QItemSelection(topLeft, bottomRight), QtCore.QItemSelectionModel.SelectionFlag.SelectCurrent)

            selectionModel.select(itemSelection, QtCore.QItemSelectionModel.SelectionFlag.Select)


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

        for r in range(model.rowCount(parentIndex)):
            for c in range(model.columnCount(parentIndex)):
                childIndex = model.index(r, c, parentIndex)
                childPath = parentPath + '|{0},{1}'.format(childIndex.row(), childIndex.column())

                if selectionModel.isSelected(childIndex):
                    self.selectedItems.append(childPath)
                if self.control.isExpanded(childIndex):
                    self.expandedItems.append(childPath)

                self.processIndexChildren(childIndex, childPath)

    def getIndexByPath(self, indexPath):
        model = self.getModel()
        if model is None:
            return None

        parentIndex = self.getRootIndex()
        for indexStr in indexPath[1:].split('|'):
            row, column = [int(x) for x in indexStr.split(',')]
            childIndex = model.index(row, column, parentIndex)
            if not childIndex.isValid():
                return None
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
        # So I need to construct QItemSelection and merge all indexes to it.
        # When I pass QItemSelection to select(), it works fine.
        indexesToSelect = []

        selectedIndexesPathsPrefValue = self.ctrl.getAttr(Attr.SelectedIndexes)
        if selectedIndexesPathsPrefValue:
            for indexPath in selectedIndexesPathsPrefValue.split():
                index = self.getIndexByPath(indexPath)
                if not index:
                    continue
                indexesToSelect.append(index)

        itemSelection = QtCore.QItemSelection()
        for index in indexesToSelect:
            itemSelection.merge(QtCore.QItemSelection(index, index), QtCore.QItemSelectionModel.SelectionFlag.SelectCurrent)
        selectionModel.select(itemSelection, QtCore.QItemSelectionModel.SelectionFlag.Select)

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
    UIType.PYQTGroupBox: QtCtrlCheckButton,
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
    UIType.PYSIDEGroupBox: QtCtrlCheckButton,
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
        return constructors[uiType](control, defaultValue)
    else:
        raise RuntimeError('Cannot create controller: Unknown UI Type.')

