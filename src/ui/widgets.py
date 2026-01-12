from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QScrollArea, QCheckBox, QPushButton, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon, QFont

from .styles import StyleManager

class PillWidget(QWidget):
    clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("PillWidget")
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 0, 15, 0)
        
        self.label = QLabel("Thinking...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        # Transparent overlay for click intercept
        self.overlay = QWidget(self)
        self.overlay.setGeometry(self.rect())
        
    def set_text(self, text):
        self.label.setText(text)

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)
        
    def resizeEvent(self, event):
        self.overlay.resize(self.size())
        super().resizeEvent(event)

class TaskItem(QWidget):
    delete_requested = pyqtSignal(str) # ID
    status_changed = pyqtSignal(str, bool) # ID, is_checked
    
    def __init__(self, task_id, text, done=False, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.checkbox = QCheckBox(text)
        self.checkbox.setChecked(done)
        self.checkbox.setStyleSheet(StyleManager.checkbox_style())
        self.checkbox.stateChanged.connect(self.on_check)
        
        # Strikethrough effect on init
        self.update_style(done)

        layout.addWidget(self.checkbox)
        layout.addStretch()
        
        # Delete button (hidden by default, show on hover?) 
        # For simplicity, keeping it always visible but subtle
        self.del_btn = QPushButton("×")
        self.del_btn.setFixedSize(20, 20)
        self.del_btn.setFlat(True)
        self.del_btn.setStyleSheet("color: rgba(255,255,255,0.5); font-weight: bold;")
        self.del_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.del_btn.clicked.connect(lambda: self.delete_requested.emit(self.task_id))
        
        layout.addWidget(self.del_btn)
        
        self.setLayout(layout)

    def on_check(self, state):
        is_checked = (state == 2) # Qt.CheckState.Checked is 2
        self.update_style(is_checked)
        self.status_changed.emit(self.task_id, is_checked)

    def update_style(self, is_checked):
        font = self.checkbox.font()
        font.setStrikeOut(is_checked)
        self.checkbox.setFont(font)
        # Dim text if checked
        if is_checked:
            self.checkbox.setStyleSheet(StyleManager.checkbox_style() + "QCheckBox { color: rgba(255,255,255,0.5); }")
        else:
            self.checkbox.setStyleSheet(StyleManager.checkbox_style() + "QCheckBox { color: white; }")

class ExpandedWidget(QWidget):
    close_requested = pyqtSignal()
    add_task_requested = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ExpandedWidget")
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Tasks")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        
        close_btn = QPushButton("−") # Minimize symbol
        close_btn.setFixedSize(25, 25)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255,255,255,0.1);
                border-radius: 12px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover { background: rgba(255,255,255,0.2); }
        """)
        close_btn.clicked.connect(self.close_requested.emit)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        self.layout.addLayout(header_layout)
        
        # Input
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Add a task...")
        self.input_field.setStyleSheet(StyleManager.input_style())
        self.input_field.returnPressed.connect(self.on_add)
        self.layout.addWidget(self.input_field)
        
        # Scroll Area for tasks
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        
        self.task_container = QWidget()
        self.task_layout = QVBoxLayout()
        self.task_layout.setContentsMargins(0, 5, 0, 5)
        self.task_layout.setSpacing(2)
        self.task_layout.addStretch() # Push items up
        self.task_container.setLayout(self.task_layout)
        
        self.scroll.setWidget(self.task_container)
        self.layout.addWidget(self.scroll)
        
        self.setLayout(self.layout)

    def on_add(self):
        text = self.input_field.text().strip()
        if text:
            self.add_task_requested.emit(text)
            self.input_field.clear()

    def add_task_widget(self, widget):
        # Insert before the spacer (stretch)
        count = self.task_layout.count()
        self.task_layout.insertWidget(count - 1, widget)

    def clear_tasks(self):
        # Remove all widgets except the spacer
        while self.task_layout.count() > 1:
            item = self.task_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
