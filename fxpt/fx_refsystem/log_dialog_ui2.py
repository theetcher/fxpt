# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'log_dialog_ui.ui'
#
# Created: Fri Nov 18 22:58:33 2016
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(777, 147)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.uiTXT_log = QtWidgets.QPlainTextEdit(Dialog)
        self.uiTXT_log.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.uiTXT_log.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.uiTXT_log.setObjectName("uiTXT_log")
        self.verticalLayout.addWidget(self.uiTXT_log)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.uiBTN_close = QtWidgets.QPushButton(Dialog)
        self.uiBTN_close.setObjectName("uiBTN_close")
        self.horizontalLayout.addWidget(self.uiBTN_close)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.uiBTN_close, QtCore.SIGNAL("clicked()"), Dialog.accept)
        QtCore.QObject.connect(Dialog, QtCore.SIGNAL("finished(int)"), Dialog.onDialogFinished)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Log", None, -1))
        self.uiBTN_close.setText(QtWidgets.QApplication.translate("Dialog", "Close", None, -1))

