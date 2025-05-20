import sys
import os
import csv
import subprocess
import threading
import asyncio
from datetime import datetime
from typing import override

from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QInputDialog, QTreeWidgetItem, QMenu, QWidget,
                               QVBoxLayout, QPushButton, QDialog, QColorDialog, QGridLayout, QTextBrowser, QHBoxLayout)
from PySide6.QtCore import Qt, QThread, Signal, QSize
from ui_main_window import Ui_MainWindow
from ui_register_device_diag import Ui_diag_register_device
from ui_add_cmd_diag import Ui_AddCommandDialog


class RegisterDeviceDialog(QDialog):
    device_registered = Signal()  # 添加信号

    def __init__(self, parent=None, serial=None):
        super().__init__(parent)
        self.ui = Ui_diag_register_device()
        self.ui.setupUi(self)
        self.ui.btn_register_device.clicked.connect(self.accept)
        self.ui.btn_cancel_device.clicked.connect(self.reject)
        self.main_window = parent
        if serial:
            self.ui.diag_input_serial.setText(serial)

    @override
    def accept(self):
        serial = self.ui.diag_input_serial.text()
        note = self.ui.diag_input_note.text()

        if not serial:
            QMessageBox.warning(self, "警告", "设备序列号不能为空")
            return
        if not note:
            QMessageBox.warning(self, "警告", "备注信息不能为空")
            return

        # 检查序列号是否已登记
        if serial in self.main_window.registered_devices:
            QMessageBox.warning(self, "警告",
                                f"设备序列号 {serial} 已经登记过，如需修改备注信息，可采用如下方法：\n1.连接设备，右键修改设备信息\n2.连接设备，右键删除设备信息，重新登记\n3"
                                f".修改本地devices.csv文件，点击刷新在线设备")
            return

        self.main_window.registered_devices[serial] = note
        self.main_window.save_devices()

        # 发送信号通知主窗口刷新设备列表
        self.device_registered.emit()

        super().accept()


class AddCmdDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_AddCommandDialog()
        self.ui.setupUi(self)
        self.ui.btn_save_cmd.clicked.connect(self.accept)
        self.ui.btn_cancel_cmd.clicked.connect(self.reject)
        self.ui.btn_choose_color.clicked.connect(self.choose_color)
        self.color = "#FFFFFF"  # 默认白色
        self.ui.btn_choose_color.setStyleSheet(f"background-color: {self.color}")

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()
            self.ui.btn_choose_color.setStyleSheet(f"background-color: {self.color}")

    @override
    def accept(self):
        self.name = self.ui.diag_input_btn_name.text()
        # 如果命令以 'adb' 开头，去掉它
        cmd = self.ui.diag_input_adb.text().strip()
        if cmd.lower().startswith('adb '):
            cmd = cmd[4:].strip()
        self.cmd = cmd
        self.is_blocking = self.ui.radio_block_yes.isChecked()
        self.color = self.color
        super().accept()


class CommandThread(QThread):
    output = Signal(str, str, str, str, bool)  # time, serial, note, text, is_error
    finished = Signal()  # 添加完成信号

    def __init__(self, serial, note, cmd, parent=None):
        super().__init__(parent)
        self.serial = serial
        self.note = note
        self.cmd = cmd
        self.is_running = True
        self.process = None

    @override
    def run(self):
        try:
            # 如果命令以 'adb' 开头，去掉它
            cmd = self.cmd.strip()
            if cmd.lower().startswith('adb '):
                cmd = cmd[4:].strip()
            
            self.process = subprocess.Popen(
                f"adb -s {self.serial} {cmd}",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True,
                bufsize=1,  # 行缓冲
                universal_newlines=True  # 使用通用换行符
            )

            # 实时读取输出
            while self.is_running:
                # 读取一行输出
                line = self.process.stdout.readline()
                if not line and self.process.poll() is not None:
                    break
                if line:
                    self.output.emit(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        self.serial,
                        self.note,
                        line.strip(),
                        False
                    )

            # 检查是否有错误输出
            stderr = self.process.stderr.read()
            if stderr:
                self.output.emit(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    self.serial,
                    self.note,
                    stderr,
                    True
                )

        except Exception as e:
            self.output.emit(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.serial,
                self.note,
                str(e),
                True
            )
        finally:
            self.finished.emit()  # 发送完成信号

    def stop(self):
        self.is_running = False
        if self.process:
            try:
                self.process.terminate()  # 先尝试正常终止
                self.process.wait(timeout=1)  # 等待最多1秒
            except subprocess.TimeoutExpired:
                self.process.kill()  # 如果超时，强制终止
            except Exception as e:
                print(f"停止进程时出错: {e}")


