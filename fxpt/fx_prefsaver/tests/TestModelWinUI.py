# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TestModelWinUI.ui'
#
# Created: Thu Nov 27 23:29:52 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(955, 914)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_3 = QtGui.QSplitter(self.centralwidget)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName("splitter_3")
        self.splitter_2 = QtGui.QSplitter(self.splitter_3)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.uiLSTV_test1 = QtGui.QListView(self.widget)
        self.uiLSTV_test1.setObjectName("uiLSTV_test1")
        self.horizontalLayout.addWidget(self.uiLSTV_test1)
        self.uiTBLV_test1 = QtGui.QTableView(self.widget)
        self.uiTBLV_test1.setSortingEnabled(True)
        self.uiTBLV_test1.setObjectName("uiTBLV_test1")
        self.uiTBLV_test1.horizontalHeader().setSortIndicatorShown(True)
        self.horizontalLayout.addWidget(self.uiTBLV_test1)
        self.uiCOLV_test1 = QtGui.QColumnView(self.splitter)
        self.uiCOLV_test1.setObjectName("uiCOLV_test1")
        self.uiTRV_test1 = QtGui.QTreeView(self.splitter_2)
        self.uiTRV_test1.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.uiTRV_test1.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.uiTRV_test1.setSortingEnabled(True)
        self.uiTRV_test1.setObjectName("uiTRV_test1")
        self.uiTRV_test1.header().setDefaultSectionSize(150)
        self.uiTRV_test1.header().setMinimumSectionSize(150)
        self.uiTXT_output = QtGui.QPlainTextEdit(self.splitter_3)
        font = QtGui.QFont()
        font.setFamily("Lucida Console")
        self.uiTXT_output.setFont(font)
        self.uiTXT_output.setObjectName("uiTXT_output")
        self.verticalLayout.addWidget(self.splitter_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.uiTRV_test1, QtCore.SIGNAL("clicked(QModelIndex)"), MainWindow.onTreeViewItemClicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))

