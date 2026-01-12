class StyleManager:
    @staticmethod
    def get_base_style(opacity=0.9, theme_color="#6c5ce7"):
        # Glassmorphism background with customizable opacity
        bg_alpha = int(opacity * 255)
        return f"""
            QWidget {{
                color: white;
                font-family: 'Segoe UI', sans-serif;
            }}
            /* Scrollbar */
            QScrollBar:vertical {{
                border: none;
                background: transparent;
                width: 8px;
                margin: 0px 0px 0px 0px;
            }}
            QScrollBar::handle:vertical {{
                background: rgba(255, 255, 255, 0.2);
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """

    @staticmethod
    def pill_style(opacity=0.9, theme_color="#6c5ce7"):
        bg_alpha = int(opacity * 255)
        return f"""
            #PillWidget {{
                background-color: {theme_color}{bg_alpha:02x}; /* Hex + Alpha */
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 50);
            }}
            QLabel {{
                font-weight: bold;
                font-size: 14px;
            }}
        """

    @staticmethod
    def expanded_style(opacity=0.9):
        bg_alpha = int(opacity * 255)
        return f"""
            #ExpandedWidget {{
                background-color: rgba(20, 20, 35, {bg_alpha});
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 30);
            }}
        """
    
    @staticmethod
    def input_style():
        return """
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 5px;
                padding: 8px;
                color: white;
                selection-background-color: rgba(108, 92, 231, 100);
            }
            QLineEdit:focus {
                background-color: rgba(255, 255, 255, 0.15);
            }
        """

    @staticmethod
    def checkbox_style(theme_color="#6c5ce7"):
        return f"""
            QCheckBox {{
                spacing: 10px;
                font-size: 14px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 5px;
                border: 2px solid rgba(255, 255, 255, 0.5);
                background: transparent;
            }}
            QCheckBox::indicator:hover {{
                border-color: {theme_color};
            }}
            QCheckBox::indicator:checked {{
                background-color: {theme_color};
                border-color: {theme_color};
                image: none; /* Can add check icon here if needed */
            }}
        """