class LogWriter:
    def __init__(self, log_file):
        self.writer_thread = None
        self.log_file = log_file
        self.loop = asyncio.new_event_loop()
        self.queue = asyncio.Queue()
        self.writer_task = None
        self.start_writer()

    def start_writer(self):
        def run_writer():
            asyncio.set_event_loop(self.loop)
            self.writer_task = self.loop.create_task(self.write_logs())
            self.loop.run_forever()

        self.writer_thread = threading.Thread(target=run_writer, daemon=True)
        self.writer_thread.start()

    async def write_logs(self):
        while True:
            log_entry = await self.queue.get()
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    f.write(log_entry + '\n')
            except Exception as e:
                print(f"Error writing log: {e}")
            finally:
                self.queue.task_done()

    def write(self, log_entry):
        asyncio.run_coroutine_threadsafe(self.queue.put(log_entry), self.loop)

    def stop(self):
        if self.writer_task:
            self.loop.call_soon_threadsafe(self.writer_task.cancel)
            self.loop.stop()
            if self.writer_thread and self.writer_thread.is_alive():
                self.writer_thread.join()


class LogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("日志窗口")
        self.resize(800, 600)  # 设置更大的窗口尺寸
        
        # 创建布局
        layout = QVBoxLayout(self)
        
        # 创建文本浏览器
        self.text_browser = QTextBrowser()
        self.text_browser.setLineWrapMode(QTextBrowser.LineWrapMode.NoWrap)
        self.text_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        layout.addWidget(self.text_browser)
        
        # 创建按钮布局
        button_layout = QHBoxLayout()
        
        # 创建清除按钮
        self.clear_button = QPushButton("清除日志")
        self.clear_button.clicked.connect(self.clear_log)
        button_layout.addWidget(self.clear_button)
        
        # 创建关闭按钮
        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        
        # 设置窗口属性
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    def append_log(self, text):
        self.text_browser.append(text)
        # 滚动到底部
        self.text_browser.verticalScrollBar().setValue(
            self.text_browser.verticalScrollBar().maximum()
        )

    def clear_log(self):
        self.text_browser.clear()

    def closeEvent(self, event):
        # 通知父窗口日志窗口已关闭
        if self.parent():
            self.parent().log_window = None
        super().closeEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 初始化变量
        self.devices_file = "devices.csv"
        self.commands_file = "commands.csv"
        self.groups_file = "groups.csv"  # 新增分组信息文件
        self.log_file = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.registered_devices = {}  # serial -> note
        self.command_threads = []
        self.log_writer = LogWriter(self.log_file)
        
        # 添加按钮状态标志
        self.is_refreshing = False
        self.is_running_command = False
        self.is_stopping_command = False

        # 设置输出文本框不换行并启用水平滚动条
        self.ui.output_text_browser.setLineWrapMode(QTextBrowser.LineWrapMode.NoWrap)
        self.ui.output_text_browser.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # 创建日志窗口
        self.log_window = None

        # 连接信号
        self.bind()

        # 初始化设备管理tab页右键菜单
        self.ui.device_tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.device_tree_widget.customContextMenuRequested.connect(self.show_device_context_menu)

        # 初始化命令管理tab页右键菜单
        self.ui.cmd_tab_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.ui.cmd_tab_widget.customContextMenuRequested.connect(self.show_cmd_group_context_menu)

        # 移除UI中定义的默认分组
        self.ui.cmd_tab_widget.removeTab(0)

        # 加载已保存的数据
        self.load_devices()
        self.load_groups()  # 先加载分组
        self.load_commands()  # 再加载命令

        # 初始刷新设备列表
        self.refresh_devices()
        
        # 初始化停止按钮状态
        self.ui.btn_stop_cmd.setEnabled(False)

    def bind(self):
        self.ui.btn_refresh_online_device.clicked.connect(self.refresh_devices)
        self.ui.btn_register_device.clicked.connect(self.register_device)
        self.ui.btn_direct_run.clicked.connect(self.run_direct_command)
        self.ui.btn_add_new_group.clicked.connect(self.add_new_group)
        self.ui.btn_add_cmd.clicked.connect(self.add_new_command)
        self.ui.btn_stop_cmd.clicked.connect(self.stop_commands)
        self.ui.btn_clear_log.clicked.connect(self.clear_log)
        self.ui.btn_pop_log.clicked.connect(self.show_log_window)

    def load_devices(self):
        self.registered_devices = {}
        if os.path.exists(self.devices_file):
            with open(self.devices_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        self.registered_devices[row[0]] = row[1]

    def load_groups(self):
        """从文件加载分组信息"""
        try:
            if os.path.exists(self.groups_file):
                with open(self.groups_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content:  # 如果文件为空
                        return
                    
                    # 重新打开文件读取分组
                    f.seek(0)
                    reader = csv.reader(f)
                    has_groups = False
                    for row in reader:
                        if len(row) >= 1 and row[0].strip():  # 确保分组名称不为空
                            has_groups = True
                            group_name = row[0].strip()
                            new_group = QWidget()
                            layout = QGridLayout(new_group)
                            layout.setSpacing(10)
                            layout.setContentsMargins(10, 10, 10, 10)
                            layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
                            self.ui.cmd_tab_widget.addTab(new_group, group_name)
                    
                    # 只有在文件存在但没有任何有效分组时才创建默认分组
                    if not has_groups:
                        new_group = QWidget()
                        layout = QGridLayout(new_group)
                        layout.setSpacing(10)
                        layout.setContentsMargins(10, 10, 10, 10)
                        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
                        self.ui.cmd_tab_widget.addTab(new_group, "默认分组")
                        self.save_groups()
            else:
                # 如果分组文件不存在，创建一个空的分组
                new_group = QWidget()
                layout = QGridLayout(new_group)
                layout.setSpacing(10)
                layout.setContentsMargins(10, 10, 10, 10)
                layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
                self.ui.cmd_tab_widget.addTab(new_group, "默认分组")
                self.save_groups()
        except Exception as e:
            print(f"加载分组信息时出错: {e}")
            # 如果加载出错，创建一个空的分组
            new_group = QWidget()
            layout = QGridLayout(new_group)
            layout.setSpacing(10)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            self.ui.cmd_tab_widget.addTab(new_group, "默认分组")
            self.save_groups()

    def load_commands(self):
        """从文件加载命令按钮信息"""
        if os.path.exists(self.commands_file):
            with open(self.commands_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 4 and row[1]:  # 只有当有按钮信息时才添加按钮
                        group_name, name, cmd, is_blocking, color = row
                        self.add_command_to_group(group_name, name, cmd, is_blocking == 'True', color)

    def save_devices(self):
        with open(self.devices_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for serial, note in self.registered_devices.items():
                writer.writerow([serial, note])

    def save_groups(self):
        """保存分组信息到文件"""
        try:
            with open(self.groups_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                for i in range(self.ui.cmd_tab_widget.count()):
                    group_name = self.ui.cmd_tab_widget.tabText(i)
                    if group_name:  # 只保存非空的分组名称
                        writer.writerow([group_name])
        except Exception as e:
            print(f"保存分组信息时出错: {e}")

    def save_commands(self):
        """保存命令按钮信息到文件"""
        with open(self.commands_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for i in range(self.ui.cmd_tab_widget.count()):
                group_name = self.ui.cmd_tab_widget.tabText(i)
                group_widget = self.ui.cmd_tab_widget.widget(i)
                for button in group_widget.findChildren(QPushButton):
                    writer.writerow([
                        group_name,
                        button.text(),
                        button.property('cmd'),
                        str(button.property('is_blocking')),
                        button.property('color')
                    ])

    def refresh_devices(self):
        if self.is_refreshing:
            QMessageBox.information(self, "提示", "正在刷新设备列表，请稍候...")
            return
        self.is_refreshing = True
        try:
            # 先加载最新的设备配置
            self.load_devices()

            # 获取在线设备
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            devices = []
            for line in result.stdout.split('\n')[1:]:
                if '\tdevice' in line:
                    serial = line.split('\t')[0]
                    devices.append(serial)

            device_count = len(devices)
            # 更新设备数量
            self.ui.label_device_count.setText(str(device_count))

            # 清空设备树
            self.ui.device_tree_widget.clear()

            # 创建已登记和未登记分组
            registered_item = QTreeWidgetItem(self.ui.device_tree_widget, ['已登记设备'])
            unregistered_item = QTreeWidgetItem(self.ui.device_tree_widget, ['未登记设备'])

            # 添加设备到对应分组
            registered_count = 0
            unregistered_count = 0

            for serial in devices:
                if serial in self.registered_devices:
                    item = QTreeWidgetItem(registered_item)
                    item.setText(1, serial)
                    item.setText(2, self.registered_devices[serial])
                    item.setCheckState(0, Qt.CheckState.Unchecked)
                    registered_count += 1
                else:
                    item = QTreeWidgetItem(unregistered_item)
                    item.setText(1, serial)
                    item.setCheckState(0, Qt.CheckState.Unchecked)
                    unregistered_count += 1

            # 如果分组下没有设备，则移除该分组
            if registered_count == 0:
                self.ui.device_tree_widget.takeTopLevelItem(
                    self.ui.device_tree_widget.indexOfTopLevelItem(registered_item)
                )
            if unregistered_count == 0:
                self.ui.device_tree_widget.takeTopLevelItem(
                    self.ui.device_tree_widget.indexOfTopLevelItem(unregistered_item)
                )

            # 展开所有分组
            self.ui.device_tree_widget.expandAll()

        except Exception as e:
            QMessageBox.critical(self, "错误", f"刷新设备失败：{str(e)}")
        finally:
            self.is_refreshing = False

    def register_device(self, serial=None):
        dialog = RegisterDeviceDialog(self, serial)
        dialog.device_registered.connect(self.refresh_devices)
        dialog.exec()

    def show_device_context_menu(self, pos):
        item = self.ui.device_tree_widget.itemAt(pos)
        if not item or item.parent() is None:
            return

        menu = QMenu()
        serial = item.text(1)

        register_action = None
        edit_action = None
        delete_action = None
        if serial in self.registered_devices:
            edit_action = menu.addAction("编辑设备信息")
            delete_action = menu.addAction("删除登记信息")
        else:
            register_action = menu.addAction("登记设备")

        action = menu.exec(self.ui.device_tree_widget.mapToGlobal(pos))
        if not action:  # 如果用户点击了菜单外的区域，action 将为 None
            return

        if action == edit_action:
            self.edit_device_info(serial)
        elif action == delete_action:
            self.delete_device_info(serial)
        elif action == register_action:
            self.register_device(serial)

    def edit_device_info(self, serial):
        note, ok = QInputDialog.getText(
            self, "编辑设备信息", "请输入备注信息：",
            text=self.registered_devices[serial]
        )
        if ok:
            self.registered_devices[serial] = note
            self.save_devices()
            self.refresh_devices()

    def delete_device_info(self, serial):
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除设备 {serial} 的登记信息吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            del self.registered_devices[serial]
            self.save_devices()
            self.refresh_devices()

    def show_cmd_group_context_menu(self, pos):
        tab_bar = self.ui.cmd_tab_widget.tabBar()
        index = tab_bar.tabAt(pos)
        if index >= 0:
            menu = QMenu()
            edit_action = menu.addAction("编辑分组名称")
            delete_action = menu.addAction("删除分组")

            action = menu.exec(tab_bar.mapToGlobal(pos))

            if action == edit_action:
                self.edit_group_name(index)
            elif action == delete_action:
                self.delete_group(index)

    def edit_group_name(self, index):
        old_name = self.ui.cmd_tab_widget.tabText(index)
        new_name, ok = QInputDialog.getText(
            self, "编辑分组名称", "请输入新的分组名称：",
            text=old_name
        )
        if ok and new_name:
            # 检查是否已存在同名分组
            for i in range(self.ui.cmd_tab_widget.count()):
                if i != index and self.ui.cmd_tab_widget.tabText(i) == new_name:
                    QMessageBox.warning(self, "警告", "分组名称已存在")
                    return
            self.ui.cmd_tab_widget.setTabText(index, new_name)
            # 保存分组信息
            self.save_groups()

    def delete_group(self, index):
        reply = QMessageBox.question(
            self, "确认删除",
            "分组下的命令按钮也会被全部删除，确定要删除该分组吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.ui.cmd_tab_widget.removeTab(index)
            self.save_groups()
            self.save_commands()

    def add_new_group(self):
        name, ok = QInputDialog.getText(self, "添加新分组", "请输入分组名称：")
        if ok and name:
            # 检查是否已存在同名分组
            for i in range(self.ui.cmd_tab_widget.count()):
                if self.ui.cmd_tab_widget.tabText(i) == name:
                    QMessageBox.warning(self, "警告", "分组名称已存在")
                    return

            # 创建新分组
            new_group = QWidget()
            layout = QGridLayout(new_group)
            layout.setSpacing(10)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
            
            new_index = self.ui.cmd_tab_widget.addTab(new_group, name)
            # 切换到新创建的分组
            self.ui.cmd_tab_widget.setCurrentIndex(new_index)
            # 保存分组信息
            self.save_groups()

    def add_new_command(self):
        current_index = self.ui.cmd_tab_widget.currentIndex()
        if current_index < 0:
            QMessageBox.warning(self, "警告", "请先选择一个分组")
            return

        # 获取当前分组的widget和布局
        group_widget = self.ui.cmd_tab_widget.widget(current_index)
        layout = group_widget.layout()
        
        # 计算当前按钮数量
        current_buttons = len(group_widget.findChildren(QPushButton))
        
        # 计算每行可以放置的按钮数量（考虑按钮宽度和间距）
        button_width = 80  # 按钮宽度
        button_height = 30  # 按钮高度
        spacing = 10  # 按钮间距
        margins = 10  # 布局边距
        
        # 获取当前分组的可用宽度
        available_width = group_widget.width() - 2 * margins
        buttons_per_row = (available_width + spacing) // (button_width + spacing)
        
        # 计算每列可以放置的按钮数量（考虑按钮高度和间距）
        available_height = group_widget.height() - 2 * margins
        buttons_per_column = (available_height + spacing) // (button_height + spacing)
        
        # 计算最大按钮数量
        max_buttons = buttons_per_row * buttons_per_column
        
        # 如果当前按钮数量达到最大值，显示提示对话框
        if current_buttons >= max_buttons:
            reply = QMessageBox.question(
                self,
                "空间已满",
                "当前分组空间已满，是否创建新分组？",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.add_new_group()
            return

        # 如果还有空间，继续添加新按钮
        dialog = AddCmdDialog(self)
        if dialog.exec():
            self.add_command_to_group(
                self.ui.cmd_tab_widget.tabText(current_index),
                dialog.name,
                dialog.cmd,
                dialog.is_blocking,
                dialog.color
            )
            self.save_commands()

    def add_command_to_group(self, group_name, name, cmd, is_blocking, color):
        # 找到对应的分组
        for i in range(self.ui.cmd_tab_widget.count()):
            if self.ui.cmd_tab_widget.tabText(i) == group_name:
                group_widget = self.ui.cmd_tab_widget.widget(i)
                layout = group_widget.layout()
                if not layout:
                    layout = QGridLayout(group_widget)
                    layout.setSpacing(10)  # 设置按钮之间的间距
                    layout.setContentsMargins(10, 10, 10, 10)  # 设置布局边距
                    layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)  # 设置对齐方式为左上

                # 获取当前按钮数量，用于计算位置
                button_count = len(group_widget.findChildren(QPushButton))
                row = button_count // 3
                col = button_count % 3

                # 创建命令按钮
                button = QPushButton(name)
                button.setProperty('cmd', cmd)
                button.setProperty('is_blocking', is_blocking)
                button.setProperty('color', color)
                button.setStyleSheet(f"background-color: {color}")
                button.clicked.connect(lambda checked, b=button: self.run_command(b))
                
                # 设置按钮的固定大小
                button.setFixedSize(80, 30)  # 调整按钮的固定宽度和高度
                
                # 设置右键菜单
                button.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                button.customContextMenuRequested.connect(
                    lambda pos, b=button, g=group_name: self.show_cmd_button_context_menu(pos, b, g)
                )
                
                # 将按钮添加到网格布局中
                layout.addWidget(button, row, col)
                break

    def show_cmd_button_context_menu(self, pos, button, group_name):
        menu = QMenu()
        edit_action = menu.addAction("编辑命令")
        delete_action = menu.addAction("删除命令")

        action = menu.exec(button.mapToGlobal(pos))
        if action == edit_action:
            self.edit_command_button(button, group_name)
        elif action == delete_action:
            self.delete_command_button(button, group_name)

    def edit_command_button(self, button, group_name):
        dialog = AddCmdDialog(self)
        dialog.ui.diag_input_btn_name.setText(button.text())
        dialog.ui.diag_input_adb.setText(button.property('cmd'))
        dialog.ui.radio_block_yes.setChecked(button.property('is_blocking'))
        dialog.color = button.property('color')
        dialog.ui.btn_choose_color.setStyleSheet(f"background-color: {dialog.color}")

        if dialog.exec():
            # 更新按钮属性
            button.setText(dialog.name)
            button.setProperty('cmd', dialog.cmd)
            button.setProperty('is_blocking', dialog.is_blocking)
            button.setProperty('color', dialog.color)
            button.setStyleSheet(f"background-color: {dialog.color}")
            
            # 保存更改
            self.save_commands()

    def delete_command_button(self, button, group_name):
        reply = QMessageBox.question(
            self, "确认删除",
            "确定要删除该命令按钮吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            # 从布局中移除按钮
            button.setParent(None)
            button.deleteLater()
            
            # 重新排列剩余按钮
            self.rearrange_buttons(group_name)
            
            # 保存更改
            self.save_commands()

    def rearrange_buttons(self, group_name):
        # 找到对应的分组
        for i in range(self.ui.cmd_tab_widget.count()):
            if self.ui.cmd_tab_widget.tabText(i) == group_name:
                group_widget = self.ui.cmd_tab_widget.widget(i)
                layout = group_widget.layout()
                if not layout:
                    layout = QGridLayout(group_widget)
                    layout.setSpacing(10)  # 设置按钮之间的间距
                    layout.setContentsMargins(10, 10, 10, 10)  # 设置布局边距
                    layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)  # 设置对齐方式为左上

                # 获取所有按钮
                buttons = group_widget.findChildren(QPushButton)
                
                # 从布局中移除所有按钮
                for button in buttons:
                    layout.removeWidget(button)
                
                # 重新添加按钮到布局
                for idx, button in enumerate(buttons):
                    row = idx // 3
                    col = idx % 3
                    layout.addWidget(button, row, col)
                break

    def run_command(self, button):
        cmd = button.property('cmd')
        is_blocking = button.property('is_blocking')
        self.execute_command(cmd, is_blocking)

    def run_direct_command(self):
        cmd = self.ui.lineEdit_cmd.text()
        if cmd:
            self.execute_command(cmd, False)

    def execute_command(self, cmd, is_blocking):
        if self.is_running_command:
            QMessageBox.information(self, "提示", "正在执行命令，请等待当前命令执行完成...")
            return
        self.is_running_command = True
        try:
            # 获取选中的设备
            selected_devices = []
            for i in range(self.ui.device_tree_widget.topLevelItemCount()):
                group = self.ui.device_tree_widget.topLevelItem(i)
                for j in range(group.childCount()):
                    item = group.child(j)
                    if item.checkState(0) == Qt.CheckState.Checked:
                        serial = item.text(1)
                        note = item.text(2) if item.text(2) else "未登记"
                        selected_devices.append((serial, note))

            if not selected_devices:
                QMessageBox.warning(self, "警告", "请选择至少一个设备")
                self.is_running_command = False
                return

            # 停止之前的命令
            self.stop_commands()

            # 创建所有线程
            for serial, note in selected_devices:
                thread = CommandThread(serial, note, cmd)
                thread.output.connect(self.handle_command_output)
                thread.finished.connect(self.check_threads_status)  # 连接完成信号
                self.command_threads.append(thread)

            # 启用停止按钮
            self.ui.btn_stop_cmd.setEnabled(True)

            # 启动所有线程
            for thread in self.command_threads:
                thread.start()
        finally:
            self.is_running_command = False

    def stop_commands(self):
        if self.is_stopping_command:
            QMessageBox.information(self, "提示", "正在停止命令，请稍候...")
            return
        self.is_stopping_command = True
        try:
            # 先尝试停止所有线程
            for thread in self.command_threads:
                thread.stop()
            
            # 等待所有线程停止
            for thread in self.command_threads:
                if thread.isRunning():
                    thread.wait(1000)  # 等待最多1秒
            
            # 清理线程列表和重置按钮状态
            self.command_threads.clear()
            self.ui.btn_stop_cmd.setEnabled(False)
        finally:
            self.is_stopping_command = False

    def handle_command_output(self, time_str, serial, note, text, is_error):
        # 格式化输出
        if is_error:
            color = "red"
        else:
            color = "black"

        output = f'<span style="color: {color}">[{time_str}][{serial}][{note}]{text}</span>'

        # 更新UI
        self.ui.output_text_browser.append(output)
        
        # 如果日志窗口存在，也更新日志窗口
        if self.log_window and self.log_window.isVisible():
            self.log_window.append_log(output)

        # 异步写入日志
        self.log_writer.write(f"[{time_str}][{serial}][{note}]{text}")

    def show_log_window(self):
        if not self.log_window:
            self.log_window = LogWindow(self)
            # 将当前输出框的内容复制到日志窗口
            self.log_window.text_browser.setHtml(self.ui.output_text_browser.toHtml())
        self.log_window.show()
        self.log_window.raise_()  # 将窗口提升到最前

    def clear_log(self):
        self.ui.output_text_browser.clear()
        if self.log_window and self.log_window.isVisible():
            self.log_window.clear_log()

    def check_threads_status(self):
        # 检查是否所有线程都已完成
        all_finished = True
        for thread in self.command_threads:
            if thread.isRunning():
                all_finished = False
                break
        
        # 如果所有线程都已完成，禁用停止按钮
        if all_finished:
            self.ui.btn_stop_cmd.setEnabled(False)

    @override
    def closeEvent(self, event):
        # 停止所有正在执行的命令
        self.stop_commands()
        # 停止日志写入器
        if hasattr(self, 'log_writer'):
            self.log_writer.stop()
        # 调用父类的closeEvent
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
