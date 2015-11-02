from PySide import QtGui, QtCore
import shiboken
import maya.OpenMayaUI as omui


mainWin = None


class TestUI(QtGui.QMainWindow):

    def __init__(self, parent):
        super(TestUI, self).__init__(parent=parent)

        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)

        self.layout = QtGui.QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.lineEdit = QtGui.QLineEdit('defaultText')
        self.layout.addWidget(self.lineEdit)
        self.font = self.lineEdit.font()

        self.tableWidget = QtGui.QTableWidget()
        self.layout.addWidget(self.tableWidget)
        self.horHeader = self.tableWidget.horizontalHeader()

        self.button = QtGui.QPushButton('Click Me')
        self.layout.addWidget(self.button)
        self.button.connect(self.button, QtCore.SIGNAL('clicked()'), self.onButtonClicked)

        print 'try to access variables right after creation:'
        self.onButtonClicked()
        print

    def onButtonClicked(self):
        print 'QTableWidget -> QHeaderView: runtime: sortSection =', self.tableWidget.horizontalHeader().sortIndicatorSection()
        try:
            print 'QTableWidget -> QHeaderView: cached: sortSection =', self.horHeader.sortIndicatorSection()
        except Exception as e:
            print 'C++ object is dead. Exception:', str(e)

        print 'QLineEdit -> QFont: runtime: font is italic =', self.lineEdit.font().italic()
        try:
            print 'QLineEdit -> QFont: cached: font is italic =', self.font.italic()
        except Exception as e:
            print 'C++ object is dead. Exception:', str(e)


def run():
    global mainWin
    if not mainWin:
        ptr = omui.MQtUtil.mainWindow()
        if ptr:
            mayaQMainWindow = shiboken.wrapInstance(long(ptr), QtGui.QMainWindow)
        else:
            raise Exception('Cannot find Maya main window.')
        mainWin = TestUI(parent=mayaQMainWindow)
        # mainWin = TestUI(parent=None)

    mainWin.show()
    mainWin.raise_()
