# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'log_dialog_ui.ui'
#
# Created: Sat Apr 11 21:48:41 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(777, 147)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.uiTXT_log = QtGui.QPlainTextEdit(Dialog)
        self.uiTXT_log.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.uiTXT_log.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.uiTXT_log.setObjectName("uiTXT_log")
        self.verticalLayout.addWidget(self.uiTXT_log)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.uiBTN_close = QtGui.QPushButton(Dialog)
        self.uiBTN_close.setObjectName("uiBTN_close")
        self.horizontalLayout.addWidget(self.uiBTN_close)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.uiBTN_close, QtCore.SIGNAL("clicked()"), Dialog.accept)
        QtCore.QObject.connect(Dialog, QtCore.SIGNAL("finished(int)"), Dialog.onDialogFinished)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Log", None, QtGui.QApplication.UnicodeUTF8))
        self.uiBTN_close.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

