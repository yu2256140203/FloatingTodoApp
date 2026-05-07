# -*- coding: utf-8 -*-
"""
NEUCSE 毕业论文盲审状态检查工具 - 高级现代版
包含主题切换、高级动画、更好的视觉反馈
"""

import sys
import requests
import re
import threading
import time
import json
from datetime import datetime
from functools import wraps
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QSpinBox, QPushButton, QTextEdit, QMessageBox,
                             QFrame, QMenu, QComboBox)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, pyqtSignal, QObject, QSize, QPoint
from PyQt6.QtGui import QFont, QColor, QIcon, QPainter, QBrush, QLinearGradient, QPen, QFontMetrics
from PyQt6.QtWidgets import QScrollArea

from thesis_themes import ThemeManager, StyleSheetBuilder


class QuerySignals(QObject):
    """用于线程安全的信号传递"""
    log_signal = pyqtSignal(str)
    result_signal = pyqtSignal(str, str, str)  # account, title, status
    status_signal = pyqtSignal(str, str)  # text, color


class AnimatedLabel(QLabel):
    """带动画效果的标签"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.anim = None
        
    def animate_color_change(self, start_color, end_color, duration=500):
        """动画改变颜色"""
        self.anim = QPropertyAnimation(self, b"color")
        self.anim.setStartValue(QColor(start_color))
        self.anim.setEndValue(QColor(end_color))
        self.anim.setDuration(duration)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.start()


class ThesisCheckerAdvanced(QMainWindow):
    def __init__(self):
        super().__init__()
        self.running = False
        self.stop_event = threading.Event()
        self.last_status = None
        self.current_theme = "dark"
        
        self.query_signals = QuerySignals()
        self.query_signals.log_signal.connect(self.on_log)
        self.query_signals.result_signal.connect(self.on_result)
        self.query_signals.status_signal.connect(self.on_status_changed)
        
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("论文盲审检查工具 - 高级版")
        self.setGeometry(100, 100, 780, 900)
        self.setWindowIcon(QIcon())
        
        # 应用样式
        self.apply_theme("dark")
        
        # 主窗口widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 标题栏
        title_frame = self.create_title_bar()
        main_layout.addWidget(title_frame)
        
        # 内容区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        self.scroll_area.setWidgetResizable(True)
        
        content_frame = self.create_content_frame()
        self.scroll_area.setWidget(content_frame)
        main_layout.addWidget(self.scroll_area, 1)

    def create_title_bar(self):
        """创建标题栏"""
        frame = QFrame()
        frame.setMaximumHeight(110)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(30, 15, 30, 15)
        layout.setSpacing(10)
        
        # 顶部行：标题 + 主题选择
        top_row = QHBoxLayout()
        
        title = QLabel("论文盲审检查工具")
        title.setFont(QFont("微软雅黑", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff; text-shadow: 0px 2px 4px rgba(0,0,0,0.3);")
        
        # 主题选择
        theme_label = QLabel("主题:")
        theme_label.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["深色 (Dark)", "樱花粉 (Sakura)", "青幽 (Cyan)"])
        self.theme_combo.setCurrentIndex(0)
        self.theme_combo.currentIndexChanged.connect(self.on_theme_changed)
        self.theme_combo.setMaximumWidth(150)
        theme_combo_style = """
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                color: rgba(255, 255, 255, 0.9);
                padding: 4px 8px;
            }
            QComboBox:focus {
                border: 1px solid rgba(102, 126, 234, 0.6);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
        """
        self.theme_combo.setStyleSheet(theme_combo_style)
        
        top_row.addWidget(title)
        top_row.addStretch()
        top_row.addWidget(theme_label)
        top_row.addWidget(self.theme_combo)
        
        layout.addLayout(top_row)
        
        # 副标题
        subtitle = QLabel("NEUCSE毕业论文 • 实时状态监控 | 高级现代版本")
        subtitle.setFont(QFont("微软雅黑", 11))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.8);")
        layout.addWidget(subtitle)
        
        return frame

    def create_content_frame(self):
        """创建主内容区域"""
        main_frame = QWidget()
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
        
        layout.addStretch()
        return main_frame

    def create_config_panel(self):
        """创建配置面板"""
        theme = ThemeManager.get_theme(self.current_theme)
        
        panel = QFrame()
        panel.setStyleSheet(StyleSheetBuilder.build_glass_panel_style(theme))
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)
        
        # 标题
        title = QLabel("⚙️ 配置")
        title.setFont(QFont("微软雅黑", 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {theme['text_primary']};")
        layout.addWidget(title)
        
        # 分隔线
        sep = QFrame()
        sep.setMaximumHeight(1)
        sep.setStyleSheet(f"background: {theme['glass_border']};")
        layout.addWidget(sep)
        
        # Cookie
        cookie_label = QLabel("OPENCONF Cookie")
        cookie_label.setStyleSheet(f"color: {theme['text_primary']}; font-weight: bold;")
        self.cookie_input = self.create_input()
        layout.addWidget(cookie_label)
        layout.addWidget(self.cookie_input)
        
        # 账号和密码在同一行
        row1 = QHBoxLayout()
        
        pid_label = QLabel("账号 (pid)")
        pid_label.setStyleSheet(f"color: {theme['text_primary']}; font-weight: bold;")
        self.pid_input = self.create_input()
        row1.addWidget(pid_label)
        row1.addWidget(self.pid_input)
        
        pwd_label = QLabel("密码 (pwd)")
        pwd_label.setStyleSheet(f"color: {theme['text_primary']}; font-weight: bold;")
        self.pwd_input = self.create_input()
        self.pwd_input.setEchoMode(QLineEdit.EchoMode.Password)
        row1.addWidget(pwd_label)
        row1.addWidget(self.pwd_input)
        
        layout.addLayout(row1)
        
        # 轮询间隔
        row2 = QHBoxLayout()
        interval_label = QLabel("轮询间隔 (分钟)")
        interval_label.setStyleSheet(f"color: {theme['text_primary']}; font-weight: bold;")
        self.interval_spin = QSpinBox()
        self.interval_spin.setMinimum(1)
        self.interval_spin.setMaximum(60)
        self.interval_spin.setValue(5)
        self.interval_spin.setMaximumWidth(80)
        self.interval_spin.setStyleSheet(StyleSheetBuilder.build_spinbox_style(theme))
        
        row2.addWidget(interval_label)
        row2.addWidget(self.interval_spin)
        row2.addStretch()
        
        layout.addLayout(row2)
        
        return panel

    def create_control_panel(self):
        """创建控制面板"""
        theme = ThemeManager.get_theme(self.current_theme)
        
        panel = QFrame()
        panel.setStyleSheet(StyleSheetBuilder.build_glass_panel_style(theme))
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)
        
        # 标题
        title = QLabel("🎮 控制")
        title.setFont(QFont("微软雅黑", 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {theme['text_primary']};")
        layout.addWidget(title)
        
        # 分隔线
        sep = QFrame()
        sep.setMaximumHeight(1)
        sep.setStyleSheet(f"background: {theme['glass_border']};")
        layout.addWidget(sep)
        
        button_layout = QHBoxLayout()
        
        self.btn_start = self.create_button("🚀 开始监控", "primary")
        self.btn_start.clicked.connect(self.start_monitoring)
        button_layout.addWidget(self.btn_start)
        
        self.btn_stop = self.create_button("⏹️  停止", "danger")
        self.btn_stop.clicked.connect(self.stop_monitoring)
        self.btn_stop.setEnabled(False)
        button_layout.addWidget(self.btn_stop)
        
        self.btn_once = self.create_button("🔍 立即查询", "info")
        self.btn_once.clicked.connect(self.query_once)
        button_layout.addWidget(self.btn_once)
        
        layout.addLayout(button_layout)
        
        # 状态标签
        self.status_label = QLabel("状态: 就绪")
        self.status_label.setFont(QFont("微软雅黑", 12, QFont.Weight.Bold))
        self.status_label.setStyleSheet(f"""
            color: {theme['text_primary']};
            padding: 10px;
            border-radius: 8px;
            background: rgba(100, 200, 100, 0.2);
        """)
        layout.addWidget(self.status_label)
        
        return panel

    def create_result_panel(self):
        """创建结果面板"""
        theme = ThemeManager.get_theme(self.current_theme)
        
        panel = QFrame()
        panel.setStyleSheet(StyleSheetBuilder.build_glass_panel_style(theme))
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)
        
        # 标题
        title = QLabel("📊 查询结果")
        title.setFont(QFont("微软雅黑", 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {theme['text_primary']};")
        layout.addWidget(title)
        
        # 分隔线
        sep = QFrame()
        sep.setMaximumHeight(1)
        sep.setStyleSheet(f"background: {theme['glass_border']};")
        layout.addWidget(sep)
        
        self.account_display = self.create_result_item("账号", "—", theme)
        layout.addWidget(self.account_display)
        
        self.title_display = self.create_result_item("论文标题", "—", theme)
        layout.addWidget(self.title_display)
        
        self.status_display = self.create_result_item("状态", "—", theme)
        layout.addWidget(self.status_display)
        
        return panel

    def create_log_panel(self):
        """创建日志面板"""
        theme = ThemeManager.get_theme(self.current_theme)
        
        panel = QFrame()
        panel.setStyleSheet(StyleSheetBuilder.build_glass_panel_style(theme))
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(12)
        
        # 标题
        title = QLabel("📝 日志")
        title.setFont(QFont("微软雅黑", 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {theme['text_primary']};")
        layout.addWidget(title)
        
        # 分隔线
        sep = QFrame()
        sep.setMaximumHeight(1)
        sep.setStyleSheet(f"background: {theme['glass_border']};")
        layout.addWidget(sep)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet(StyleSheetBuilder.build_text_edit_style(theme))
        
        layout.addWidget(self.log_text)
        return panel

    # ==================== 组件工厂方法 ====================
    
    def create_input(self):
        """创建输入框"""
        theme = ThemeManager.get_theme(self.current_theme)
        input_field = QLineEdit()
        input_field.setMinimumHeight(42)
        input_field.setFont(QFont("微软雅黑", 10))
        input_field.setStyleSheet(StyleSheetBuilder.build_input_style(theme))
        return input_field

    def create_button(self, text, button_type="primary"):
        """创建按钮"""
        theme = ThemeManager.get_theme(self.current_theme)
        button = QPushButton(text)
        button.setMinimumHeight(44)
        button.setFont(QFont("微软雅黑", 11, QFont.Weight.Bold))
        button.setStyleSheet(StyleSheetBuilder.build_button_style(theme, button_type))
        return button

    def create_result_item(self, label, value, theme):
        """创建结果显示项"""
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid {theme['glass_border']};
                border-radius: 8px;
                padding: 12px;
            }}
        """)
        
        layout = QHBoxLayout(container)
        layout.setContentsMargins(12, 8, 12, 8)
        
        label_widget = QLabel(label + ":")
        label_widget.setFont(QFont("微软雅黑", 10, QFont.Weight.Bold))
        label_widget.setStyleSheet(f"color: {theme['accent_color']};")
        label_widget.setMinimumWidth(70)
        
        value_widget = QLabel(value)
        value_widget.setFont(QFont("微软雅黑", 11, QFont.Weight.Bold))
        value_widget.setStyleSheet(f"color: {theme['text_primary']};")
        value_widget.setWordWrap(True)
        
        layout.addWidget(label_widget)
        layout.addWidget(value_widget, 1)
        
        # 保存引用
        if "账号" in label:
            self.account_label_ref = value_widget
        elif "标题" in label:
            self.title_label_ref = value_widget
        else:
            self.status_label_ref = value_widget
        
        return container

    # ==================== 主题管理 ====================
    
    def apply_theme(self, theme_name):
        """应用主题"""
        self.current_theme = theme_name
        theme = ThemeManager.get_theme(theme_name)
        
        # 设置主窗口背景
        main_bg = f"""background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 {theme['bg_gradient_start']},
            stop:0.5 {theme['bg_gradient_mid']},
            stop:1 {theme['bg_gradient_end']});"""
        
        self.centralWidget().setStyleSheet(f"QWidget {{ {main_bg} }}")
        
        # 更新所有组件的样式
        self.update_all_styles()

    def on_theme_changed(self, index):
        """主题改变"""
        themes = ["dark", "sakura", "cyan"]
        if index < len(themes):
            self.apply_theme(themes[index])

    def update_all_styles(self):
        """更新所有样式"""
        # 这将在重新创建UI时调用，现在简单实现
        pass

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
        """立即查询"""
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
        
        self.query_signals.status_signal.emit("监控中...", "green")
        self.log("✓ 开始监控")
        
        threading.Thread(target=self._polling_loop, daemon=True).start()

    def stop_monitoring(self):
        """停止监控"""
        self.running = False
        self.stop_event.set()
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        
        self.query_signals.status_signal.emit("已停止", "gray")
        self.log("⏹️  已停止监控")

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
        self.query_signals.log_signal.emit(f"✓ 获取 token 成功")
        
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
        
        self.query_signals.log_signal.emit(f"✓ 查询成功 → {account} | 状态: {status}")
        self.query_signals.result_signal.emit(account, title, status)
        
        if status != "等待评阅" and self.last_status == "等待评阅":
            self.query_signals.log_signal.emit("⚠️  状态已变化！即将申请用户注意")
            self.show_alert(account, title, status)
        
        self.last_status = status

    def _extract_field(self, html, pattern):
        """提取字段"""
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
        """处理日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {msg}")

    def on_result(self, account, title, status):
        """处理结果"""
        self.account_label_ref.setText(account)
        self.title_label_ref.setText(title)
        
        if status != "等待评阅":
            self.status_label_ref.setStyleSheet("color: rgba(255, 100, 100, 0.95);")
        else:
            self.status_label_ref.setStyleSheet("color: rgba(100, 200, 100, 0.95);")
        
        self.status_label_ref.setText(status)

    def on_status_changed(self, text, color):
        """处理状态变化"""
        color_map = {
            "green": "rgba(100, 200, 100, 0.2)",
            "red": "rgba(200, 100, 100, 0.2)",
            "gray": "rgba(128, 128, 128, 0.2)",
        }
        theme = ThemeManager.get_theme(self.current_theme)
        self.status_label.setText(f"状态: {text}")
        self.status_label.setStyleSheet(f"""
            color: {theme['text_primary']};
            padding: 10px;
            border-radius: 8px;
            background: {color_map.get(color, color_map['gray'])};
        """)

    def log(self, msg):
        """记录日志"""
        self.query_signals.log_signal.emit(msg)

    def load_settings(self):
        """加载设置"""
        try:
            with open("thesis_settings.json", 'r') as f:
                settings = json.load(f)
                self.cookie_input.setText(settings.get("cookie", ""))
                self.pid_input.setText(settings.get("pid", ""))
                self.pwd_input.setText(settings.get("pwd", ""))
                self.interval_spin.setValue(settings.get("interval", 5))
        except:
            pass

    def closeEvent(self, event):
        """关闭时保存设置"""
        try:
            settings = {
                "cookie": self.cookie_input.text(),
                "pid": self.pid_input.text(),
                "pwd": self.pwd_input.text(),
                "interval": self.interval_spin.value(),
            }
            with open("thesis_settings.json", 'w') as f:
                json.dump(settings, f, ensure_ascii=False)
        except:
            pass
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = ThesisCheckerAdvanced()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
