"""样式定义文件"""

# 主窗口样式
MAIN_STYLE = """
/* Main Window */
QMainWindow {
    background-color: white;
}

/* Tab Widget */
QTabWidget::pane {
    border: none;
    background-color: white;
    border-radius: 4px;
}

/* Command Tab Widget */
QWidget[objectName^="cmd_tab_widget"] {
    background-color: #e8e8e8;
    border: 1px solid #dcdcdc;
    border-radius: 4px;
}

QWidget[objectName^="cmd_tab_widget"] QWidget {
    background-color: #e8e8e8;
    border: none;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #f5f5f5;
    border: 1px solid #dcdcdc;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    border-bottom: none;
}

QTabBar::tab:selected {
    background-color: white;
    border-bottom: 5px solid #53A6D8;
    margin-bottom: -1px;  /* 抵消底部边框的宽度，避免出现双边框 */
}

QTabBar::tab:hover:!selected {
    background-color: #fafafa;
}

/* Main Window Buttons */
QMainWindow QPushButton {
    background-color: #53A6D8;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
}

QMainWindow QPushButton:hover {
    background-color: #6BB5E3;
}

QMainWindow QPushButton:pressed {
    background-color: #4A95C7;
}

QMainWindow QPushButton:disabled {
    background-color: #d9d9d9;
}

/* Line Edit */
QLineEdit {
    padding: 6px;
    border: 1px solid #dcdcdc;
    border-radius: 4px;
    background-color: white;
}

QLineEdit:focus {
    border-color: #53A6D8;
}

/* Tree Widget */
QTreeWidget {
    border: 1px solid #dcdcdc;
    border-radius: 4px;
    background-color: white;
}

QTreeWidget::item {
    padding: 4px;
}

QTreeWidget::item:selected {
    background-color: #E8F4FC;
    color: #53A6D8;
}

/* Text Browser */
QTextBrowser {
    border: 1px solid #dcdcdc;
    border-radius: 4px;
    background-color: white;
    padding: 8px;
}

/* Labels */
QLabel {
    color: #262626;
}
"""

# 对话框样式
DIALOG_STYLE = """
/* Dialog */
QDialog {
    background-color: white;
}

/* Log Window */
QDialog QTextBrowser {
    background-color: white;
    border: 1px solid #dcdcdc;
    border-radius: 4px;
    padding: 8px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 12px;
    line-height: 1.5;
}

/* Dialog Buttons */
QDialog QPushButton {
    background-color: #53A6D8;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    min-width: 80px;
}

QDialog QPushButton:hover {
    background-color: #6BB5E3;
}

QDialog QPushButton:pressed {
    background-color: #4A95C7;
}
"""

# 命令按钮样式
COMMAND_BUTTON_STYLE = """
/* Command Buttons */
QMainWindow QWidget[objectName^="cmd_tab_widget"] QPushButton {
    background-color: #53A6D8;
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
    text-align: center;
}

QMainWindow QWidget[objectName^="cmd_tab_widget"] QPushButton:hover {
    filter: brightness(110%);
}

QMainWindow QWidget[objectName^="cmd_tab_widget"] QPushButton:pressed {
    filter: brightness(90%);
}
"""

# 动态按钮样式
DYNAMIC_BUTTON_STYLE = """
/* Color Choose Button */
QPushButton#btn_choose_color {
    border: 1px solid #dcdcdc;
    border-radius: 4px;
    padding: 4px;
    min-width: 60px;
    min-height: 24px;
}

QPushButton#btn_choose_color:hover {
    border-color: #53A6D8;
}

/* Command Button Base Style */
QPushButton[objectName^="cmd_button"] {
    color: white;
    border: none;
    padding: 4px 8px;
    border-radius: 4px;
    font-weight: bold;
    text-align: center;
}

QPushButton[objectName^="cmd_button"]:hover {
    filter: brightness(110%);
}

QPushButton[objectName^="cmd_button"]:pressed {
    filter: brightness(90%);
}

/* Command Completer */
QCompleter {
    background-color: white;
    border: 1px solid #dcdcdc;
    border-radius: 4px;
    padding: 4px;
}

QCompleter::item {
    padding: 4px 8px;
    border-bottom: 1px solid #f0f0f0;
}

QCompleter::item:selected {
    background-color: #E8F4FC;
    color: #53A6D8;
}

QCompleter::item:hover {
    background-color: #f5f5f5;
}
"""


def get_stylesheet():
    """获取所有样式表"""
    return MAIN_STYLE + DIALOG_STYLE + COMMAND_BUTTON_STYLE + DYNAMIC_BUTTON_STYLE
