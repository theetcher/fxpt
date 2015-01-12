# from PyQt4 import QtGui
import os

from fxpt.fx_prefsaver import PrefSaver
from fxpt.fx_prefsaver.Serializers import SerializerOptVar, SerializerFileJson, SerializerFilePickle

QtGui = None
QtCore = None

CFG_FILENAME = os.path.dirname(__file__) + '\\prefs.cfg'


# noinspection PyAttributeOutsideInit
class TestQtWindow(object):

    QtTypePyQt = 0
    QtTypePySide = 1

    # noinspection PyArgumentList
    def __init__(self, qtType, ser, parent=None):

        self.qtType = qtType

        global QtCore
        global QtGui
        if self.qtType == TestQtWindow.QtTypePyQt:
            # noinspection PyUnresolvedReferences
            from PyQt4 import QtCore
            from PyQt4 import QtGui
            import TestPyQtWindowUI
            self.ui = TestPyQtWindowUI.Ui_MainWindow()
        else:
            # noinspection PyUnresolvedReferences
            from PySide import QtCore
            from PySide import QtGui
            import TestPySideWindowUI
            self.ui = TestPySideWindowUI.Ui_MainWindow()

        self.win = QtGui.QMainWindow(parent=parent)

        self.dlg = QtGui.QDialog(parent=self.win)
        self.dlg.setObjectName('uiDLG_testDialog')
        self.dlg.setWindowTitle(str(self.dlg))

        self.registerSlots()
        self.ui.setupUi(self.win)

        self.win.setWindowTitle('{0}; {1}'.format(str(self.win), str(self.dlg)))

        self.fillListTreeColumnView()
        self.fillTableView()

        self.ui.uiTREW_test1.expandAll()
        self.ui.uiTREV_test1.expandAll()

        self.prefSaver = PrefSaver.PrefSaver(self.createSerializer(ser))
        self.initPrefs()

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
        self.win.onStackedWidgetPageDec = self.onStackedWidgetPageDec
        self.win.onStackedWidgetPageInc = self.onStackedWidgetPageInc
        self.win.onSavePrefsClicked = self.onSavePrefsClicked
        self.win.onLoadPrefsClicked = self.onLoadPrefsClicked
        self.win.onResetPrefsClicked = self.onResetPrefsClicked
        self.win.onShowDialogClicked = self.onShowDialogClicked

    def show(self):
        self.win.show()

    def raise_(self):
        self.win.raise_()

    # noinspection PyMethodMayBeStatic
    def createSerializer(self, ser):
        if ser == 'SerializerFilePickle':
            return SerializerFilePickle(CFG_FILENAME)
        if ser == 'SerializerFileJson':
            return SerializerFileJson(CFG_FILENAME)
        elif ser == 'SerializerOptVar':
            return SerializerOptVar('TestQtWindow')
        else:
            assert False, 'Unknown serializer type'

    # noinspection PyAttributeOutsideInit
    def initPrefs(self, defaults=False):

        PyQtControls = [
            (self.win, PrefSaver.UIType.PYQTWindow, (200, 200, 900, 500)),
            (self.dlg, PrefSaver.UIType.PYQTWindow, (300, 300, 200, 200)),
            (self.ui.uiCHK_test1, PrefSaver.UIType.PYQTCheckBox, QtCore.Qt.Unchecked),
            (self.ui.uiCHK_testTri1, PrefSaver.UIType.PYQTCheckBox, QtCore.Qt.Unchecked),
            (self.ui.uiRAD_test1, PrefSaver.UIType.PYQTRadioButton, True),
            (self.ui.uiRAD_test2, PrefSaver.UIType.PYQTRadioButton, False),
            (self.ui.uiLED_test1, PrefSaver.UIType.PYQTLineEdit, 'defaultValue'),
            (self.ui.uiSPN_test1, PrefSaver.UIType.PYQTSpinBox, 5),
            (self.ui.uiSPNDBL_test1, PrefSaver.UIType.PYQTDoubleSpinBox, 10.5),
            (self.ui.uiTIMEDT_test1, PrefSaver.UIType.PYQTTimeEdit, QtCore.QTime.currentTime()),
            (self.ui.uiDATEDT_test1, PrefSaver.UIType.PYQTDateEdit, QtCore.QDate.currentDate()),
            (self.ui.uiDTEDIT_test1, PrefSaver.UIType.PYQTDateTimeEdit, QtCore.QDateTime.currentDateTime()),
            (self.ui.uiBTN_test1, PrefSaver.UIType.PYQTCheckButton, False),
            (self.ui.uiCBX_test1, PrefSaver.UIType.PYQTComboBox, -1),
            (self.ui.uiCBX_test2, PrefSaver.UIType.PYQTComboBoxEditable, -1),
            (self.ui.uiSCR_test1, PrefSaver.UIType.PYQTScrollBar, 0),
            (self.ui.uiSCA_test1, PrefSaver.UIType.PYQTScrollArea, (0, 0)),
            (self.ui.uiSLD_test1, PrefSaver.UIType.PYQTSlider, 0),
            (self.ui.uiDIA_test1, PrefSaver.UIType.PYQTDial, 0),
            (self.ui.uiTXTEDT_test1, PrefSaver.UIType.PYQTTextEdit, 'default text with <strong>bold contents</strong>'),
            (self.ui.uiPTXEDT_test1, PrefSaver.UIType.PYQTPlainTextEdit, 'default text'),
            (self.ui.uiSTK_test1, PrefSaver.UIType.PYQTStackedWidget, 0),
            (self.ui.uiTBX_test1, PrefSaver.UIType.PYQTToolBox, 0),
            (self.ui.uiTBX_test2, PrefSaver.UIType.PYQTToolBox, 0),
            (self.ui.uiTAB_test1, PrefSaver.UIType.PYQTTabWidget, 0),
            (self.ui.uiSPL_test1, PrefSaver.UIType.PYQTSplitter, (100, 400)),
            (self.ui.uiLSTWID_test1, PrefSaver.UIType.PYQTListWidget, None),
            (self.ui.uiTBLWID_test1, PrefSaver.UIType.PYQTTableWidget, None),
            (self.ui.uiTREW_test1, PrefSaver.UIType.PYQTTreeWidget, None),
            (self.ui.uiLSTV_test1, PrefSaver.UIType.PYQTListView, None),
            (self.ui.uiTBLV_test1, PrefSaver.UIType.PYQTTableView, None),
            (self.ui.uiTREV_test1, PrefSaver.UIType.PYQTTreeView, None)
        ]

        PySideControls = [
            (self.win, PrefSaver.UIType.PYSIDEWindow, (200, 200, 900, 500)),
            (self.dlg, PrefSaver.UIType.PYSIDEWindow, (300, 300, 200, 200)),
            (self.ui.uiCHK_test1, PrefSaver.UIType.PYSIDECheckBox, QtCore.Qt.Unchecked),
            (self.ui.uiCHK_testTri1, PrefSaver.UIType.PYSIDECheckBox, QtCore.Qt.Unchecked),
            (self.ui.uiRAD_test1, PrefSaver.UIType.PYSIDERadioButton, True),
            (self.ui.uiRAD_test2, PrefSaver.UIType.PYSIDERadioButton, False),
            (self.ui.uiLED_test1, PrefSaver.UIType.PYSIDELineEdit, 'defaultValue'),
            (self.ui.uiSPN_test1, PrefSaver.UIType.PYSIDESpinBox, 5),
            (self.ui.uiSPNDBL_test1, PrefSaver.UIType.PYSIDEDoubleSpinBox, 10.5),
            (self.ui.uiTIMEDT_test1, PrefSaver.UIType.PYSIDETimeEdit, QtCore.QTime.currentTime()),
            (self.ui.uiDATEDT_test1, PrefSaver.UIType.PYSIDEDateEdit, QtCore.QDate.currentDate()),
            (self.ui.uiDTEDIT_test1, PrefSaver.UIType.PYSIDEDateTimeEdit, QtCore.QDateTime.currentDateTime()),
            (self.ui.uiBTN_test1, PrefSaver.UIType.PYSIDECheckButton, False),
            (self.ui.uiCBX_test1, PrefSaver.UIType.PYSIDEComboBox, -1),
            (self.ui.uiCBX_test2, PrefSaver.UIType.PYSIDEComboBoxEditable, -1),
            (self.ui.uiSCR_test1, PrefSaver.UIType.PYSIDEScrollBar, 0),
            (self.ui.uiSCA_test1, PrefSaver.UIType.PYSIDEScrollArea, (0, 0)),
            (self.ui.uiSLD_test1, PrefSaver.UIType.PYSIDESlider, 0),
            (self.ui.uiDIA_test1, PrefSaver.UIType.PYSIDEDial, 0),
            (self.ui.uiTXTEDT_test1, PrefSaver.UIType.PYSIDETextEdit, 'default text with <strong>bold contents</strong>'),
            (self.ui.uiPTXEDT_test1, PrefSaver.UIType.PYSIDEPlainTextEdit, 'default text'),
            (self.ui.uiSTK_test1, PrefSaver.UIType.PYSIDEStackedWidget, 0),
            (self.ui.uiTBX_test1, PrefSaver.UIType.PYSIDEToolBox, 0),
            (self.ui.uiTBX_test2, PrefSaver.UIType.PYSIDEToolBox, 0),
            (self.ui.uiTAB_test1, PrefSaver.UIType.PYSIDETabWidget, 0),
            (self.ui.uiSPL_test1, PrefSaver.UIType.PYSIDESplitter, (100, 400)),
            (self.ui.uiLSTWID_test1, PrefSaver.UIType.PYSIDEListWidget, None),
            (self.ui.uiTBLWID_test1, PrefSaver.UIType.PYSIDETableWidget, None),
            (self.ui.uiTREW_test1, PrefSaver.UIType.PYSIDETreeWidget, None),
            (self.ui.uiLSTV_test1, PrefSaver.UIType.PYSIDEListView, None),
            (self.ui.uiTBLV_test1, PrefSaver.UIType.PYSIDETableView, None),
            (self.ui.uiTREV_test1, PrefSaver.UIType.PYSIDETreeView, None)
        ]

        if self.qtType == TestQtWindow.QtTypePyQt:
            controlList = PyQtControls
        else:
            controlList = PySideControls

        for control, cType, default in controlList:
            if defaults:
                self.prefSaver.addControl(control, cType, default)
            else:
                self.prefSaver.addControl(control, cType)

        self.setupVariable()

    def setupVariable(self):

        def variable1Getter():
            return self.ui.uiLED_testVariable1.text()

        def variable1Setter(arg):
            self.ui.uiLED_testVariable1.setText(arg)

        self.prefSaver.addVariable('variable1', variable1Getter, variable1Setter, 'defaultVariable1Value')

    def onStackedWidgetPageDec(self):
        self.nextStackIdx(-1)

    def onStackedWidgetPageInc(self):
        self.nextStackIdx(1)

    def nextStackIdx(self, inc):
        self.ui.uiSTK_test1.setCurrentIndex((self.ui.uiSTK_test1.currentIndex() + inc) % 3)

    def onSavePrefsClicked(self):
        self.prefSaver.savePrefs()

    def onLoadPrefsClicked(self):
        self.prefSaver.loadPrefs()

    def onResetPrefsClicked(self):
        self.prefSaver.resetPrefs()

    def onShowDialogClicked(self):
        self.dlg.show()
