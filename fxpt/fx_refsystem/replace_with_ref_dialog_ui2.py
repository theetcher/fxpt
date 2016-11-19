# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'replace_with_ref_dialog_ui.ui'
#
# Created: Fri Nov 18 22:58:33 2016
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(520, 174)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.uiLBL_text = QtWidgets.QLabel(self.groupBox)
        self.uiLBL_text.setTextFormat(QtCore.Qt.RichText)
        self.uiLBL_text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.uiLBL_text.setWordWrap(True)
        self.uiLBL_text.setObjectName("uiLBL_text")
        self.horizontalLayout.addWidget(self.uiLBL_text)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.uiBTN_saveReplace = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiBTN_saveReplace.sizePolicy().hasHeightForWidth())
        self.uiBTN_saveReplace.setSizePolicy(sizePolicy)
        self.uiBTN_saveReplace.setObjectName("uiBTN_saveReplace")
        self.horizontalLayout_2.addWidget(self.uiBTN_saveReplace)
        self.uiBTN_replace = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiBTN_replace.sizePolicy().hasHeightForWidth())
        self.uiBTN_replace.setSizePolicy(sizePolicy)
        self.uiBTN_replace.setObjectName("uiBTN_replace")
        self.horizontalLayout_2.addWidget(self.uiBTN_replace)
        self.uiBTN_cancel = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiBTN_cancel.sizePolicy().hasHeightForWidth())
        self.uiBTN_cancel.setSizePolicy(sizePolicy)
        self.uiBTN_cancel.setObjectName("uiBTN_cancel")
        self.horizontalLayout_2.addWidget(self.uiBTN_cancel)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.uiBTN_saveReplace, QtCore.SIGNAL("clicked()"), Dialog.onSaveReplaceClicked)
        QtCore.QObject.connect(self.uiBTN_replace, QtCore.SIGNAL("clicked()"), Dialog.onReplaceClicked)
        QtCore.QObject.connect(self.uiBTN_cancel, QtCore.SIGNAL("clicked()"), Dialog.onCancelClicked)
        QtCore.QObject.connect(Dialog, QtCore.SIGNAL("finished(int)"), Dialog.onDialogFinished)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Replace With Reference", None, -1))
        self.uiLBL_text.setText(QtWidgets.QApplication.translate("Dialog", "Text", None, -1))
        self.uiBTN_saveReplace.setText(QtWidgets.QApplication.translate("Dialog", "Save and Replace", None, -1))
        self.uiBTN_replace.setText(QtWidgets.QApplication.translate("Dialog", "Replace", None, -1))
        self.uiBTN_cancel.setText(QtWidgets.QApplication.translate("Dialog", "Cancel", None, -1))

