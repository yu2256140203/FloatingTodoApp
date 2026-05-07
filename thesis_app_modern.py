# -*- coding: utf-8 -*-
"""
NEUCSE 毕业论文盲审状态检查工具 - Modern UI Edition
现代化UI设计：毛玻璃、二次元风格、流畅动画
"""

import sys
import requests
import re
import threading
import time
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QSpinBox, QPushButton, QTextEdit, QMessageBox,
                             QFrame, QStackedWidget)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal, QObject, QSize
from PyQt6.QtGui import QFont, QColor, QIcon, QPainter, QBrush, QLinearGradient, QPen
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

class QuerySignals(QObject):
    """用于线程安全的信号传递"""
    log_signal = pyqtSignal(str)
    result_signal = pyqtSignal(str, str, str)  # account, title, status
    error_signal = pyqtSignal(str)

class ThesisCheckerModern(QMainWindow):
    def __init__(self):
        super().__init__()
        self.running = False
        self.stop_event = threading.Event()
        self.last_status = None
        self.current_audio = None
        
        self.query_signals = QuerySignals()
        self.query_signals.log_signal.connect(self.on_log)
        self.query_signals.result_signal.connect(self.on_result)
        self.query_signals.error_signal.connect(self.on_error)
        
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("论文盲审检查 - Modern")
        self.setGeometry(100, 100, 720, 800)
        self.setWindowIcon(QIcon())
        
        # 应用样式
        self.apply_modern_style()
        
        # 主窗口widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 标题栏
        title_frame = self.create_title_bar()
        main_layout.addWidget(title_frame)
        
        # 内容区域 - 使用ScrollArea容纳滚动
        content_frame = self.create_content_frame()
        main_layout.addWidget(content_frame, 1)

    def create_title_bar(self):
        """创建现代化标题栏"""
        frame = QFrame()
        frame.setMaximumHeight(100)
        frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(102, 126, 234, 0.25),
                    stop:1 rgba(118, 75, 162, 0.25));
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(30, 15, 30, 15)
        layout.setSpacing(10)
        
        # 主标题
        title = QLabel("论文盲审检查工具")
        title.setFont(QFont("微软雅黑", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff; text-shadow: 0px 2px 4px rgba(0,0,0,0.3);")
        
        # 副标题
        subtitle = QLabel("NEUCSE毕业论文 • 实时状态监控")
        subtitle.setFont(QFont("微软雅黑", 11))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        
        layout.addWidget(title)
        layout.addWidget(subtitle)
        
        return frame

    def create_content_frame(self):
        """创建主内容区域"""
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background: transparent;
            }
        """)
        
        layout = QVBoxLayout(main_frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # 配置面板
        config_panel = self.create_config_panel()
        layout.addWidget(config_panel)
        
        # 控制按钮
        control_panel = self.create_control_panel()
        layout.addWidget(control_panel)
        
        # 结果显示面板
        result_panel = self.create_result_panel()
        layout.addWidget(result_panel)
        
        # 日志面板
        log_panel = self.create_log_panel()
        layout.addWidget(log_panel, 1)
        
        return main_frame

    def create_config_panel(self):
        """创建配置输入面板"""
        panel = self.create_glass_panel("⚙️ 配置")
        layout = panel.findChild(QVBoxLayout)
        
        # Cookie
        self.cookie_label = QLabel("OPENCONF Cookie")
        self.cookie_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-weight: bold;")
        self.cookie_input = self.create_modern_input()
        layout.addWidget(self.cookie_label)
        layout.addWidget(self.cookie_input)
        
        # 账号和密码在同一行
        row1_layout = QHBoxLayout()
        
        pid_label = QLabel("账号 (pid)")
        pid_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-weight: bold;")
        self.pid_input = self.create_modern_input()
        row1_layout.addWidget(pid_label)
        row1_layout.addWidget(self.pid_input)
        
        pwd_label = QLabel("密码 (pwd)")
        pwd_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-weight: bold;")
        self.pwd_input = self.create_modern_input()
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        row1_layout.addWidget(pwd_label)
        row1_layout.addWidget(self.pwd_input)
        
        layout.addLayout(row1_layout)
        
        # 轮询间隔
        row2_layout = QHBoxLayout()
        interval_label = QLabel("轮询间隔 (分钟)")
        interval_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-weight: bold;")
        self.interval_spin = QSpinBox()
        self.interval_spin.setMinimum(1)
        self.interval_spin.setMaximum(60)
        self.interval_spin.setValue(5)
        self.interval_spin.setStyleSheet(self.get_spinbox_style())
        self.interval_spin.setMaximumWidth(80)
        
        row2_layout.addWidget(interval_label)
        row2_layout.addWidget(self.interval_spin)
        row2_layout.addStretch()
        
        layout.addLayout(row2_layout)
        
        return panel

    def create_control_panel(self):
        """创建控制按钮面板"""
        panel = self.create_glass_panel("🎮 控制")
        layout = panel.findChild(QVBoxLayout)
        
        button_layout = QHBoxLayout()
        
        # 开始监控按钮
        self.btn_start = self.create_modern_button("🚀 开始监控")
        self.btn_start.clicked.connect(self.start_monitoring)
        button_layout.addWidget(self.btn_start)
        
        # 停止按钮
        self.btn_stop = self.create_modern_button("⏹️  停止", style="danger")
        self.btn_stop.clicked.connect(self.stop_monitoring)
        self.btn_stop.setEnabled(False)
        button_layout.addWidget(self.btn_stop)
        
        # 立即查询按钮
        self.btn_once = self.create_modern_button("🔍 立即查询", style="info")
        self.btn_once.clicked.connect(self.query_once)
        button_layout.addWidget(self.btn_once)
        
        layout.addLayout(button_layout)
        
        # 状态标签
        self.status_label = QLabel("状态: 就绪")
        self.status_label.setFont(QFont("微软雅黑", 12, QFont.Weight.Bold))
        self.status_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.9);
            padding: 10px;
            border-radius: 8px;
            background: rgba(100, 200, 100, 0.2);
        """)
        layout.addWidget(self.status_label)
        
        return panel

    def create_result_panel(self):
        """创建结果显示面板"""
        panel = self.create_glass_panel("📊 查询结果")
        layout = panel.findChild(QVBoxLayout)
        
        # 账号
        self.account_display = self.create_result_item("账号", "—")
        layout.addWidget(self.account_display)
        
        # 论文标题
        self.title_display = self.create_result_item("论文标题", "—")
        layout.addWidget(self.title_display)
        
        # 状态 (特殊显示)
        self.status_display = self.create_result_item("状态", "—")
        layout.addWidget(self.status_display)
        
        return panel

    def create_log_panel(self):
        """创建日志面板"""
        panel = self.create_glass_panel("📝 日志", expandable=True)
        layout = panel.findChild(QVBoxLayout)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 8px;
                color: rgba(100, 255, 100, 0.9);
                font-family: "Courier New", monospace;
                font-size: 10px;
                padding: 10px;
                selection-background-color: rgba(102, 126, 234, 0.4);
            }
            QTextEdit:focus {
                border: 1px solid rgba(255, 255, 255, 0.25);
            }
        """)
        
        layout.addWidget(self.log_text)
        return panel

    # ==================== 样式和组件工厂方法 ====================
    
    def create_glass_panel(self, title, expandable=False):
        """创建毛玻璃风格面板"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 15px;
            }
        """)
        
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(20, 15, 20, 15)
        panel_layout.setSpacing(12)
        
        # 标题
        if title:
            title_label = QLabel(title)
            title_label.setFont(QFont("微软雅黑", 13, QFont.Weight.Bold))
            title_label.setStyleSheet("color: rgba(255, 255, 255, 0.95);")
            panel_layout.addWidget(title_label)
            
            # 分隔线
            sep = QFrame()
            sep.setMaximumHeight(1)
            sep.setStyleSheet("background: rgba(255, 255, 255, 0.15);")
            panel_layout.addWidget(sep)
        
        return panel

    def create_modern_input(self):
        """创建现代化输入框"""
        input_field = QLineEdit()
        input_field.setMinimumHeight(42)
        input_field.setFont(QFont("微软雅黑", 10))
        input_field.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.08);
                border: 2px solid rgba(255, 255, 255, 0.15);
                border-radius: 8px;
                color: rgba(255, 255, 255, 0.95);
                padding: 8px 12px;
                selection-background-color: rgba(102, 126, 234, 0.8);
            }
            QLineEdit:focus {
                border: 2px solid rgba(102, 126, 234, 0.6);
                background: rgba(255, 255, 255, 0.12);
            }
        """)
        return input_field

    def create_modern_button(self, text, style="primary"):
        """创建现代化按钮"""
        button = QPushButton(text)
        button.setMinimumHeight(44)
        button.setFont(QFont("微软雅黑", 11, QFont.Weight.Bold))
        
        if style == "primary":
            button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #667eea,
                        stop:1 #764ba2);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #7e8ffa,
                        stop:1 #8a5bb4);
                    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
                }
                QPushButton:pressed {
                    transform: translate(0px, 2px);
                }
            """)
        elif style == "danger":
            button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #f093fb,
                        stop:1 #f5576c);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #fa9fff,
                        stop:1 #ff7d82);
                }
                QPushButton:pressed {
                    transform: translate(0px, 2px);
                }
            """)
        elif style == "info":
            button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #4facfe,
                        stop:1 #00f2fe);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #65fdff,
                        stop:1 #1affff);
                }
                QPushButton:pressed {
                    transform: translate(0px, 2px);
                }
            """)
        
        return button

    def create_result_item(self, label, value):
        """创建结果显示项"""
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 12px;
            }
        """)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(12, 8, 12, 8)
        
        label_widget = QLabel(label + ":")
        label_widget.setFont(QFont("微软雅黑", 10, QFont.Weight.Bold))
        label_widget.setStyleSheet("color: rgba(102, 126, 234, 0.9);")
        label_widget.setMinimumWidth(70)
        
        value_widget = QLabel(value)
        value_widget.setFont(QFont("微软雅黑", 11, QFont.Weight.Bold))
        value_widget.setStyleSheet("color: rgba(255, 255, 255, 0.95);")
        value_widget.setWordWrap(True)
        
        layout.addWidget(label_widget)
        layout.addWidget(value_widget, 1)
        
        # 保存引用以便后期更新
        if "account" in label:
            self.account_label_ref = value_widget
        elif "标题" in label:
            self.title_label_ref = value_widget
        else:
            self.status_label_ref = value_widget
        
        return container

    def get_spinbox_style(self):
        """获取SpinBox样式"""
        return """
            QSpinBox {
                background: rgba(255, 255, 255, 0.08);
                border: 2px solid rgba(255, 255, 255, 0.15);
                border-radius: 6px;
                color: rgba(255, 255, 255, 0.95);
                padding: 4px 8px;
                font: 10pt "微软雅黑";
            }
            QSpinBox:focus {
                border: 2px solid rgba(102, 126, 234, 0.6);
                background: rgba(255, 255, 255, 0.12);
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background: rgba(102, 126, 234, 0.3);
                border: none;
                border-radius: 3px;
                width: 20px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background: rgba(102, 126, 234, 0.5);
            }
        """

    def apply_modern_style(self):
        """应用整体现代化样式"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f172a,
                    stop:0.5 #1e3a5f,
                    stop:1 #1a1a2e);
            }
            QLabel {
                color: rgba(255, 255, 255, 0.9);
            }
        """)

    # ==================== 业务逻辑 ====================
    
    def check_inputs(self):
        """检查输入"""
        if not self.cookie_input.text().strip():
            QMessageBox.warning(self, "提示", "请填写 OPENCONF Cookie")
            return False
        if not self.pid_input.text().strip():
            QMessageBox.warning(self, "提示", "请填写账号 (pid)")
            return False
        if not self.pwd_input.text().strip():
            QMessageBox.warning(self, "提示", "请填写密码 (pwd)")
            return False
        return True

    def query_once(self):
        """立即查询一次"""
        if not self.check_inputs():
            return
        threading.Thread(target=self._do_query, daemon=True).start()

    def start_monitoring(self):
        """开始监控"""
        if not self.check_inputs():
            return
        
        self.running = True
        self.stop_event.clear()
        self.last_status = None
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        
        self.update_status("监控中...", "green")
        self.log("开始监控")
        
        threading.Thread(target=self._polling_loop, daemon=True).start()

    def stop_monitoring(self):
        """停止监控"""
        self.running = False
        self.stop_event.set()
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        
        self.update_status("已停止", "gray")
        self.log("已停止监控")

    def _polling_loop(self):
        """轮询循环"""
        while not self.stop_event.is_set():
            self._do_query()
            interval_sec = self.interval_spin.value() * 60
            
            for _ in range(interval_sec):
                if self.stop_event.is_set():
                    return
                time.sleep(1)

    def _do_query(self):
        """执行查询"""
        cookie = self.cookie_input.text().strip()
        pid = self.pid_input.text().strip()
        pwd = self.pwd_input.text().strip()
        
        base_url = "http://219.216.65.57/author/status.php"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                      "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cookie": f"OPENCONF={cookie}",
            "host": "219.216.65.57",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
        
        session = requests.Session()
        
        try:
            self.query_signals.log_signal.emit("正在获取表单 token…")
            resp_get = session.get(base_url, headers=headers, timeout=15)
            resp_get.encoding = "utf-8"
            html_form = resp_get.text
        except requests.RequestException as e:
            self.query_signals.log_signal.emit(f"❌ GET 请求失败: {e}")
            return
        
        token_match = re.search(r'name="token"\s+value="([^"]+)"', html_form)
        if not token_match:
            self.query_signals.log_signal.emit("❌ 未能获取 token，请检查 Cookie 是否有效")
            return
        
        token = token_match.group(1)
        self.query_signals.log_signal.emit(f"✓ 获取 token 成功: {token[:16]}…")
        
        post_data = {
            "ocaction": "Check Status",
            "token": token,
            "pid": pid,
            "pwd": pwd,
        }
        
        post_headers = {
            **headers,
            "content-type": "application/x-www-form-urlencoded",
            "origin": base_url,
            "referer": base_url,
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "1",
        }
        
        try:
            self.query_signals.log_signal.emit("正在提交查询…")
            resp_post = session.post(base_url, headers=post_headers, data=post_data, timeout=15)
            resp_post.encoding = "utf-8"
            html_result = resp_post.text
        except requests.RequestException as e:
            self.query_signals.log_signal.emit(f"❌ POST 请求失败: {e}")
            return
        
        # 检查错误
        err_match = re.search(r'class="warn"[^>]*>(.*?)</span>', html_result)
        if err_match:
            err_msg = err_match.group(1).strip()
            self.query_signals.log_signal.emit(f"❌ 查询失败: {err_msg}")
            self.query_signals.result_signal.emit("—", "—", f"错误: {err_msg}")
            return
        
        account = self._extract_field(html_result, r"账号:</strong>\s*(.*?)\s*</p>")
        title = self._extract_field(html_result, r"论文标题:</strong>\s*(.*?)\s*</p>")
        status = self._extract_field(html_result, r"状态:</strong>\s*(.*?)\s*</p>")
        
        if not status:
            self.query_signals.log_signal.emit("❌ 未能解析到状态信息")
            self.query_signals.result_signal.emit("解析失败", "解析失败", "解析失败")
            return
        
        self.query_signals.log_signal.emit(f"✓ 查询成功 → {account} | {status}")
        self.query_signals.result_signal.emit(account, title, status)
        
        # 状态变化提醒
        if status != "等待评阅" and self.last_status == "等待评阅":
            self.query_signals.log_signal.emit("⚠️  !!! 状态已变化，即将弹窗提醒 !!!")
            self.show_alert(account, title, status)
        
        self.last_status = status

    def _extract_field(self, html, pattern):
        """提取HTML字段"""
        m = re.search(pattern, html)
        return m.group(1).strip() if m else None

    def show_alert(self, account, title, status):
        """显示提醒"""
        QMessageBox.critical(
            self, 
            "🎉 论文状态更新",
            f"您的论文状态已发生变化！\n\n"
            f"账号: {account}\n"
            f"论文标题: {title}\n"
            f"当前状态: {status}\n\n"
            f"请尽快登录系统查看。"
        )

    # ==================== 信号处理 ====================
    
    def on_log(self, msg):
        """处理日志信号"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {msg}")

    def on_result(self, account, title, status):
        """处理结果信号"""
        self.account_label_ref.setText(account)
        self.title_label_ref.setText(title)
        
        # 状态特殊处理
        if status != "等待评阅":
            self.status_label_ref.setStyleSheet("color: rgba(255, 100, 100, 0.95);")
        else:
            self.status_label_ref.setStyleSheet("color: rgba(100, 200, 100, 0.95);")
        
        self.status_label_ref.setText(status)

    def on_error(self, msg):
        """处理错误信号"""
        QMessageBox.critical(self, "错误", msg)

    def update_status(self, text, color="gray"):
        """更新状态标签"""
        color_map = {
            "green": "rgba(100, 200, 100, 0.2)",
            "red": "rgba(200, 100, 100, 0.2)",
            "gray": "rgba(128, 128, 128, 0.2)",
        }
        self.status_label.setText(f"状态: {text}")
        self.status_label.setStyleSheet(f"""
            color: rgba(255, 255, 255, 0.9);
            padding: 10px;
            border-radius: 8px;
            background: {color_map.get(color, color_map['gray'])};
        """)

    def log(self, msg):
        """记录日志"""
        self.query_signals.log_signal.emit(msg)

    def load_settings(self):
        """加载保存的设置"""
        try:
            import json
            settings_file = "thesis_settings.json"
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                self.cookie_input.setText(settings.get("cookie", ""))
                self.pid_input.setText(settings.get("pid", ""))
                self.pwd_input.setText(settings.get("pwd", ""))
                self.interval_spin.setValue(settings.get("interval", 5))
        except:
            pass

    def closeEvent(self, event):
        """保存设置"""
        try:
            import json
            settings = {
                "cookie": self.cookie_input.text(),
                "pid": self.pid_input.text(),
                "pwd": self.pwd_input.text(),
                "interval": self.interval_spin.value(),
            }
            with open("thesis_settings.json", 'w') as f:
                json.dump(settings, f)
        except:
            pass
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = ThesisCheckerModern()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
