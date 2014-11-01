# from PyQt4 import QtGui
import os

from fxpt.fx_prefsaver import PrefSaver

QtGui = None

CFG_FILENAME = os.path.dirname(__file__) + '/prefs.cfg'


# noinspection PyAttributeOutsideInit
class TestQtWindow(object):

    QtTypePyQt = 0
    QtTypePySide = 1

    # noinspection PyArgumentList
    def __init__(self, qtType, ser, parent=None):

        global QtGui
        if qtType == TestQtWindow.QtTypePyQt:
            from PyQt4 import QtGui
            import TestPyQtWindowUI
            self.ui = TestPyQtWindowUI.Ui_MainWindow()
        else:
            from PySide import QtGui
            import TestPySideWindowUI
            self.ui = TestPySideWindowUI.Ui_MainWindow()

        self.win = QtGui.QMainWindow(parent=parent)

        self.dlg = QtGui.QDialog(parent=self.win)
        self.dlg.setObjectName('uiDLG_testDialog')
        self.dlg.setWindowTitle(str(self.dlg))

        self.registerSlots()
        self.initPrefs(ser)
        self.ui.setupUi(self.win)

        self.win.setWindowTitle('{}; {}'.format(str(self.win), str(self.dlg)))

        self.fillListTreeColumnView()
        self.fillTableView()

        self.ui.uiTREW_test1.expandAll()
        self.ui.uiTREV_test1.expandAll()

    def fillListTreeColumnView(self):
        model = QtGui.QStandardItemModel()
        self.ui.uiTREV_test1.setModel(model)
        self.ui.uiLSTV_test1.setModel(model)
        self.ui.uiCOLV_test1.setModel(model)

        invisibleRoot = model.invisibleRootItem()

        folder1 = self.createItem('folder1')
        invisibleRoot.appendRow((folder1, self.createItem('value1')))
        folder11 = self.createItem('folder11')
        folder1.appendRow((folder11, self.createItem('value11')))
        folder11.appendRow((self.createItem('item111'), self.createItem('value111')))
        folder11.appendRow((self.createItem('item112'), self.createItem('value112')))
        folder11.appendRow((self.createItem('item113'), self.createItem('value113')))

        folder2 = self.createItem('folder2')
        invisibleRoot.appendRow((folder2, self.createItem('value2')))
        folder21 = self.createItem('folder21')
        folder2.appendRow((folder21, self.createItem('value21')))
        folder21.appendRow((self.createItem('item211'), self.createItem('value211')))
        folder21.appendRow((self.createItem('item212'), self.createItem('value212')))
        folder21.appendRow((self.createItem('item213'), self.createItem('value213')))

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

    def fillTableView(self):
        model = QtGui.QStandardItemModel(7, 2, self.ui.uiTBLV_test1)

        model.setItem(0, 0, self.createItem('value11'))
        model.setItem(0, 1, self.createItem('value12'))
        model.setItem(1, 0, self.createItem('value21'))
        model.setItem(1, 1, self.createItem('value22'))
        model.setItem(2, 0, self.createItem('value31'))
        model.setItem(2, 1, self.createItem('value32'))
        model.setItem(3, 0, self.createItem('value41'))
        model.setItem(3, 1, self.createItem('value42'))
        model.setItem(4, 0, self.createItem('value51'))
        model.setItem(4, 1, self.createItem('value52'))
        model.setItem(5, 0, self.createItem('value61'))
        model.setItem(5, 1, self.createItem('value62'))
        model.setItem(6, 0, self.createItem('value71'))
        model.setItem(6, 1, self.createItem('value72'))

        self.ui.uiTBLV_test1.setModel(model)

    # noinspection PyMethodMayBeStatic
    def createItem(self, text):
        return QtGui.QStandardItem(text)

    def fillColumnView(self):
        pass

    def registerSlots(self):
        self.win.onSavePrefsClicked = self.onSavePrefsClicked
        self.win.onLoadPrefsClicked = self.onLoadPrefsClicked
        self.win.onResetPrefsClicked = self.onResetPrefsClicked
        self.win.onShowDialogClicked = self.onShowDialogClicked

    def show(self):
        self.win.show()

    def raise_(self):
        self.win.raise_()

    # noinspection PyAttributeOutsideInit
    def initPrefs(self, ser):

        if ser == 'SerializerFilePickle':
            from fxpt.fx_prefsaver.SerializerFilePickle import SerializerFilePickle
            serializer = SerializerFilePickle(CFG_FILENAME)
        elif ser == 'SerializerOptVars':
            from fxpt.fx_prefsaver.SerializerOptVars import SerializerOptVars
            serializer = SerializerOptVars('TestQtWindow')
        else:
            assert False, 'Unknown serializer type'

        self.prefSaver = PrefSaver.PrefSaver(serializer)

        self.prefSaver.addControl(self.win, PrefSaver.UITypes.PYQTWindow, (200, 200, 900, 500))
        # self.prefSaver.addControl(self, PrefSaver.UITypes.PYSIDEWindow, (200, 200, 900, 500))
        # self.prefSaver.addControl(self.uiSPLmain, PrefSaver.UIType.QtSplitter, (600, 0))
        #
        # self.lastBrowsedFolder = DIR_SCENES_SRC
        #
        # def setLastBrowsedFolder(s):
        #     self.lastBrowsedFolder = s
        # self.prefSaver.addVariable('lastBrowsedFolder', lambda: self.lastBrowsedFolder, setLastBrowsedFolder, DIR_SCENES_SRC)

    def onSavePrefsClicked(self):
        # print 'onSavePrefsClicked()'
        self.prefSaver.savePrefs()

    def onLoadPrefsClicked(self):
        # print 'onLoadPrefsClicked()'
        self.prefSaver.loadPrefs()

    def onResetPrefsClicked(self):
        # print 'onResetPrefsClicked()'
        self.prefSaver.resetPrefs()

    def onShowDialogClicked(self):
        self.dlg.show()
