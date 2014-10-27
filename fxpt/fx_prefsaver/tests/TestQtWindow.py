# from PyQt4 import QtGui

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
        self.initPrefs()
        self.ui.setupUi(self.win)

        self.win.setWindowTitle('{}; {}'.format(str(self.win), str(self.dlg)))

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

    def onShowDialogClicked(self):
        self.dlg.show()
