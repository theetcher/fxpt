# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'retarget_dialog_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from . line_edit_path import LineEditPath

from  . import resources_rc2

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(614, 250)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QSize(16777215, 250))
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(4)
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.uiLED_retargetRoot = LineEditPath(self.groupBox)
        self.uiLED_retargetRoot.setObjectName(u"uiLED_retargetRoot")

        self.gridLayout.addWidget(self.uiLED_retargetRoot, 0, 1, 1, 1)

        self.uiCHK_forceRetarget = QCheckBox(self.groupBox)
        self.uiCHK_forceRetarget.setObjectName(u"uiCHK_forceRetarget")
        self.uiCHK_forceRetarget.setMinimumSize(QSize(0, 20))

        self.gridLayout.addWidget(self.uiCHK_forceRetarget, 1, 1, 1, 1)

        self.uiBTN_browse = QToolButton(self.groupBox)
        self.uiBTN_browse.setObjectName(u"uiBTN_browse")
        icon = QIcon()
        icon.addFile(u":/icons/folder.png", QSize(), QIcon.Normal, QIcon.Off)
        self.uiBTN_browse.setIcon(icon)
        self.uiBTN_browse.setIconSize(QSize(18, 18))

        self.gridLayout.addWidget(self.uiBTN_browse, 0, 2, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.uiGRP_useSourceRoot = QGroupBox(self.groupBox)
        self.uiGRP_useSourceRoot.setObjectName(u"uiGRP_useSourceRoot")
        self.uiGRP_useSourceRoot.setCheckable(True)
        self.gridLayout_2 = QGridLayout(self.uiGRP_useSourceRoot)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.uiLED_sourceRoot = LineEditPath(self.uiGRP_useSourceRoot)
        self.uiLED_sourceRoot.setObjectName(u"uiLED_sourceRoot")

        self.gridLayout_2.addWidget(self.uiLED_sourceRoot, 0, 1, 1, 1)

        self.uiBTN_browseSource = QToolButton(self.uiGRP_useSourceRoot)
        self.uiBTN_browseSource.setObjectName(u"uiBTN_browseSource")
        self.uiBTN_browseSource.setIcon(icon)
        self.uiBTN_browseSource.setIconSize(QSize(18, 18))

        self.gridLayout_2.addWidget(self.uiBTN_browseSource, 0, 2, 1, 1)

        self.label_16 = QLabel(self.uiGRP_useSourceRoot)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_16, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.uiGRP_useSourceRoot)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.uiLBL_status = QLabel(Dialog)
        self.uiLBL_status.setObjectName(u"uiLBL_status")
        self.uiLBL_status.setStyleSheet(u"QLabel {color : red}")

        self.horizontalLayout_2.addWidget(self.uiLBL_status)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.uiBTN_ok = QPushButton(Dialog)
        self.uiBTN_ok.setObjectName(u"uiBTN_ok")

        self.horizontalLayout_2.addWidget(self.uiBTN_ok)

        self.uiBTN_cancel = QPushButton(Dialog)
        self.uiBTN_cancel.setObjectName(u"uiBTN_cancel")

        self.horizontalLayout_2.addWidget(self.uiBTN_cancel)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        QWidget.setTabOrder(self.uiLED_retargetRoot, self.uiBTN_browse)
        QWidget.setTabOrder(self.uiBTN_browse, self.uiBTN_cancel)
        QWidget.setTabOrder(self.uiBTN_cancel, self.uiCHK_forceRetarget)
        QWidget.setTabOrder(self.uiCHK_forceRetarget, self.uiBTN_ok)

        self.retranslateUi(Dialog)
        self.uiBTN_cancel.clicked.connect(Dialog.reject)
        self.uiBTN_browse.clicked.connect(Dialog.onBrowseClicked)
        Dialog.finished.connect(Dialog.onDialogFinished)
        self.uiLED_retargetRoot.editingFinished.connect(Dialog.onValidateUiNeeded)
        self.uiBTN_ok.clicked.connect(Dialog.onOkClicked)
        self.uiBTN_browseSource.clicked.connect(Dialog.onBrowseSourceClicked)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Retarget", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"Parameters", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Retarget to:", None))
        self.uiCHK_forceRetarget.setText(QCoreApplication.translate("Dialog", u"Force retarget", None))
        self.uiBTN_browse.setText(QCoreApplication.translate("Dialog", u"...", None))
#if QT_CONFIG(shortcut)
        self.uiBTN_browse.setShortcut(QCoreApplication.translate("Dialog", u"Ctrl+S, Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.uiGRP_useSourceRoot.setTitle(QCoreApplication.translate("Dialog", u"Use source root", None))
        self.uiBTN_browseSource.setText(QCoreApplication.translate("Dialog", u"...", None))
#if QT_CONFIG(shortcut)
        self.uiBTN_browseSource.setShortcut(QCoreApplication.translate("Dialog", u"Ctrl+S, Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Source root folder:", None))
        self.uiLBL_status.setText("")
        self.uiBTN_ok.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.uiBTN_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

