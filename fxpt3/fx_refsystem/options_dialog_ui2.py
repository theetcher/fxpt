# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'options_dialog_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(576, 351)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.uiLST_roots = QListWidget(self.groupBox)
        self.uiLST_roots.setObjectName(u"uiLST_roots")
        self.uiLST_roots.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.uiLST_roots.setAlternatingRowColors(True)
        self.uiLST_roots.setSortingEnabled(True)

        self.verticalLayout.addWidget(self.uiLST_roots)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.uiBTN_add = QPushButton(self.groupBox)
        self.uiBTN_add.setObjectName(u"uiBTN_add")

        self.horizontalLayout.addWidget(self.uiBTN_add)

        self.uiBTN_remove = QPushButton(self.groupBox)
        self.uiBTN_remove.setObjectName(u"uiBTN_remove")

        self.horizontalLayout.addWidget(self.uiBTN_remove)

        self.uiBTN_setActive = QPushButton(self.groupBox)
        self.uiBTN_setActive.setObjectName(u"uiBTN_setActive")

        self.horizontalLayout.addWidget(self.uiBTN_setActive)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMinimumSize(QSize(0, 0))
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        Dialog.finished.connect(Dialog.onDialogFinished)
        Dialog.accepted.connect(Dialog.onDialogAccepted)
        self.uiBTN_add.clicked.connect(Dialog.onAddClicked)
        self.uiBTN_setActive.clicked.connect(Dialog.onSetActiveClicked)
        self.uiLST_roots.itemSelectionChanged.connect(Dialog.onSelectionChanged)
        self.uiBTN_remove.clicked.connect(Dialog.onRemoveClicked)

        self.uiLST_roots.setCurrentRow(-1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"FX RefSystem Options", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"References Location Roots", None))
        self.uiBTN_add.setText(QCoreApplication.translate("Dialog", u"Add", None))
        self.uiBTN_remove.setText(QCoreApplication.translate("Dialog", u"Remove", None))
        self.uiBTN_setActive.setText(QCoreApplication.translate("Dialog", u"Set Active", None))
    # retranslateUi

