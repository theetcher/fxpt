# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'qt_window_test_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(962, 771)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.uiSPL_test1 = QSplitter(self.centralwidget)
        self.uiSPL_test1.setObjectName(u"uiSPL_test1")
        self.uiSPL_test1.setOrientation(Qt.Horizontal)
        self.uiSPL_test1.setHandleWidth(10)
        self.layoutWidget = QWidget(self.uiSPL_test1)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.uiCHK_test1 = QCheckBox(self.layoutWidget)
        self.uiCHK_test1.setObjectName(u"uiCHK_test1")

        self.verticalLayout.addWidget(self.uiCHK_test1)

        self.uiCHK_testTri1 = QCheckBox(self.layoutWidget)
        self.uiCHK_testTri1.setObjectName(u"uiCHK_testTri1")
        self.uiCHK_testTri1.setTristate(True)

        self.verticalLayout.addWidget(self.uiCHK_testTri1)

        self.uiGRPBOX_test1 = QGroupBox(self.layoutWidget)
        self.uiGRPBOX_test1.setObjectName(u"uiGRPBOX_test1")
        self.uiGRPBOX_test1.setCheckable(True)
        self.uiGRPBOX_test1.setChecked(True)
        self.horizontalLayout = QHBoxLayout(self.uiGRPBOX_test1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.uiRAD_test1 = QRadioButton(self.uiGRPBOX_test1)
        self.uiRAD_test1.setObjectName(u"uiRAD_test1")

        self.horizontalLayout.addWidget(self.uiRAD_test1)

        self.uiRAD_test2 = QRadioButton(self.uiGRPBOX_test1)
        self.uiRAD_test2.setObjectName(u"uiRAD_test2")

        self.horizontalLayout.addWidget(self.uiRAD_test2)


        self.verticalLayout.addWidget(self.uiGRPBOX_test1)

        self.uiLED_test1 = QLineEdit(self.layoutWidget)
        self.uiLED_test1.setObjectName(u"uiLED_test1")

        self.verticalLayout.addWidget(self.uiLED_test1)

        self.uiSPN_test1 = QSpinBox(self.layoutWidget)
        self.uiSPN_test1.setObjectName(u"uiSPN_test1")

        self.verticalLayout.addWidget(self.uiSPN_test1)

        self.uiSPNDBL_test1 = QDoubleSpinBox(self.layoutWidget)
        self.uiSPNDBL_test1.setObjectName(u"uiSPNDBL_test1")

        self.verticalLayout.addWidget(self.uiSPNDBL_test1)

        self.uiTIMEDT_test1 = QTimeEdit(self.layoutWidget)
        self.uiTIMEDT_test1.setObjectName(u"uiTIMEDT_test1")

        self.verticalLayout.addWidget(self.uiTIMEDT_test1)

        self.uiDATEDT_test1 = QDateEdit(self.layoutWidget)
        self.uiDATEDT_test1.setObjectName(u"uiDATEDT_test1")

        self.verticalLayout.addWidget(self.uiDATEDT_test1)

        self.uiDTEDIT_test1 = QDateTimeEdit(self.layoutWidget)
        self.uiDTEDIT_test1.setObjectName(u"uiDTEDIT_test1")

        self.verticalLayout.addWidget(self.uiDTEDIT_test1)

        self.uiBTN_test1 = QPushButton(self.layoutWidget)
        self.uiBTN_test1.setObjectName(u"uiBTN_test1")
        self.uiBTN_test1.setCheckable(True)

        self.verticalLayout.addWidget(self.uiBTN_test1)

        self.uiCBX_test1 = QComboBox(self.layoutWidget)
        self.uiCBX_test1.addItem("")
        self.uiCBX_test1.addItem("")
        self.uiCBX_test1.addItem("")
        self.uiCBX_test1.addItem("")
        self.uiCBX_test1.addItem("")
        self.uiCBX_test1.addItem("")
        self.uiCBX_test1.addItem("")
        self.uiCBX_test1.setObjectName(u"uiCBX_test1")

        self.verticalLayout.addWidget(self.uiCBX_test1)

        self.uiCBX_test2 = QComboBox(self.layoutWidget)
        self.uiCBX_test2.setObjectName(u"uiCBX_test2")
        self.uiCBX_test2.setEditable(True)

        self.verticalLayout.addWidget(self.uiCBX_test2)

        self.uiSCR_test1 = QScrollBar(self.layoutWidget)
        self.uiSCR_test1.setObjectName(u"uiSCR_test1")
        self.uiSCR_test1.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.uiSCR_test1)

        self.uiSLD_test1 = QSlider(self.layoutWidget)
        self.uiSLD_test1.setObjectName(u"uiSLD_test1")
        self.uiSLD_test1.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.uiSLD_test1)

        self.uiDIA_test1 = QDial(self.layoutWidget)
        self.uiDIA_test1.setObjectName(u"uiDIA_test1")

        self.verticalLayout.addWidget(self.uiDIA_test1)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_15.addWidget(self.label_4)

        self.uiLED_testVariable1 = QLineEdit(self.layoutWidget)
        self.uiLED_testVariable1.setObjectName(u"uiLED_testVariable1")

        self.horizontalLayout_15.addWidget(self.uiLED_testVariable1)


        self.verticalLayout.addLayout(self.horizontalLayout_15)

        self.uiBTN_showDialog = QPushButton(self.layoutWidget)
        self.uiBTN_showDialog.setObjectName(u"uiBTN_showDialog")

        self.verticalLayout.addWidget(self.uiBTN_showDialog)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.uiSPL_test1.addWidget(self.layoutWidget)
        self.uiTAB_test1 = QTabWidget(self.uiSPL_test1)
        self.uiTAB_test1.setObjectName(u"uiTAB_test1")
        self.uiTABPG_listWidget = QWidget()
        self.uiTABPG_listWidget.setObjectName(u"uiTABPG_listWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.uiTABPG_listWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.uiLSTWID_test1 = QListWidget(self.uiTABPG_listWidget)
        QListWidgetItem(self.uiLSTWID_test1)
        QListWidgetItem(self.uiLSTWID_test1)
        QListWidgetItem(self.uiLSTWID_test1)
        QListWidgetItem(self.uiLSTWID_test1)
        QListWidgetItem(self.uiLSTWID_test1)
        QListWidgetItem(self.uiLSTWID_test1)
        QListWidgetItem(self.uiLSTWID_test1)
        self.uiLSTWID_test1.setObjectName(u"uiLSTWID_test1")
        self.uiLSTWID_test1.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.horizontalLayout_2.addWidget(self.uiLSTWID_test1)

        self.uiTAB_test1.addTab(self.uiTABPG_listWidget, "")
        self.uiTABPG_treeWidget = QWidget()
        self.uiTABPG_treeWidget.setObjectName(u"uiTABPG_treeWidget")
        self.horizontalLayout_3 = QHBoxLayout(self.uiTABPG_treeWidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.uiTREW_test1 = QTreeWidget(self.uiTABPG_treeWidget)
        QTreeWidgetItem(self.uiTREW_test1)
        QTreeWidgetItem(self.uiTREW_test1)
        QTreeWidgetItem(self.uiTREW_test1)
        __qtreewidgetitem = QTreeWidgetItem(self.uiTREW_test1)
        __qtreewidgetitem1 = QTreeWidgetItem(__qtreewidgetitem)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        QTreeWidgetItem(__qtreewidgetitem1)
        __qtreewidgetitem2 = QTreeWidgetItem(self.uiTREW_test1)
        __qtreewidgetitem3 = QTreeWidgetItem(__qtreewidgetitem2)
        QTreeWidgetItem(__qtreewidgetitem3)
        QTreeWidgetItem(__qtreewidgetitem3)
        QTreeWidgetItem(__qtreewidgetitem3)
        __qtreewidgetitem4 = QTreeWidgetItem(self.uiTREW_test1)
        __qtreewidgetitem5 = QTreeWidgetItem(__qtreewidgetitem4)
        QTreeWidgetItem(__qtreewidgetitem5)
        QTreeWidgetItem(__qtreewidgetitem5)
        QTreeWidgetItem(__qtreewidgetitem5)
        self.uiTREW_test1.setObjectName(u"uiTREW_test1")
        self.uiTREW_test1.setAlternatingRowColors(True)
        self.uiTREW_test1.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.uiTREW_test1.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.uiTREW_test1.setSortingEnabled(True)
        self.uiTREW_test1.header().setMinimumSectionSize(200)
        self.uiTREW_test1.header().setDefaultSectionSize(200)
        self.uiTREW_test1.header().setProperty("showSortIndicator", True)

        self.horizontalLayout_3.addWidget(self.uiTREW_test1)

        self.uiTAB_test1.addTab(self.uiTABPG_treeWidget, "")
        self.uiTABPG_tableWidget = QWidget()
        self.uiTABPG_tableWidget.setObjectName(u"uiTABPG_tableWidget")
        self.horizontalLayout_4 = QHBoxLayout(self.uiTABPG_tableWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.uiTBLWID_test1 = QTableWidget(self.uiTABPG_tableWidget)
        if (self.uiTBLWID_test1.columnCount() < 2):
            self.uiTBLWID_test1.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.uiTBLWID_test1.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.uiTBLWID_test1.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.uiTBLWID_test1.rowCount() < 7):
            self.uiTBLWID_test1.setRowCount(7)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.uiTBLWID_test1.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.uiTBLWID_test1.setVerticalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.uiTBLWID_test1.setVerticalHeaderItem(2, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.uiTBLWID_test1.setVerticalHeaderItem(3, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.uiTBLWID_test1.setVerticalHeaderItem(4, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.uiTBLWID_test1.setVerticalHeaderItem(5, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.uiTBLWID_test1.setVerticalHeaderItem(6, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.uiTBLWID_test1.setItem(0, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.uiTBLWID_test1.setItem(0, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.uiTBLWID_test1.setItem(1, 0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.uiTBLWID_test1.setItem(1, 1, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.uiTBLWID_test1.setItem(2, 0, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.uiTBLWID_test1.setItem(2, 1, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.uiTBLWID_test1.setItem(3, 0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.uiTBLWID_test1.setItem(3, 1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.uiTBLWID_test1.setItem(4, 0, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.uiTBLWID_test1.setItem(4, 1, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.uiTBLWID_test1.setItem(5, 0, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.uiTBLWID_test1.setItem(5, 1, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.uiTBLWID_test1.setItem(6, 0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.uiTBLWID_test1.setItem(6, 1, __qtablewidgetitem22)
        self.uiTBLWID_test1.setObjectName(u"uiTBLWID_test1")
        self.uiTBLWID_test1.setSortingEnabled(True)
        self.uiTBLWID_test1.horizontalHeader().setProperty("showSortIndicator", True)

        self.horizontalLayout_4.addWidget(self.uiTBLWID_test1)

        self.uiTAB_test1.addTab(self.uiTABPG_tableWidget, "")
        self.uiTABPG_listView = QWidget()
        self.uiTABPG_listView.setObjectName(u"uiTABPG_listView")
        self.horizontalLayout_7 = QHBoxLayout(self.uiTABPG_listView)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.uiLSTV_test1 = QListView(self.uiTABPG_listView)
        self.uiLSTV_test1.setObjectName(u"uiLSTV_test1")
        self.uiLSTV_test1.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.horizontalLayout_7.addWidget(self.uiLSTV_test1)

        self.uiTAB_test1.addTab(self.uiTABPG_listView, "")
        self.uiTABPG_treeView = QWidget()
        self.uiTABPG_treeView.setObjectName(u"uiTABPG_treeView")
        self.horizontalLayout_8 = QHBoxLayout(self.uiTABPG_treeView)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.uiTREV_test1 = QTreeView(self.uiTABPG_treeView)
        self.uiTREV_test1.setObjectName(u"uiTREV_test1")
        self.uiTREV_test1.setAlternatingRowColors(True)
        self.uiTREV_test1.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.uiTREV_test1.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.uiTREV_test1.setSortingEnabled(True)
        self.uiTREV_test1.header().setMinimumSectionSize(200)
        self.uiTREV_test1.header().setDefaultSectionSize(200)
        self.uiTREV_test1.header().setProperty("showSortIndicator", True)

        self.horizontalLayout_8.addWidget(self.uiTREV_test1)

        self.uiTAB_test1.addTab(self.uiTABPG_treeView, "")
        self.uiTABPG_tableView = QWidget()
        self.uiTABPG_tableView.setObjectName(u"uiTABPG_tableView")
        self.horizontalLayout_10 = QHBoxLayout(self.uiTABPG_tableView)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.uiTBLV_test1 = QTableView(self.uiTABPG_tableView)
        self.uiTBLV_test1.setObjectName(u"uiTBLV_test1")
        self.uiTBLV_test1.setSortingEnabled(True)
        self.uiTBLV_test1.horizontalHeader().setProperty("showSortIndicator", True)

        self.horizontalLayout_10.addWidget(self.uiTBLV_test1)

        self.uiTAB_test1.addTab(self.uiTABPG_tableView, "")
        self.uiTABPG_columnView = QWidget()
        self.uiTABPG_columnView.setObjectName(u"uiTABPG_columnView")
        self.horizontalLayout_9 = QHBoxLayout(self.uiTABPG_columnView)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.uiCOLV_test1 = QColumnView(self.uiTABPG_columnView)
        self.uiCOLV_test1.setObjectName(u"uiCOLV_test1")

        self.horizontalLayout_9.addWidget(self.uiCOLV_test1)

        self.uiTAB_test1.addTab(self.uiTABPG_columnView, "")
        self.uiTABPG_scrollText = QWidget()
        self.uiTABPG_scrollText.setObjectName(u"uiTABPG_scrollText")
        self.horizontalLayout_6 = QHBoxLayout(self.uiTABPG_scrollText)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.uiSCA_test1 = QScrollArea(self.uiTABPG_scrollText)
        self.uiSCA_test1.setObjectName(u"uiSCA_test1")
        self.uiSCA_test1.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 634, 676))
        self.horizontalLayout_11 = QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.uiTXTEDT_test1 = QTextEdit(self.scrollAreaWidgetContents)
        self.uiTXTEDT_test1.setObjectName(u"uiTXTEDT_test1")
        self.uiTXTEDT_test1.setMinimumSize(QSize(300, 600))

        self.horizontalLayout_11.addWidget(self.uiTXTEDT_test1)

        self.uiPTXEDT_test1 = QPlainTextEdit(self.scrollAreaWidgetContents)
        self.uiPTXEDT_test1.setObjectName(u"uiPTXEDT_test1")
        self.uiPTXEDT_test1.setMinimumSize(QSize(300, 600))

        self.horizontalLayout_11.addWidget(self.uiPTXEDT_test1)

        self.uiSCA_test1.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_6.addWidget(self.uiSCA_test1)

        self.uiTAB_test1.addTab(self.uiTABPG_scrollText, "")
        self.uiTABPG_stackTool = QWidget()
        self.uiTABPG_stackTool.setObjectName(u"uiTABPG_stackTool")
        self.verticalLayout_6 = QVBoxLayout(self.uiTABPG_stackTool)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(4, 6, 4, 4)
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_2)

        self.uiBTN_stackDec = QPushButton(self.uiTABPG_stackTool)
        self.uiBTN_stackDec.setObjectName(u"uiBTN_stackDec")

        self.horizontalLayout_12.addWidget(self.uiBTN_stackDec)

        self.uiBTN_stackInc = QPushButton(self.uiTABPG_stackTool)
        self.uiBTN_stackInc.setObjectName(u"uiBTN_stackInc")

        self.horizontalLayout_12.addWidget(self.uiBTN_stackInc)


        self.verticalLayout_6.addLayout(self.horizontalLayout_12)

        self.uiSTK_test1 = QStackedWidget(self.uiTABPG_stackTool)
        self.uiSTK_test1.setObjectName(u"uiSTK_test1")
        self.page0 = QWidget()
        self.page0.setObjectName(u"page0")
        self.horizontalLayout_14 = QHBoxLayout(self.page0)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.page0)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)

        self.verticalLayout_3.addWidget(self.label)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.uiTBX_test1 = QToolBox(self.page0)
        self.uiTBX_test1.setObjectName(u"uiTBX_test1")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setGeometry(QRect(0, 0, 98, 28))
        self.uiTBX_test1.addItem(self.page, u"Page 1")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 98, 28))
        self.uiTBX_test1.addItem(self.page_2, u"Page 2")
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.page_5.setGeometry(QRect(0, 0, 318, 557))
        self.uiTBX_test1.addItem(self.page_5, u"Page 3")

        self.horizontalLayout_13.addWidget(self.uiTBX_test1)

        self.uiTBX_test2 = QToolBox(self.page0)
        self.uiTBX_test2.setObjectName(u"uiTBX_test2")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setGeometry(QRect(0, 0, 98, 28))
        self.uiTBX_test2.addItem(self.page_3, u"Page 1")
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.page_4.setGeometry(QRect(0, 0, 98, 28))
        self.uiTBX_test2.addItem(self.page_4, u"Page 2")
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.page_6.setGeometry(QRect(0, 0, 318, 557))
        self.uiTBX_test2.addItem(self.page_6, u"Page 3")

        self.horizontalLayout_13.addWidget(self.uiTBX_test2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_13)


        self.horizontalLayout_14.addLayout(self.verticalLayout_3)

        self.uiSTK_test1.addWidget(self.page0)
        self.page1 = QWidget()
        self.page1.setObjectName(u"page1")
        self.verticalLayout_4 = QVBoxLayout(self.page1)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_2 = QLabel(self.page1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.verticalLayout_4.addWidget(self.label_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.uiSTK_test1.addWidget(self.page1)
        self.page2 = QWidget()
        self.page2.setObjectName(u"page2")
        self.verticalLayout_5 = QVBoxLayout(self.page2)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_3 = QLabel(self.page2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout_5.addWidget(self.label_3)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)

        self.uiSTK_test1.addWidget(self.page2)

        self.verticalLayout_6.addWidget(self.uiSTK_test1)

        self.uiTAB_test1.addTab(self.uiTABPG_stackTool, "")
        self.uiSPL_test1.addWidget(self.uiTAB_test1)

        self.verticalLayout_2.addWidget(self.uiSPL_test1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.uiBTN_savePrefs = QPushButton(self.centralwidget)
        self.uiBTN_savePrefs.setObjectName(u"uiBTN_savePrefs")

        self.horizontalLayout_5.addWidget(self.uiBTN_savePrefs)

        self.uiBTN_loadPrefs = QPushButton(self.centralwidget)
        self.uiBTN_loadPrefs.setObjectName(u"uiBTN_loadPrefs")

        self.horizontalLayout_5.addWidget(self.uiBTN_loadPrefs)

        self.uiBTN_resetPrefs = QPushButton(self.centralwidget)
        self.uiBTN_resetPrefs.setObjectName(u"uiBTN_resetPrefs")

        self.horizontalLayout_5.addWidget(self.uiBTN_resetPrefs)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.verticalLayout_2.setStretch(0, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.uiBTN_savePrefs.clicked.connect(MainWindow.onSavePrefsClicked)
        self.uiBTN_loadPrefs.clicked.connect(MainWindow.onLoadPrefsClicked)
        self.uiBTN_resetPrefs.clicked.connect(MainWindow.onResetPrefsClicked)
        self.uiBTN_showDialog.clicked.connect(MainWindow.onShowDialogClicked)
        self.uiBTN_stackDec.clicked.connect(MainWindow.onStackedWidgetPageDec)
        self.uiBTN_stackInc.clicked.connect(MainWindow.onStackedWidgetPageInc)

        self.uiTAB_test1.setCurrentIndex(2)
        self.uiSTK_test1.setCurrentIndex(0)
        self.uiTBX_test1.setCurrentIndex(2)
        self.uiTBX_test2.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.uiCHK_test1.setText(QCoreApplication.translate("MainWindow", u"CheckBox", None))
        self.uiCHK_testTri1.setText(QCoreApplication.translate("MainWindow", u"TriState CheckBox", None))
        self.uiGRPBOX_test1.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.uiRAD_test1.setText(QCoreApplication.translate("MainWindow", u"RadioButton1", None))
        self.uiRAD_test2.setText(QCoreApplication.translate("MainWindow", u"RadioButton2", None))
        self.uiBTN_test1.setText(QCoreApplication.translate("MainWindow", u"Check Button", None))
        self.uiCBX_test1.setItemText(0, QCoreApplication.translate("MainWindow", u"Item1", None))
        self.uiCBX_test1.setItemText(1, QCoreApplication.translate("MainWindow", u"Item2", None))
        self.uiCBX_test1.setItemText(2, QCoreApplication.translate("MainWindow", u"Item3", None))
        self.uiCBX_test1.setItemText(3, QCoreApplication.translate("MainWindow", u"Item4", None))
        self.uiCBX_test1.setItemText(4, QCoreApplication.translate("MainWindow", u"Item5", None))
        self.uiCBX_test1.setItemText(5, QCoreApplication.translate("MainWindow", u"Item6", None))
        self.uiCBX_test1.setItemText(6, QCoreApplication.translate("MainWindow", u"Item7", None))

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Variable:", None))
        self.uiBTN_showDialog.setText(QCoreApplication.translate("MainWindow", u"Show Dialog", None))

        __sortingEnabled = self.uiLSTWID_test1.isSortingEnabled()
        self.uiLSTWID_test1.setSortingEnabled(False)
        ___qlistwidgetitem = self.uiLSTWID_test1.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"Item1", None));
        ___qlistwidgetitem1 = self.uiLSTWID_test1.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Item2", None));
        ___qlistwidgetitem2 = self.uiLSTWID_test1.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Item3", None));
        ___qlistwidgetitem3 = self.uiLSTWID_test1.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Item4", None));
        ___qlistwidgetitem4 = self.uiLSTWID_test1.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Item7", None));
        ___qlistwidgetitem5 = self.uiLSTWID_test1.item(5)
        ___qlistwidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Item6", None));
        ___qlistwidgetitem6 = self.uiLSTWID_test1.item(6)
        ___qlistwidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Item5", None));
        self.uiLSTWID_test1.setSortingEnabled(__sortingEnabled)

        self.uiTAB_test1.setTabText(self.uiTAB_test1.indexOf(self.uiTABPG_listWidget), QCoreApplication.translate("MainWindow", u"List Widget", None))
        ___qtreewidgetitem = self.uiTREW_test1.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"column2", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"column1", None));

        __sortingEnabled1 = self.uiTREW_test1.isSortingEnabled()
        self.uiTREW_test1.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.uiTREW_test1.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"rootItem3", None));
        ___qtreewidgetitem2 = self.uiTREW_test1.topLevelItem(1)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"rootItem2", None));
        ___qtreewidgetitem3 = self.uiTREW_test1.topLevelItem(2)
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("MainWindow", u"rootItem1", None));
        ___qtreewidgetitem4 = self.uiTREW_test1.topLevelItem(3)
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("MainWindow", u"folder3", None));
        ___qtreewidgetitem5 = ___qtreewidgetitem4.child(0)
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("MainWindow", u"folder31", None));
        ___qtreewidgetitem6 = ___qtreewidgetitem5.child(0)
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("MainWindow", u"item313", None));
        ___qtreewidgetitem7 = ___qtreewidgetitem5.child(1)
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("MainWindow", u"item312", None));
        ___qtreewidgetitem8 = ___qtreewidgetitem5.child(2)
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("MainWindow", u"item311", None));
        ___qtreewidgetitem9 = self.uiTREW_test1.topLevelItem(4)
        ___qtreewidgetitem9.setText(1, QCoreApplication.translate("MainWindow", u"value6", None));
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("MainWindow", u"folder2", None));
        ___qtreewidgetitem10 = ___qtreewidgetitem9.child(0)
        ___qtreewidgetitem10.setText(1, QCoreApplication.translate("MainWindow", u"value7", None));
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("MainWindow", u"folder21", None));
        ___qtreewidgetitem11 = ___qtreewidgetitem10.child(0)
        ___qtreewidgetitem11.setText(0, QCoreApplication.translate("MainWindow", u"item213", None));
        ___qtreewidgetitem12 = ___qtreewidgetitem10.child(1)
        ___qtreewidgetitem12.setText(0, QCoreApplication.translate("MainWindow", u"item212", None));
        ___qtreewidgetitem13 = ___qtreewidgetitem10.child(2)
        ___qtreewidgetitem13.setText(1, QCoreApplication.translate("MainWindow", u"value8", None));
        ___qtreewidgetitem13.setText(0, QCoreApplication.translate("MainWindow", u"item211", None));
        ___qtreewidgetitem14 = self.uiTREW_test1.topLevelItem(5)
        ___qtreewidgetitem14.setText(1, QCoreApplication.translate("MainWindow", u"value1", None));
        ___qtreewidgetitem14.setText(0, QCoreApplication.translate("MainWindow", u"folder1", None));
        ___qtreewidgetitem15 = ___qtreewidgetitem14.child(0)
        ___qtreewidgetitem15.setText(1, QCoreApplication.translate("MainWindow", u"value2", None));
        ___qtreewidgetitem15.setText(0, QCoreApplication.translate("MainWindow", u"folder11", None));
        ___qtreewidgetitem16 = ___qtreewidgetitem15.child(0)
        ___qtreewidgetitem16.setText(1, QCoreApplication.translate("MainWindow", u"value5", None));
        ___qtreewidgetitem16.setText(0, QCoreApplication.translate("MainWindow", u"item113", None));
        ___qtreewidgetitem17 = ___qtreewidgetitem15.child(1)
        ___qtreewidgetitem17.setText(1, QCoreApplication.translate("MainWindow", u"value4", None));
        ___qtreewidgetitem17.setText(0, QCoreApplication.translate("MainWindow", u"item112", None));
        ___qtreewidgetitem18 = ___qtreewidgetitem15.child(2)
        ___qtreewidgetitem18.setText(1, QCoreApplication.translate("MainWindow", u"value3", None));
        ___qtreewidgetitem18.setText(0, QCoreApplication.translate("MainWindow", u"item111", None));
        self.uiTREW_test1.setSortingEnabled(__sortingEnabled1)

        self.uiTAB_test1.setTabText(self.uiTAB_test1.indexOf(self.uiTABPG_treeWidget), QCoreApplication.translate("MainWindow", u"Tree Widget", None))
        ___qtablewidgetitem = self.uiTBLWID_test1.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Column1", None));
        ___qtablewidgetitem1 = self.uiTBLWID_test1.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Column2", None));
        ___qtablewidgetitem2 = self.uiTBLWID_test1.verticalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Row1", None));
        ___qtablewidgetitem3 = self.uiTBLWID_test1.verticalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Row2", None));
        ___qtablewidgetitem4 = self.uiTBLWID_test1.verticalHeaderItem(2)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Row3", None));
        ___qtablewidgetitem5 = self.uiTBLWID_test1.verticalHeaderItem(3)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Row4", None));
        ___qtablewidgetitem6 = self.uiTBLWID_test1.verticalHeaderItem(4)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Row5", None));
        ___qtablewidgetitem7 = self.uiTBLWID_test1.verticalHeaderItem(5)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Row6", None));
        ___qtablewidgetitem8 = self.uiTBLWID_test1.verticalHeaderItem(6)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Row7", None));

        __sortingEnabled2 = self.uiTBLWID_test1.isSortingEnabled()
        self.uiTBLWID_test1.setSortingEnabled(False)
        ___qtablewidgetitem9 = self.uiTBLWID_test1.item(0, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"value11", None));
        ___qtablewidgetitem10 = self.uiTBLWID_test1.item(0, 1)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"value12", None));
        ___qtablewidgetitem11 = self.uiTBLWID_test1.item(1, 0)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"value61", None));
        ___qtablewidgetitem12 = self.uiTBLWID_test1.item(1, 1)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"value62", None));
        ___qtablewidgetitem13 = self.uiTBLWID_test1.item(2, 0)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"value51", None));
        ___qtablewidgetitem14 = self.uiTBLWID_test1.item(2, 1)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"value52", None));
        ___qtablewidgetitem15 = self.uiTBLWID_test1.item(3, 0)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"value41", None));
        ___qtablewidgetitem16 = self.uiTBLWID_test1.item(3, 1)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"value42", None));
        ___qtablewidgetitem17 = self.uiTBLWID_test1.item(4, 0)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"value31", None));
        ___qtablewidgetitem18 = self.uiTBLWID_test1.item(4, 1)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"value32", None));
        ___qtablewidgetitem19 = self.uiTBLWID_test1.item(5, 0)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"value21", None));
        ___qtablewidgetitem20 = self.uiTBLWID_test1.item(5, 1)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"value22", None));
        ___qtablewidgetitem21 = self.uiTBLWID_test1.item(6, 0)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"value71", None));
        ___qtablewidgetitem22 = self.uiTBLWID_test1.item(6, 1)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"value72", None));
        self.uiTBLWID_test1.setSortingEnabled(__sortingEnabled2)

        self.uiTAB_test1.setTabText(self.uiTAB_test1.indexOf(self.uiTABPG_tableWidget), QCoreApplication.translate("MainWindow", u"Table Widget", None))
        self.uiTAB_test1.setTabText(self.uiTAB_test1.indexOf(self.uiTABPG_listView), QCoreApplication.translate("MainWindow", u"List View", None))
        self.uiTAB_test1.setTabText(self.uiTAB_test1.indexOf(self.uiTABPG_treeView), QCoreApplication.translate("MainWindow", u"Tree View", None))
        self.uiTAB_test1.setTabText(self.uiTAB_test1.indexOf(self.uiTABPG_tableView), QCoreApplication.translate("MainWindow", u"Table View", None))
        self.uiTAB_test1.setTabText(self.uiTAB_test1.indexOf(self.uiTABPG_columnView), QCoreApplication.translate("MainWindow", u"Column View", None))
        self.uiTAB_test1.setTabText(self.uiTAB_test1.indexOf(self.uiTABPG_scrollText), QCoreApplication.translate("MainWindow", u"ScrollArea And Text", None))
        self.uiBTN_stackDec.setText(QCoreApplication.translate("MainWindow", u"<<", None))
        self.uiBTN_stackInc.setText(QCoreApplication.translate("MainWindow", u">>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"StackedWidget Page 0", None))
        self.uiTBX_test1.setItemText(self.uiTBX_test1.indexOf(self.page), QCoreApplication.translate("MainWindow", u"Page 1", None))
        self.uiTBX_test1.setItemText(self.uiTBX_test1.indexOf(self.page_2), QCoreApplication.translate("MainWindow", u"Page 2", None))
        self.uiTBX_test1.setItemText(self.uiTBX_test1.indexOf(self.page_5), QCoreApplication.translate("MainWindow", u"Page 3", None))
        self.uiTBX_test2.setItemText(self.uiTBX_test2.indexOf(self.page_3), QCoreApplication.translate("MainWindow", u"Page 1", None))
        self.uiTBX_test2.setItemText(self.uiTBX_test2.indexOf(self.page_4), QCoreApplication.translate("MainWindow", u"Page 2", None))
        self.uiTBX_test2.setItemText(self.uiTBX_test2.indexOf(self.page_6), QCoreApplication.translate("MainWindow", u"Page 3", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"StackedWidget Page 1", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"StackedWidget Page 2", None))
        self.uiTAB_test1.setTabText(self.uiTAB_test1.indexOf(self.uiTABPG_stackTool), QCoreApplication.translate("MainWindow", u"Stacked Widget and ToolBox", None))
        self.uiBTN_savePrefs.setText(QCoreApplication.translate("MainWindow", u"Save Prefs", None))
        self.uiBTN_loadPrefs.setText(QCoreApplication.translate("MainWindow", u"Load Prefs", None))
        self.uiBTN_resetPrefs.setText(QCoreApplication.translate("MainWindow", u"Reset Prefs", None))
    # retranslateUi

