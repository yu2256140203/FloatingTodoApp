# -*- coding: utf-8 -*-
"""
高级主题管理和样式定义
为Thesis应用提供多种美观的主题
"""

class ThemeManager:
    """主题管理器"""
    
    # 主题定义 - 深色主题
    DARK_THEME = {
        "name": "Dark",
        "primary_start": "#667eea",
        "primary_end": "#764ba2",
        "secondary_start": "#4facfe",
        "secondary_end": "#00f2fe",
        "danger_start": "#f093fb",
        "danger_end": "#f5576c",
        "bg_gradient_start": "#0f172a",
        "bg_gradient_mid": "#1e3a5f",
        "bg_gradient_end": "#1a1a2e",
        "glass_bg": "rgba(255, 255, 255, 0.08)",
        "glass_border": "rgba(255, 255, 255, 0.2)",
        "text_primary": "rgba(255, 255, 255, 0.95)",
        "text_secondary": "rgba(255, 255, 255, 0.8)",
        "text_muted": "rgba(255, 255, 255, 0.6)",
        "accent_color": "rgba(102, 126, 234, 0.9)",
    }
    
    # 主题定义 - 樱花粉主题
    SAKURA_THEME = {
        "name": "Sakura",
        "primary_start": "#ff6b9d",
        "primary_end": "#c06c84",
        "secondary_start": "#ffa07a",
        "secondary_end": "#ff69b4",
        "danger_start": "#ff1493",
        "danger_end": "#ff69b4",
        "bg_gradient_start": "#fff0f5",
        "bg_gradient_mid": "#ffe4e1",
        "bg_gradient_end": "#ffd7e8",
        "glass_bg": "rgba(255, 105, 180, 0.08)",
        "glass_border": "rgba(255, 105, 180, 0.2)",
        "text_primary": "rgba(100, 50, 100, 0.95)",
        "text_secondary": "rgba(100, 50, 100, 0.8)",
        "text_muted": "rgba(100, 50, 100, 0.6)",
        "accent_color": "rgba(255, 105, 180, 0.9)",
    }
    
    # 主题定义 - 青幽主题
    CYAN_THEME = {
        "name": "Cyan",
        "primary_start": "#00f2fe",
        "primary_end": "#4facfe",
        "secondary_start": "#00d4ff",
        "secondary_end": "#0099ff",
        "danger_start": "#ff006e",
        "danger_end": "#fb5607",
        "bg_gradient_start": "#0a1428",
        "bg_gradient_mid": "#0d47a1",
        "bg_gradient_end": "#1a237e",
        "glass_bg": "rgba(0, 242, 254, 0.08)",
        "glass_border": "rgba(0, 242, 254, 0.2)",
        "text_primary": "rgba(255, 255, 255, 0.95)",
        "text_secondary": "rgba(255, 255, 255, 0.8)",
        "text_muted": "rgba(255, 255, 255, 0.6)",
        "accent_color": "rgba(0, 242, 254, 0.9)",
    }
    
    @staticmethod
    def get_theme(theme_name="dark"):
        """获取主题"""
        themes = {
            "dark": ThemeManager.DARK_THEME,
            "sakura": ThemeManager.SAKURA_THEME,
            "cyan": ThemeManager.CYAN_THEME,
        }
        return themes.get(theme_name.lower(), ThemeManager.DARK_THEME)


class StyleSheetBuilder:
    """样式表构建器"""
    
    @staticmethod
    def build_main_style(theme):
        """构建主窗口样式"""
        return f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {theme['bg_gradient_start']},
                    stop:0.5 {theme['bg_gradient_mid']},
                    stop:1 {theme['bg_gradient_end']});
            }}
        """
    
    @staticmethod
    def build_glass_panel_style(theme):
        """构建毛玻璃面板样式"""
        return f"""
            QFrame {{
                background: {theme['glass_bg']};
                border: 2px solid {theme['glass_border']};
                border-radius: 15px;
            }}
        """
    
    @staticmethod
    def build_button_style(theme, button_type="primary"):
        """构建按钮样式"""
        if button_type == "primary":
            return f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {theme['primary_start']},
                        stop:1 {theme['primary_end']});
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {theme['primary_end']},
                        stop:1 {theme['primary_start']});
                    box-shadow: 0 4px 16px {theme['accent_color']};
                }}
                QPushButton:pressed {{
                    padding: 12px 8px 8px 12px;
                }}
            """
        elif button_type == "danger":
            return f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {theme['danger_start']},
                        stop:1 {theme['danger_end']});
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {theme['danger_end']},
                        stop:1 {theme['danger_start']});
                }}
            """
        elif button_type == "info":
            return f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {theme['secondary_start']},
                        stop:1 {theme['secondary_end']});
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 {theme['secondary_end']},
                        stop:1 {theme['secondary_start']});
                }}
            """
    
    @staticmethod
    def build_input_style(theme):
        """构建输入框样式"""
        return f"""
            QLineEdit {{
                background: {theme['glass_bg']};
                border: 2px solid {theme['glass_border']};
                border-radius: 8px;
                color: {theme['text_primary']};
                padding: 8px 12px;
                selection-background-color: {theme['accent_color']};
            }}
            QLineEdit:focus {{
                border: 2px solid {theme['primary_start']};
                background: rgba(102, 126, 234, 0.12);
            }}
        """
    
    @staticmethod
    def build_text_edit_style(theme):
        """构建文本编辑框样式"""
        return f"""
            QTextEdit {{
                background: rgba(0, 0, 0, 0.3);
                border: 1px solid {theme['glass_border']};
                border-radius: 8px;
                color: rgba(100, 255, 100, 0.9);
                font-family: "Courier New", monospace;
                font-size: 10px;
                padding: 10px;
                selection-background-color: {theme['accent_color']};
            }}
            QTextEdit:focus {{
                border: 1px solid {theme['primary_start']};
            }}
        """
    
    @staticmethod
    def build_spinbox_style(theme):
        """构建SpinBox样式"""
        return f"""
            QSpinBox {{
                background: {theme['glass_bg']};
                border: 2px solid {theme['glass_border']};
                border-radius: 6px;
                color: {theme['text_primary']};
                padding: 4px 8px;
            }}
            QSpinBox:focus {{
                border: 2px solid {theme['primary_start']};
                background: rgba(102, 126, 234, 0.12);
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background: rgba(102, 126, 234, 0.3);
                border: none;
                border-radius: 3px;
                width: 20px;
            }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
                background: rgba(102, 126, 234, 0.5);
            }}
        """
