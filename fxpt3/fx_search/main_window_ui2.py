# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from  . import resources_rc2

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(881, 636)
        icon = QIcon()
        icon.addFile(u":/icons/fx_search_search.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.ui_ACT_selectAll = QAction(MainWindow)
        self.ui_ACT_selectAll.setObjectName(u"ui_ACT_selectAll")
        self.ui_ACT_deselectAll = QAction(MainWindow)
        self.ui_ACT_deselectAll.setObjectName(u"ui_ACT_deselectAll")
        self.ui_ACT_useAllTabs = QAction(MainWindow)
        self.ui_ACT_useAllTabs.setObjectName(u"ui_ACT_useAllTabs")
        self.ui_ACT_useAllTabs.setCheckable(True)
        self.ui_ACT_copyFullNamesToClipboard = QAction(MainWindow)
        self.ui_ACT_copyFullNamesToClipboard.setObjectName(u"ui_ACT_copyFullNamesToClipboard")
        self.ui_ACT_copyShortNamesToClipboard = QAction(MainWindow)
        self.ui_ACT_copyShortNamesToClipboard.setObjectName(u"ui_ACT_copyShortNamesToClipboard")
        self.ui_ACT_showHelp = QAction(MainWindow)
        self.ui_ACT_showHelp.setObjectName(u"ui_ACT_showHelp")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.verticalLayout_4 = QVBoxLayout(self.frame)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(4, 8, 4, 8)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(2)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_4 = QSpacerItem(4, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)

        self.ui_LED_search = QLineEdit(self.frame)
        self.ui_LED_search.setObjectName(u"ui_LED_search")

        self.horizontalLayout_8.addWidget(self.ui_LED_search)

        self.horizontalSpacer_2 = QSpacerItem(2, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)

        self.ui_BTN_search = QPushButton(self.frame)
        self.ui_BTN_search.setObjectName(u"ui_BTN_search")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui_BTN_search.sizePolicy().hasHeightForWidth())
        self.ui_BTN_search.setSizePolicy(sizePolicy)
        self.ui_BTN_search.setMaximumSize(QSize(24, 24))
        self.ui_BTN_search.setIcon(icon)
        self.ui_BTN_search.setIconSize(QSize(22, 22))

        self.horizontalLayout_8.addWidget(self.ui_BTN_search)

        self.horizontalSpacer_3 = QSpacerItem(4, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)

        self.ui_BTN_soCaseSensitive = QPushButton(self.frame)
        self.ui_BTN_soCaseSensitive.setObjectName(u"ui_BTN_soCaseSensitive")
        sizePolicy.setHeightForWidth(self.ui_BTN_soCaseSensitive.sizePolicy().hasHeightForWidth())
        self.ui_BTN_soCaseSensitive.setSizePolicy(sizePolicy)
        self.ui_BTN_soCaseSensitive.setMaximumSize(QSize(24, 24))
        self.ui_BTN_soCaseSensitive.setStyleSheet(u"QPushButton{border: none} QPushButton:checked {background-color: #707070;}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/fx_search_case.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ui_BTN_soCaseSensitive.setIcon(icon1)
        self.ui_BTN_soCaseSensitive.setIconSize(QSize(20, 20))
        self.ui_BTN_soCaseSensitive.setCheckable(True)
        self.ui_BTN_soCaseSensitive.setFlat(True)

        self.horizontalLayout_8.addWidget(self.ui_BTN_soCaseSensitive)

        self.ui_BTN_soRegex = QPushButton(self.frame)
        self.ui_BTN_soRegex.setObjectName(u"ui_BTN_soRegex")
        sizePolicy.setHeightForWidth(self.ui_BTN_soRegex.sizePolicy().hasHeightForWidth())
        self.ui_BTN_soRegex.setSizePolicy(sizePolicy)
        self.ui_BTN_soRegex.setMaximumSize(QSize(24, 24))
        self.ui_BTN_soRegex.setStyleSheet(u"QPushButton{border: none} QPushButton:checked {background-color: #707070;}")
        icon2 = QIcon()
        icon2.addFile(u":/icons/fx_search_regex.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ui_BTN_soRegex.setIcon(icon2)
        self.ui_BTN_soRegex.setIconSize(QSize(22, 22))
        self.ui_BTN_soRegex.setCheckable(True)
        self.ui_BTN_soRegex.setFlat(True)

        self.horizontalLayout_8.addWidget(self.ui_BTN_soRegex)

        self.ui_BTN_soSelectFound = QPushButton(self.frame)
        self.ui_BTN_soSelectFound.setObjectName(u"ui_BTN_soSelectFound")
        sizePolicy.setHeightForWidth(self.ui_BTN_soSelectFound.sizePolicy().hasHeightForWidth())
        self.ui_BTN_soSelectFound.setSizePolicy(sizePolicy)
        self.ui_BTN_soSelectFound.setMaximumSize(QSize(24, 24))
        self.ui_BTN_soSelectFound.setStyleSheet(u"QPushButton{border: none} QPushButton:checked {background-color: #707070;}")
        icon3 = QIcon()
        icon3.addFile(u":/icons/fx_search_select.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ui_BTN_soSelectFound.setIcon(icon3)
        self.ui_BTN_soSelectFound.setIconSize(QSize(20, 20))
        self.ui_BTN_soSelectFound.setCheckable(True)
        self.ui_BTN_soSelectFound.setFlat(True)

        self.horizontalLayout_8.addWidget(self.ui_BTN_soSelectFound)

        self.ui_BTN_soIncludeShapes = QPushButton(self.frame)
        self.ui_BTN_soIncludeShapes.setObjectName(u"ui_BTN_soIncludeShapes")
        sizePolicy.setHeightForWidth(self.ui_BTN_soIncludeShapes.sizePolicy().hasHeightForWidth())
        self.ui_BTN_soIncludeShapes.setSizePolicy(sizePolicy)
        self.ui_BTN_soIncludeShapes.setMaximumSize(QSize(24, 24))
        self.ui_BTN_soIncludeShapes.setStyleSheet(u"QPushButton{border: none} QPushButton:checked {background-color: #707070;}")
        icon4 = QIcon()
        icon4.addFile(u":/icons/fx_search_shape.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ui_BTN_soIncludeShapes.setIcon(icon4)
        self.ui_BTN_soIncludeShapes.setIconSize(QSize(20, 20))
        self.ui_BTN_soIncludeShapes.setCheckable(True)
        self.ui_BTN_soIncludeShapes.setFlat(True)

        self.horizontalLayout_8.addWidget(self.ui_BTN_soIncludeShapes)

        self.ui_BTN_soSearchSelected = QPushButton(self.frame)
        self.ui_BTN_soSearchSelected.setObjectName(u"ui_BTN_soSearchSelected")
        sizePolicy.setHeightForWidth(self.ui_BTN_soSearchSelected.sizePolicy().hasHeightForWidth())
        self.ui_BTN_soSearchSelected.setSizePolicy(sizePolicy)
        self.ui_BTN_soSearchSelected.setMaximumSize(QSize(24, 24))
        self.ui_BTN_soSearchSelected.setStyleSheet(u"QPushButton{border: none} QPushButton:checked {background-color: #707070;}")
        icon5 = QIcon()
        icon5.addFile(u":/icons/fx_search_in_selected.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ui_BTN_soSearchSelected.setIcon(icon5)
        self.ui_BTN_soSearchSelected.setIconSize(QSize(20, 20))
        self.ui_BTN_soSearchSelected.setCheckable(True)
        self.ui_BTN_soSearchSelected.setFlat(True)

        self.horizontalLayout_8.addWidget(self.ui_BTN_soSearchSelected)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.frame)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.ui_STK_results = QStackedWidget(self.groupBox)
        self.ui_STK_results.setObjectName(u"ui_STK_results")
        self.ui_STKPG_status = QWidget()
        self.ui_STKPG_status.setObjectName(u"ui_STKPG_status")
        self.horizontalLayout_2 = QHBoxLayout(self.ui_STKPG_status)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ui_TXT_status = QLabel(self.ui_STKPG_status)
        self.ui_TXT_status.setObjectName(u"ui_TXT_status")
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(24)
        font.setStyleStrategy(QFont.PreferAntialias)
        self.ui_TXT_status.setFont(font)
        self.ui_TXT_status.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.ui_TXT_status)

        self.ui_STK_results.addWidget(self.ui_STKPG_status)
        self.ui_STKPG_results = QWidget()
        self.ui_STKPG_results.setObjectName(u"ui_STKPG_results")
        self.horizontalLayout_4 = QHBoxLayout(self.ui_STKPG_results)
        self.horizontalLayout_4.setContentsMargins(4, 4, 4, 4)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ui_TAB_results = QTabWidget(self.ui_STKPG_results)
        self.ui_TAB_results.setObjectName(u"ui_TAB_results")

        self.horizontalLayout_4.addWidget(self.ui_TAB_results)

        self.ui_STK_results.addWidget(self.ui_STKPG_results)

        self.horizontalLayout_5.addWidget(self.ui_STK_results)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.frame)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(140, 0))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(6, 2, 6, 6)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.ui_BTN_catAllOn = QPushButton(self.groupBox_2)
        self.ui_BTN_catAllOn.setObjectName(u"ui_BTN_catAllOn")

        self.horizontalLayout_6.addWidget(self.ui_BTN_catAllOn)

        self.ui_BTN_catAllOff = QPushButton(self.groupBox_2)
        self.ui_BTN_catAllOff.setObjectName(u"ui_BTN_catAllOff")

        self.horizontalLayout_6.addWidget(self.ui_BTN_catAllOff)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.line = QFrame(self.groupBox_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.ui_LAY_catButtons = QVBoxLayout()
        self.ui_LAY_catButtons.setSpacing(2)
        self.ui_LAY_catButtons.setObjectName(u"ui_LAY_catButtons")

        self.verticalLayout_2.addLayout(self.ui_LAY_catButtons)

        self.verticalLayout_2.setStretch(2, 1)

        self.horizontalLayout.addWidget(self.groupBox_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.verticalLayout_5.addWidget(self.frame)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)

        self.ui_BTN_close = QPushButton(self.centralwidget)
        self.ui_BTN_close.setObjectName(u"ui_BTN_close")
        sizePolicy.setHeightForWidth(self.ui_BTN_close.sizePolicy().hasHeightForWidth())
        self.ui_BTN_close.setSizePolicy(sizePolicy)
        self.ui_BTN_close.setMinimumSize(QSize(100, 30))
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(True)
        font1.setWeight(75)
        self.ui_BTN_close.setFont(font1)

        self.horizontalLayout_7.addWidget(self.ui_BTN_close)


        self.verticalLayout_5.addLayout(self.horizontalLayout_7)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 881, 21))
        self.menuSelect = QMenu(self.menuBar)
        self.menuSelect.setObjectName(u"menuSelect")
        self.menuOptions = QMenu(self.menuBar)
        self.menuOptions.setObjectName(u"menuOptions")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuEdit = QMenu(self.menuBar)
        self.menuEdit.setObjectName(u"menuEdit")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuSelect.menuAction())
        self.menuBar.addAction(self.menuOptions.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.menuSelect.addAction(self.ui_ACT_selectAll)
        self.menuSelect.addAction(self.ui_ACT_deselectAll)
        self.menuSelect.addSeparator()
        self.menuOptions.addAction(self.ui_ACT_useAllTabs)
        self.menuHelp.addAction(self.ui_ACT_showHelp)
        self.menuEdit.addAction(self.ui_ACT_copyFullNamesToClipboard)
        self.menuEdit.addAction(self.ui_ACT_copyShortNamesToClipboard)

        self.retranslateUi(MainWindow)
        self.ui_BTN_catAllOn.clicked.connect(MainWindow.ui_onCatOnOffClicked)
        self.ui_BTN_catAllOff.clicked.connect(MainWindow.ui_onCatOnOffClicked)
        self.ui_BTN_close.clicked.connect(MainWindow.ui_onCloseClicked)
        self.ui_BTN_search.clicked.connect(MainWindow.ui_onSearchClicked)
        self.ui_LED_search.returnPressed.connect(MainWindow.ui_onSearchClicked)
        self.ui_TAB_results.currentChanged.connect(MainWindow.ui_onResultTabChanged)
        self.ui_ACT_useAllTabs.changed.connect(MainWindow.ui_onResultTabChanged)
        self.ui_ACT_showHelp.triggered.connect(MainWindow.ui_onShowHelpClicked)
        self.ui_ACT_selectAll.triggered.connect(MainWindow.ui_onSelectAllClicked)
        self.ui_ACT_deselectAll.triggered.connect(MainWindow.ui_onDeselectAllClicked)
        self.ui_ACT_copyFullNamesToClipboard.triggered.connect(MainWindow.ui_onCopyFullNameClicked)
        self.ui_ACT_copyShortNamesToClipboard.triggered.connect(MainWindow.ui_onCopyShortNameClicked)

        self.ui_STK_results.setCurrentIndex(1)
        self.ui_TAB_results.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Search", None))
        self.ui_ACT_selectAll.setText(QCoreApplication.translate("MainWindow", u"Select All", None))
#if QT_CONFIG(tooltip)
        self.ui_ACT_selectAll.setToolTip(QCoreApplication.translate("MainWindow", u"Select All", None))
#endif // QT_CONFIG(tooltip)
        self.ui_ACT_deselectAll.setText(QCoreApplication.translate("MainWindow", u"Deselect All", None))
#if QT_CONFIG(tooltip)
        self.ui_ACT_deselectAll.setToolTip(QCoreApplication.translate("MainWindow", u"Deselect All", None))
#endif // QT_CONFIG(tooltip)
        self.ui_ACT_useAllTabs.setText(QCoreApplication.translate("MainWindow", u"Use All Tabs", None))
#if QT_CONFIG(tooltip)
        self.ui_ACT_useAllTabs.setToolTip(QCoreApplication.translate("MainWindow", u"Use All Tabs", None))
#endif // QT_CONFIG(tooltip)
        self.ui_ACT_copyFullNamesToClipboard.setText(QCoreApplication.translate("MainWindow", u"Copy Full Names to Clipboard", None))
        self.ui_ACT_copyShortNamesToClipboard.setText(QCoreApplication.translate("MainWindow", u"Copy Short Names to Clipboard", None))
        self.ui_ACT_showHelp.setText(QCoreApplication.translate("MainWindow", u"Help on FX Search", None))
#if QT_CONFIG(tooltip)
        self.ui_ACT_showHelp.setToolTip(QCoreApplication.translate("MainWindow", u"Help on FX Search", None))
#endif // QT_CONFIG(tooltip)
        self.ui_BTN_search.setText("")
#if QT_CONFIG(tooltip)
        self.ui_BTN_soCaseSensitive.setToolTip(QCoreApplication.translate("MainWindow", u"Case Sensitive", None))
#endif // QT_CONFIG(tooltip)
        self.ui_BTN_soCaseSensitive.setText("")
#if QT_CONFIG(tooltip)
        self.ui_BTN_soRegex.setToolTip(QCoreApplication.translate("MainWindow", u"Search by Regular Expression", None))
#endif // QT_CONFIG(tooltip)
        self.ui_BTN_soRegex.setText("")
#if QT_CONFIG(tooltip)
        self.ui_BTN_soSelectFound.setToolTip(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: nowrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Select all Found Objects</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ui_BTN_soSelectFound.setText("")
#if QT_CONFIG(tooltip)
        self.ui_BTN_soIncludeShapes.setToolTip(QCoreApplication.translate("MainWindow", u"Include Shapes in Search", None))
#endif // QT_CONFIG(tooltip)
        self.ui_BTN_soIncludeShapes.setText("")
#if QT_CONFIG(tooltip)
        self.ui_BTN_soSearchSelected.setToolTip(QCoreApplication.translate("MainWindow", u"Search in Selected Objects", None))
#endif // QT_CONFIG(tooltip)
        self.ui_BTN_soSearchSelected.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Search Results", None))
        self.ui_TXT_status.setText(QCoreApplication.translate("MainWindow", u"searching...", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Search Categories", None))
        self.ui_BTN_catAllOn.setText(QCoreApplication.translate("MainWindow", u"All On", None))
        self.ui_BTN_catAllOff.setText(QCoreApplication.translate("MainWindow", u"All Off", None))
        self.ui_BTN_close.setText(QCoreApplication.translate("MainWindow", u"Close", None))
        self.menuSelect.setTitle(QCoreApplication.translate("MainWindow", u"Select", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
    # retranslateUi

