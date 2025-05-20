# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QTabWidget, QTextBrowser, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(350, 650)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(350, 650))
        MainWindow.setMaximumSize(QSize(350, 650))
        self.actionAddDevice = QAction(MainWindow)
        self.actionAddDevice.setObjectName(u"actionAddDevice")
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.action_import_devices = QAction(MainWindow)
        self.action_import_devices.setObjectName(u"action_import_devices")
        self.actionAddCommand = QAction(MainWindow)
        self.actionAddCommand.setObjectName(u"actionAddCommand")
        self.action_export_commands = QAction(MainWindow)
        self.action_export_commands.setObjectName(u"action_export_commands")
        self.action_import_commands = QAction(MainWindow)
        self.action_import_commands.setObjectName(u"action_import_commands")
        self.actionOpenLocalCfg = QAction(MainWindow)
        self.actionOpenLocalCfg.setObjectName(u"actionOpenLocalCfg")
        self.actionExportCfgToLocal = QAction(MainWindow)
        self.actionExportCfgToLocal.setObjectName(u"actionExportCfgToLocal")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tab_widget = QTabWidget(self.centralwidget)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_widget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab_device = QWidget()
        self.tab_device.setObjectName(u"tab_device")
        self.tab_device.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.verticalLayout_3 = QVBoxLayout(self.tab_device)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.tab_device)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.label_device_count = QLabel(self.tab_device)
        self.label_device_count.setObjectName(u"label_device_count")

        self.horizontalLayout.addWidget(self.label_device_count)

        self.btn_refresh_online_device = QPushButton(self.tab_device)
        self.btn_refresh_online_device.setObjectName(u"btn_refresh_online_device")

        self.horizontalLayout.addWidget(self.btn_refresh_online_device)

        self.btn_register_device = QPushButton(self.tab_device)
        self.btn_register_device.setObjectName(u"btn_register_device")

        self.horizontalLayout.addWidget(self.btn_register_device)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.device_tree_widget = QTreeWidget(self.tab_device)
        self.device_tree_widget.setObjectName(u"device_tree_widget")
        self.device_tree_widget.setMinimumSize(QSize(305, 350))
        self.device_tree_widget.setMaximumSize(QSize(305, 16777215))
        self.device_tree_widget.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.device_tree_widget.setColumnCount(3)
        self.device_tree_widget.header().setVisible(False)
        self.device_tree_widget.header().setCascadingSectionResizes(False)
        self.device_tree_widget.header().setHighlightSections(False)

        self.verticalLayout_2.addWidget(self.device_tree_widget)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.tab_widget.addTab(self.tab_device, "")
        self.tab_cmd = QWidget()
        self.tab_cmd.setObjectName(u"tab_cmd")
        self.verticalLayout_5 = QVBoxLayout(self.tab_cmd)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_cmd = QLineEdit(self.tab_cmd)
        self.lineEdit_cmd.setObjectName(u"lineEdit_cmd")

        self.horizontalLayout_2.addWidget(self.lineEdit_cmd)

        self.btn_direct_run = QPushButton(self.tab_cmd)
        self.btn_direct_run.setObjectName(u"btn_direct_run")

        self.horizontalLayout_2.addWidget(self.btn_direct_run)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btn_add_new_group = QPushButton(self.tab_cmd)
        self.btn_add_new_group.setObjectName(u"btn_add_new_group")

        self.horizontalLayout_3.addWidget(self.btn_add_new_group)

        self.btn_add_cmd = QPushButton(self.tab_cmd)
        self.btn_add_cmd.setObjectName(u"btn_add_cmd")

        self.horizontalLayout_3.addWidget(self.btn_add_cmd)

        self.btn_stop_cmd = QPushButton(self.tab_cmd)
        self.btn_stop_cmd.setObjectName(u"btn_stop_cmd")

        self.horizontalLayout_3.addWidget(self.btn_stop_cmd)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.line = QFrame(self.tab_cmd)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.cmd_tab_widget = QTabWidget(self.tab_cmd)
        self.cmd_tab_widget.setObjectName(u"cmd_tab_widget")
        self.cmd_table_default = QWidget()
        self.cmd_table_default.setObjectName(u"cmd_table_default")
        self.cmd_tab_widget.addTab(self.cmd_table_default, "")

        self.verticalLayout_4.addWidget(self.cmd_tab_widget)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        self.tab_widget.addTab(self.tab_cmd, "")

        self.verticalLayout.addWidget(self.tab_widget)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btn_clear_log = QPushButton(self.centralwidget)
        self.btn_clear_log.setObjectName(u"btn_clear_log")
        self.btn_clear_log.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_4.addWidget(self.btn_clear_log)

        self.btn_pop_log = QPushButton(self.centralwidget)
        self.btn_pop_log.setObjectName(u"btn_pop_log")
        self.btn_pop_log.setMaximumSize(QSize(100, 60))

        self.horizontalLayout_4.addWidget(self.btn_pop_log)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.output_text_browser = QTextBrowser(self.centralwidget)
        self.output_text_browser.setObjectName(u"output_text_browser")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.output_text_browser.sizePolicy().hasHeightForWidth())
        self.output_text_browser.setSizePolicy(sizePolicy1)
        self.output_text_browser.setMinimumSize(QSize(0, 0))
        self.output_text_browser.setMaximumSize(QSize(16777215, 150))

        self.verticalLayout.addWidget(self.output_text_browser)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tab_widget.setCurrentIndex(0)
        self.cmd_tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Android\u8bbe\u5907\u6279\u91cf\u64cd\u4f5c\u5de5\u5177", None))
        self.actionAddDevice.setText(QCoreApplication.translate("MainWindow", u"\u767b\u8bb0\u8bbe\u5907", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u8bbe\u5907\u5217\u8868", None))
        self.action_import_devices.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u8bbe\u5907\u5217\u8868", None))
        self.actionAddCommand.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u65b0\u547d\u4ee4", None))
        self.action_export_commands.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u547d\u4ee4\u5217\u8868", None))
        self.action_import_commands.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u547d\u4ee4\u5217\u8868", None))
        self.actionOpenLocalCfg.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u914d\u7f6e\u6587\u4ef6\u8def\u5f84", None))
        self.actionExportCfgToLocal.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u914d\u7f6e\u5230\u672c\u5730", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u5728\u7ebf\u8bbe\u5907\uff1a", None))
        self.label_device_count.setText("")
        self.btn_refresh_online_device.setText(QCoreApplication.translate("MainWindow", u"\u5237\u65b0\u5728\u7ebf\u8bbe\u5907", None))
        self.btn_register_device.setText(QCoreApplication.translate("MainWindow", u"\u767b\u8bb0\u65b0\u8bbe\u5907", None))
        ___qtreewidgetitem = self.device_tree_widget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"\u5907\u6ce8", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"\u5e8f\u5217\u53f7", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u5206\u7c7b", None));
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_device), QCoreApplication.translate("MainWindow", u"\u8bbe\u5907\u7ba1\u7406", None))
        self.btn_direct_run.setText(QCoreApplication.translate("MainWindow", u"\u76f4\u63a5\u4e0b\u53d1", None))
        self.btn_add_new_group.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u65b0\u5206\u7ec4", None))
        self.btn_add_cmd.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u65b0\u6309\u94ae", None))
        self.btn_stop_cmd.setText(QCoreApplication.translate("MainWindow", u"\u505c\u6b62\u963b\u585e\u5f0f\u547d\u4ee4", None))
        self.cmd_tab_widget.setTabText(self.cmd_tab_widget.indexOf(self.cmd_table_default), QCoreApplication.translate("MainWindow", u"\u9ed8\u8ba4\u5206\u7ec4", None))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.tab_cmd), QCoreApplication.translate("MainWindow", u"\u547d\u4ee4\u7ba1\u7406", None))
        self.btn_clear_log.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u9664\u65e5\u5fd7", None))
        self.btn_pop_log.setText(QCoreApplication.translate("MainWindow", u"\u5f39\u51fa\u65e5\u5fd7\u6846", None))
    # retranslateUi

