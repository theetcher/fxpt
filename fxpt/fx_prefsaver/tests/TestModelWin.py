from PySide import QtGui, QtCore

import TestModelWinUI


class TestModelWin(QtGui.QMainWindow):

    def __init__(self):
        super(TestModelWin, self).__init__()
        self.ui = TestModelWinUI.Ui_MainWindow()
        self.ui.setupUi(self)

        self.model = self.createModel()

        # proxyModel = QtGui.QSortFilterProxyModel()
        # proxyModel.setSourceModel(model)

        self.ui.uiLSTV_test1.setModel(self.model)

        self.ui.uiTRV_test1.setModel(self.model)
        self.ui.uiTBLV_test1.setModel(self.model)
        self.ui.uiCOLV_test1.setModel(self.model)

        self.ui.uiTRV_test1.expandAll()

        # persIndexes = self.model.persistentIndexList()
        # self.log(str(persIndexes))

        self.dumpModel(self.model, self.model.invisibleRootItem().index(), '', '')
        # self.dumpModel(self.model, self.model.index(0, 0), '', '')
        # self.dumpModel(self.model, QtCore.QModelIndex(), '', '')

        # self.log(self.model.index(0, 0))
        # self.log(self.model.invisibleRootItem().index())

    def createModel(self):
        model = QtGui.QStandardItemModel()

        invisibleRoot = model.invisibleRootItem()

        folder1 = self.createItem('folder1')
        invisibleRoot.appendRow((folder1, self.createItem('value1')))
        folder11 = self.createItem('folder11')
        folder1.appendRow((folder11, self.createItem('value11')))
        folder11.appendRow((self.createItem('item111'), self.createItem('value111')))
        folder11.appendRow((self.createItem('item112'), self.createItem('value112')))
        folder11.appendRow((self.createItem('item113'), self.createItem('value113')))

        folder2 = self.createItem('folder2')

        testItem = self.createItem('value2')

        invisibleRoot.appendRow((folder2, testItem))
        folder21 = self.createItem('folder21')
        folder2.appendRow((folder21, self.createItem('value21')))
        folder21.appendRow((self.createItem('item211'), self.createItem('value211')))
        folder21.appendRow((self.createItem('item212'), self.createItem('value212')))
        folder21.appendRow((self.createItem('item213'), self.createItem('value213')))

        testItem.appendRow((self.createItem('TEST_item1'), self.createItem('TEST_item2')))

        folder3 = self.createItem('folder3')
        invisibleRoot.appendRow(folder3)
        folder31 = self.createItem('folder31')
        folder3.appendRow(folder31)
        folder31.appendRow(self.createItem('item311'))
        folder31.appendRow(self.createItem('item312'))
        folder31.appendRow(self.createItem('item313'))

        invisibleRoot.appendRow(self.createItem('rootItem1'))
        invisibleRoot.appendRow(self.createItem('rootItem2'))
        invisibleRoot.appendRow(self.createItem('rootItem3'))

        self.log(model.columnCount())

        return model

    # noinspection PyMethodMayBeStatic
    def createItem(self, text):
        return QtGui.QStandardItem(text)

    def dumpModel(self, model, parentIndex, parentPath, s):

        # http://comments.gmane.org/gmane.comp.lib.qt.general/32583

        # for r in range(model.rowCount(parentIndex)):
        #     for c in range(model.columnCount(parentIndex)):
        #         index = model.index(r, c, parentIndex)
        #         self.log('{} ({},{}) {}'.format(s, index.row(), index.column(), index.data(QtCore.Qt.DisplayRole)))
        #     for c in range(model.columnCount(parentIndex)):
        #         index = model.index(r, c, parentIndex)
        #         self.dumpModel(model, index, s + '     ')

        for r in range(model.rowCount(parentIndex)):
            for c in range(model.columnCount(parentIndex)):
                childIndex = model.index(r, c, parentIndex)
                childPath = parentPath + '|{},{}'.format(childIndex.row(), childIndex.column())
                self.log('{} ({},{}) {} {}'.format(s, childIndex.row(), childIndex.column(), childPath, childIndex.data(QtCore.Qt.DisplayRole)))
                self.dumpModel(model, childIndex, childPath, s + '     ')

    def log(self, text):
        self.ui.uiTXT_output.appendPlainText(str(text))

    def onTreeViewItemClicked(self, index):
        self.log('')
        self.log('index -> ' + str(index))
        self.log('parent -> ' + str(index.parent()))
        # self.log('children -> ' + str(index.children()))
