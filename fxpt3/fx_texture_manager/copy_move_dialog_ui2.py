# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'copy_move_dialog_ui.ui'
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
        Dialog.resize(857, 320)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QSize(16777215, 320))
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_2 = QGroupBox(Dialog)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout = QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(6)
        self.gridLayout_3.setVerticalSpacing(4)
        self.uiCHK_deleteSources = QCheckBox(self.groupBox_2)
        self.uiCHK_deleteSources.setObjectName(u"uiCHK_deleteSources")
        self.uiCHK_deleteSources.setMinimumSize(QSize(0, 20))

        self.gridLayout_3.addWidget(self.uiCHK_deleteSources, 2, 1, 1, 1)

        self.uiBTN_browseTarget = QToolButton(self.groupBox_2)
        self.uiBTN_browseTarget.setObjectName(u"uiBTN_browseTarget")
        icon = QIcon()
        icon.addFile(u":/icons/folder.png", QSize(), QIcon.Normal, QIcon.Off)
        self.uiBTN_browseTarget.setIcon(icon)
        self.uiBTN_browseTarget.setIconSize(QSize(18, 18))

        self.gridLayout_3.addWidget(self.uiBTN_browseTarget, 0, 2, 1, 1)

        self.uiLED_targetRoot = LineEditPath(self.groupBox_2)
        self.uiLED_targetRoot.setObjectName(u"uiLED_targetRoot")

        self.gridLayout_3.addWidget(self.uiLED_targetRoot, 0, 1, 1, 1)

        self.label_10 = QLabel(self.groupBox_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.label_10, 0, 0, 1, 1)

        self.uiCHK_retarget = QCheckBox(self.groupBox_2)
        self.uiCHK_retarget.setObjectName(u"uiCHK_retarget")
        self.uiCHK_retarget.setMinimumSize(QSize(0, 20))

        self.gridLayout_3.addWidget(self.uiCHK_retarget, 1, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.uiGRP_folderStructure = QGroupBox(self.groupBox_2)
        self.uiGRP_folderStructure.setObjectName(u"uiGRP_folderStructure")
        self.uiGRP_folderStructure.setCheckable(True)
        self.gridLayout = QGridLayout(self.uiGRP_folderStructure)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.uiLED_sourceRoot = LineEditPath(self.uiGRP_folderStructure)
        self.uiLED_sourceRoot.setObjectName(u"uiLED_sourceRoot")

        self.gridLayout.addWidget(self.uiLED_sourceRoot, 0, 1, 1, 1)

        self.uiBTN_browseSource = QToolButton(self.uiGRP_folderStructure)
        self.uiBTN_browseSource.setObjectName(u"uiBTN_browseSource")
        self.uiBTN_browseSource.setIcon(icon)
        self.uiBTN_browseSource.setIconSize(QSize(18, 18))

        self.gridLayout.addWidget(self.uiBTN_browseSource, 0, 2, 1, 1)

        self.label_16 = QLabel(self.uiGRP_folderStructure)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_16, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.uiGRP_folderStructure)

        self.uiGRP_addTextures = QGroupBox(self.groupBox_2)
        self.uiGRP_addTextures.setObjectName(u"uiGRP_addTextures")
        self.uiGRP_addTextures.setCheckable(True)
        self.gridLayout_2 = QGridLayout(self.uiGRP_addTextures)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_22 = QLabel(self.uiGRP_addTextures)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_22, 0, 0, 1, 1)

        self.uiLED_texSuffixes = QLineEdit(self.uiGRP_addTextures)
        self.uiLED_texSuffixes.setObjectName(u"uiLED_texSuffixes")

        self.gridLayout_2.addWidget(self.uiLED_texSuffixes, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.uiGRP_addTextures)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
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

        self.groupBox_2.raise_()
        QWidget.setTabOrder(self.uiBTN_cancel, self.uiBTN_ok)

        self.retranslateUi(Dialog)
        self.uiBTN_cancel.clicked.connect(Dialog.reject)
        Dialog.finished.connect(Dialog.onDialogFinished)
        self.uiBTN_ok.clicked.connect(Dialog.onOkClicked)
        self.uiBTN_browseTarget.clicked.connect(Dialog.onBrowseTargetClicked)
        self.uiBTN_browseSource.clicked.connect(Dialog.onBrowseSourceClicked)
        self.uiLED_sourceRoot.editingFinished.connect(Dialog.onValidateUiNeeded)
        self.uiLED_targetRoot.editingFinished.connect(Dialog.onValidateUiNeeded)
        self.uiGRP_folderStructure.clicked.connect(Dialog.onValidateUiNeeded)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Copy and Move", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Dialog", u"Parameters", None))
        self.uiCHK_deleteSources.setText(QCoreApplication.translate("Dialog", u"Delete sources", None))
        self.uiBTN_browseTarget.setText(QCoreApplication.translate("Dialog", u"...", None))
#if QT_CONFIG(shortcut)
        self.uiBTN_browseTarget.setShortcut(QCoreApplication.translate("Dialog", u"Ctrl+S, Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.label_10.setText(QCoreApplication.translate("Dialog", u"Copy to:", None))
        self.uiCHK_retarget.setText(QCoreApplication.translate("Dialog", u"Retarget", None))
        self.uiGRP_folderStructure.setTitle(QCoreApplication.translate("Dialog", u"Copy folder structure", None))
        self.uiBTN_browseSource.setText(QCoreApplication.translate("Dialog", u"...", None))
#if QT_CONFIG(shortcut)
        self.uiBTN_browseSource.setShortcut(QCoreApplication.translate("Dialog", u"Ctrl+S, Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.label_16.setText(QCoreApplication.translate("Dialog", u"Original root folder:", None))
        self.uiGRP_addTextures.setTitle(QCoreApplication.translate("Dialog", u"Copy additional textures", None))
        self.label_22.setText(QCoreApplication.translate("Dialog", u"Texture suffixes:", None))
        self.uiLED_texSuffixes.setText(QCoreApplication.translate("Dialog", u"_nm, _spec, _hdetm, _em", None))
        self.uiLBL_status.setText("")
        self.uiBTN_ok.setText(QCoreApplication.translate("Dialog", u"OK", None))
        self.uiBTN_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

