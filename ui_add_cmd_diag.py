# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_add_cmd_diag.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_AddCommandDialog(object):
    def setupUi(self, AddCommandDialog):
        if not AddCommandDialog.objectName():
            AddCommandDialog.setObjectName(u"AddCommandDialog")
        AddCommandDialog.resize(260, 220)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddCommandDialog.sizePolicy().hasHeightForWidth())
        AddCommandDialog.setSizePolicy(sizePolicy)
        AddCommandDialog.setMinimumSize(QSize(260, 220))
        AddCommandDialog.setMaximumSize(QSize(260, 220))
        self.verticalLayout = QVBoxLayout(AddCommandDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.radio_block_no = QRadioButton(AddCommandDialog)
        self.radio_block_no.setObjectName(u"radio_block_no")
        self.radio_block_no.setMinimumSize(QSize(0, 30))
        self.radio_block_no.setMaximumSize(QSize(16777215, 30))
        self.radio_block_no.setChecked(True)

        self.gridLayout.addWidget(self.radio_block_no, 2, 3, 1, 1)

        self.color_label = QLabel(AddCommandDialog)
        self.color_label.setObjectName(u"color_label")

        self.gridLayout.addWidget(self.color_label, 3, 0, 1, 1)

        self.btn_save_cmd = QPushButton(AddCommandDialog)
        self.btn_save_cmd.setObjectName(u"btn_save_cmd")
        self.btn_save_cmd.setMinimumSize(QSize(0, 30))
        self.btn_save_cmd.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.btn_save_cmd, 4, 2, 1, 2)

        self.radio_block_yes = QRadioButton(AddCommandDialog)
        self.radio_block_yes.setObjectName(u"radio_block_yes")

        self.gridLayout.addWidget(self.radio_block_yes, 2, 2, 1, 1)

        self.btn_cancel_cmd = QPushButton(AddCommandDialog)
        self.btn_cancel_cmd.setObjectName(u"btn_cancel_cmd")
        self.btn_cancel_cmd.setMinimumSize(QSize(0, 30))
        self.btn_cancel_cmd.setMaximumSize(QSize(16777215, 30))
        self.btn_cancel_cmd.setFlat(False)

        self.gridLayout.addWidget(self.btn_cancel_cmd, 4, 0, 1, 2)

        self.diag_input_btn_name = QLineEdit(AddCommandDialog)
        self.diag_input_btn_name.setObjectName(u"diag_input_btn_name")
        self.diag_input_btn_name.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.diag_input_btn_name, 0, 1, 1, 3)

        self.diag_input_adb = QLineEdit(AddCommandDialog)
        self.diag_input_adb.setObjectName(u"diag_input_adb")
        self.diag_input_adb.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.diag_input_adb, 1, 1, 1, 3)

        self.cmd_label = QLabel(AddCommandDialog)
        self.cmd_label.setObjectName(u"cmd_label")

        self.gridLayout.addWidget(self.cmd_label, 1, 0, 1, 1)

        self.name_label = QLabel(AddCommandDialog)
        self.name_label.setObjectName(u"name_label")

        self.gridLayout.addWidget(self.name_label, 0, 0, 1, 1)

        self.label = QLabel(AddCommandDialog)
        self.label.setObjectName(u"label")
        self.label.setToolTipDuration(-1)

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.btn_choose_color = QPushButton(AddCommandDialog)
        self.btn_choose_color.setObjectName(u"btn_choose_color")
        self.btn_choose_color.setMinimumSize(QSize(0, 30))
        self.btn_choose_color.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.btn_choose_color, 3, 1, 1, 3)

        self.label_2 = QLabel(AddCommandDialog)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(AddCommandDialog)

        QMetaObject.connectSlotsByName(AddCommandDialog)
    # setupUi

    def retranslateUi(self, AddCommandDialog):
        AddCommandDialog.setWindowTitle(QCoreApplication.translate("AddCommandDialog", u"\u6dfb\u52a0\u547d\u4ee4", None))
        self.radio_block_no.setText(QCoreApplication.translate("AddCommandDialog", u"\u5426", None))
        self.color_label.setText(QCoreApplication.translate("AddCommandDialog", u"\u6309\u94ae\u989c\u8272\uff1a", None))
        self.btn_save_cmd.setText(QCoreApplication.translate("AddCommandDialog", u"\u6dfb\u52a0", None))
        self.radio_block_yes.setText(QCoreApplication.translate("AddCommandDialog", u"\u662f", None))
        self.btn_cancel_cmd.setText(QCoreApplication.translate("AddCommandDialog", u"\u53d6\u6d88", None))
        self.cmd_label.setText(QCoreApplication.translate("AddCommandDialog", u"ADB\u547d\u4ee4\uff1a", None))
        self.name_label.setText(QCoreApplication.translate("AddCommandDialog", u"\u6309\u94ae\u540d\u79f0\uff1a", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("AddCommandDialog", u"\u5982adb logcat\u8fd9\u7c7b\u6301\u7eed\u8f93\u51fa\u7684\u547d\u4ee4", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.label.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.label.setText(QCoreApplication.translate("AddCommandDialog", u"\u963b\u585e\u5f0f\u547d\u4ee4\uff1a", None))
        self.btn_choose_color.setText(QCoreApplication.translate("AddCommandDialog", u"\u9009\u62e9\u989c\u8272", None))
        self.label_2.setText("")
    # retranslateUi

