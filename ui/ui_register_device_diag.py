# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_register_device_diag.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize)
from PySide6.QtWidgets import (QHBoxLayout, QLabel,
                               QLineEdit, QPushButton, QSizePolicy, QVBoxLayout)


class Ui_diag_register_device(object):
    def setupUi(self, diag_register_device):
        if not diag_register_device.objectName():
            diag_register_device.setObjectName(u"diag_register_device")
        diag_register_device.resize(260, 220)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(diag_register_device.sizePolicy().hasHeightForWidth())
        diag_register_device.setSizePolicy(sizePolicy)
        diag_register_device.setMinimumSize(QSize(260, 220))
        diag_register_device.setMaximumSize(QSize(260, 220))
        self.verticalLayout_3 = QVBoxLayout(diag_register_device)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 23, -1, 40)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.name_label = QLabel(diag_register_device)
        self.name_label.setObjectName(u"name_label")

        self.verticalLayout_2.addWidget(self.name_label)

        self.cmd_label = QLabel(diag_register_device)
        self.cmd_label.setObjectName(u"cmd_label")

        self.verticalLayout_2.addWidget(self.cmd_label)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.diag_input_serial = QLineEdit(diag_register_device)
        self.diag_input_serial.setObjectName(u"diag_input_serial")
        self.diag_input_serial.setMinimumSize(QSize(0, 30))
        self.diag_input_serial.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout.addWidget(self.diag_input_serial)

        self.diag_input_note = QLineEdit(diag_register_device)
        self.diag_input_note.setObjectName(u"diag_input_note")
        self.diag_input_note.setMinimumSize(QSize(0, 30))
        self.diag_input_note.setMaximumSize(QSize(16777215, 30))

        self.verticalLayout.addWidget(self.diag_input_note)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_cancel_device = QPushButton(diag_register_device)
        self.btn_cancel_device.setObjectName(u"btn_cancel_device")
        self.btn_cancel_device.setMinimumSize(QSize(0, 30))
        self.btn_cancel_device.setMaximumSize(QSize(16777215, 30))
        self.btn_cancel_device.setFlat(False)

        self.horizontalLayout_2.addWidget(self.btn_cancel_device)

        self.btn_register_device = QPushButton(diag_register_device)
        self.btn_register_device.setObjectName(u"btn_register_device")
        self.btn_register_device.setMinimumSize(QSize(0, 30))
        self.btn_register_device.setMaximumSize(QSize(16777215, 30))

        self.horizontalLayout_2.addWidget(self.btn_register_device)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(diag_register_device)

        QMetaObject.connectSlotsByName(diag_register_device)

    # setupUi

    def retranslateUi(self, diag_register_device):
        diag_register_device.setWindowTitle(
            QCoreApplication.translate("diag_register_device", u"\u767b\u8bb0\u65b0\u8bbe\u5907", None))
        self.name_label.setText(QCoreApplication.translate("diag_register_device", u"\u5e8f\u5217\u53f7\uff1a", None))
        self.cmd_label.setText(
            QCoreApplication.translate("diag_register_device", u"\u5907\u6ce8\u4fe1\u606f\uff1a", None))
        self.diag_input_serial.setPlaceholderText(QCoreApplication.translate("diag_register_device",
                                                                             u"\u901a\u8fc7adb devices\u67e5\u8be2\u7684\u5e8f\u5217\u53f7",
                                                                             None))
        self.diag_input_note.setPlaceholderText(QCoreApplication.translate("diag_register_device",
                                                                           u"\u8f93\u5165\u8bbe\u5907\u578b\u53f7\uff0c\u81ea\u5b9a\u4e49\u7f16\u53f7\u7b49",
                                                                           None))
        self.btn_cancel_device.setText(QCoreApplication.translate("diag_register_device", u"\u53d6\u6d88", None))
        self.btn_register_device.setText(QCoreApplication.translate("diag_register_device", u"\u6ce8\u518c", None))
    # retranslateUi
