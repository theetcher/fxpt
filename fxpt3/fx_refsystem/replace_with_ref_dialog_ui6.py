# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'replace_with_ref_dialog_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGroupBox, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(520, 174)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.uiLBL_text = QLabel(self.groupBox)
        self.uiLBL_text.setObjectName(u"uiLBL_text")
        self.uiLBL_text.setTextFormat(Qt.RichText)
        self.uiLBL_text.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.uiLBL_text.setWordWrap(True)

        self.horizontalLayout.addWidget(self.uiLBL_text)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.uiBTN_saveReplace = QPushButton(Dialog)
        self.uiBTN_saveReplace.setObjectName(u"uiBTN_saveReplace")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiBTN_saveReplace.sizePolicy().hasHeightForWidth())
        self.uiBTN_saveReplace.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.uiBTN_saveReplace)

        self.uiBTN_replace = QPushButton(Dialog)
        self.uiBTN_replace.setObjectName(u"uiBTN_replace")
        sizePolicy.setHeightForWidth(self.uiBTN_replace.sizePolicy().hasHeightForWidth())
        self.uiBTN_replace.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.uiBTN_replace)

        self.uiBTN_cancel = QPushButton(Dialog)
        self.uiBTN_cancel.setObjectName(u"uiBTN_cancel")
        sizePolicy.setHeightForWidth(self.uiBTN_cancel.sizePolicy().hasHeightForWidth())
        self.uiBTN_cancel.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.uiBTN_cancel)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 1)
        self.horizontalLayout_2.setStretch(3, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout.setStretch(0, 1)

        self.retranslateUi(Dialog)
        self.uiBTN_saveReplace.clicked.connect(Dialog.onSaveReplaceClicked)
        self.uiBTN_replace.clicked.connect(Dialog.onReplaceClicked)
        self.uiBTN_cancel.clicked.connect(Dialog.onCancelClicked)
        Dialog.finished.connect(Dialog.onDialogFinished)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Replace With Reference", None))
        self.groupBox.setTitle("")
        self.uiLBL_text.setText(QCoreApplication.translate("Dialog", u"Text", None))
        self.uiBTN_saveReplace.setText(QCoreApplication.translate("Dialog", u"Save and Replace", None))
        self.uiBTN_replace.setText(QCoreApplication.translate("Dialog", u"Replace", None))
        self.uiBTN_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

