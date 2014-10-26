# from PyQt4 import QtGui

# import TestPyQtWindowUI
from fxpt.fx_prefsaver import PrefSaver


# noinspection PyAttributeOutsideInit
class TestQtWindow(object):

    QtTypePyQt = 0
    QtTypePySide = 1

    # noinspection PyArgumentList
    def __init__(self, qtType, parent=None):

        if qtType == TestQtWindow.QtTypePyQt:
            from PyQt4 import QtGui
            import TestPyQtWindowUI
            self.win = QtGui.QMainWindow(parent=parent)
            self.ui = TestPyQtWindowUI.Ui_MainWindow()
            winTitle = 'PyQt Window'
        else:
            from PySide import QtGui
            import TestPySideWindowUI
            self.win = QtGui.QMainWindow(parent=parent)
            self.ui = TestPySideWindowUI.Ui_MainWindow()
            winTitle = 'PySide Window'

        self.registerSlots()
        self.initPrefs()
        self.ui.setupUi(self.win)
        self.win.setWindowTitle(winTitle)

    def registerSlots(self):
        self.win.onSavePrefsClicked = self.onSavePrefsClicked
        self.win.onLoadPrefsClicked = self.onLoadPrefsClicked
        self.win.onResetPrefsClicked = self.onResetPrefsClicked

    def show(self):
        self.win.show()

    def raise_(self):
        self.win.raise_()

    # noinspection PyAttributeOutsideInit
    def initPrefs(self):
        self.prefSaver = PrefSaver.PrefSaverFile('aaa')

        # self.prefSaver.addControl(self, PrefSaver.UIType.QtWindow, (200, 200, 900, 500))
        # self.prefSaver.addControl(self.uiSPLmain, PrefSaver.UIType.QtSplitter, (600, 0))
        #
        # self.lastBrowsedFolder = DIR_SCENES_SRC
        #
        # def setLastBrowsedFolder(s):
        #     self.lastBrowsedFolder = s
        # self.prefSaver.addVariable('lastBrowsedFolder', lambda: self.lastBrowsedFolder, setLastBrowsedFolder, DIR_SCENES_SRC)

    def onSavePrefsClicked(self):
        print 'onSavePrefsClicked()'
        # self.prefSaver.savePrefs()

    def onLoadPrefsClicked(self):
        print 'onLoadPrefsClicked()'
        # self.prefSaver.loadPrefs()

    def onResetPrefsClicked(self):
        print 'onResetPrefsClicked()'
        # self.prefSaver.resetPrefs()
