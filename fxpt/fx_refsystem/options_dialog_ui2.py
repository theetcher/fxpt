# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'options_dialog_ui.ui'
#
# Created: Fri Nov 18 22:58:33 2016
#      by: pyside2-uic  running on PySide2 2.0.0~alpha0
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(576, 351)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.uiLST_roots = QtWidgets.QListWidget(self.groupBox)
        self.uiLST_roots.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.uiLST_roots.setAlternatingRowColors(True)
        self.uiLST_roots.setObjectName("uiLST_roots")
        self.verticalLayout.addWidget(self.uiLST_roots)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.uiBTN_add = QtWidgets.QPushButton(self.groupBox)
        self.uiBTN_add.setObjectName("uiBTN_add")
        self.horizontalLayout.addWidget(self.uiBTN_add)
        self.uiBTN_remove = QtWidgets.QPushButton(self.groupBox)
        self.uiBTN_remove.setObjectName("uiBTN_remove")
        self.horizontalLayout.addWidget(self.uiBTN_remove)
        self.uiBTN_setActive = QtWidgets.QPushButton(self.groupBox)
        self.uiBTN_setActive.setObjectName("uiBTN_setActive")
        self.horizontalLayout.addWidget(self.uiBTN_setActive)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setMinimumSize(QtCore.QSize(0, 0))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.uiLST_roots.setCurrentRow(-1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QObject.connect(Dialog, QtCore.SIGNAL("finished(int)"), Dialog.onDialogFinished)
        QtCore.QObject.connect(Dialog, QtCore.SIGNAL("accepted()"), Dialog.onDialogAccepted)
        QtCore.QObject.connect(self.uiBTN_add, QtCore.SIGNAL("clicked()"), Dialog.onAddClicked)
        QtCore.QObject.connect(self.uiBTN_setActive, QtCore.SIGNAL("clicked()"), Dialog.onSetActiveClicked)
        QtCore.QObject.connect(self.uiLST_roots, QtCore.SIGNAL("itemSelectionChanged()"), Dialog.onSelectionChanged)
        QtCore.QObject.connect(self.uiBTN_remove, QtCore.SIGNAL("clicked()"), Dialog.onRemoveClicked)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "FX RefSystem Options", None, -1))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("Dialog", "References Location Roots", None, -1))
        self.uiLST_roots.setSortingEnabled(True)
        self.uiBTN_add.setText(QtWidgets.QApplication.translate("Dialog", "Add", None, -1))
        self.uiBTN_remove.setText(QtWidgets.QApplication.translate("Dialog", "Remove", None, -1))
        self.uiBTN_setActive.setText(QtWidgets.QApplication.translate("Dialog", "Set Active", None, -1))

