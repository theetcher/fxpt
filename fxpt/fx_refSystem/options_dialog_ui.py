# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'options_dialog_ui.ui'
#
# Created: Fri Apr 10 14:46:28 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(576, 351)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.uiLST_roots = QtGui.QListWidget(self.groupBox)
        self.uiLST_roots.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.uiLST_roots.setAlternatingRowColors(True)
        self.uiLST_roots.setObjectName("uiLST_roots")
        self.verticalLayout.addWidget(self.uiLST_roots)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.uiBTN_add = QtGui.QPushButton(self.groupBox)
        self.uiBTN_add.setObjectName("uiBTN_add")
        self.horizontalLayout.addWidget(self.uiBTN_add)
        self.uiBTN_remove = QtGui.QPushButton(self.groupBox)
        self.uiBTN_remove.setObjectName("uiBTN_remove")
        self.horizontalLayout.addWidget(self.uiBTN_remove)
        self.uiBTN_setActive = QtGui.QPushButton(self.groupBox)
        self.uiBTN_setActive.setObjectName("uiBTN_setActive")
        self.horizontalLayout.addWidget(self.uiBTN_setActive)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setMinimumSize(QtCore.QSize(0, 0))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
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
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "FX RefSystem Options", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "References Location Roots", None, QtGui.QApplication.UnicodeUTF8))
        self.uiLST_roots.setSortingEnabled(True)
        self.uiBTN_add.setText(QtGui.QApplication.translate("Dialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.uiBTN_remove.setText(QtGui.QApplication.translate("Dialog", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.uiBTN_setActive.setText(QtGui.QApplication.translate("Dialog", "Set Active", None, QtGui.QApplication.UnicodeUTF8))

