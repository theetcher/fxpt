# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log_dialog_ui.ui'
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
        Dialog.resize(819, 504)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.uiTXT_log = QPlainTextEdit(Dialog)
        self.uiTXT_log.setObjectName(u"uiTXT_log")
        self.uiTXT_log.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.uiTXT_log.setTextInteractionFlags(Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.uiTXT_log)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.uiBTN_close = QPushButton(Dialog)
        self.uiBTN_close.setObjectName(u"uiBTN_close")

        self.horizontalLayout.addWidget(self.uiBTN_close)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Dialog)
        self.uiBTN_close.clicked.connect(Dialog.accept)
        Dialog.finished.connect(Dialog.onDialogFinished)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Log", None))
        self.uiBTN_close.setText(QCoreApplication.translate("Dialog", u"Close", None))
    # retranslateUi

