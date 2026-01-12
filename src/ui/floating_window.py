from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QGraphicsDropShadowEffect, QMenu, QColorDialog
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, QRect
from PyQt6.QtGui import QColor, QAction

from .widgets import PillWidget, ExpandedWidget, TaskItem
from .styles import StyleManager
from ..logic.todo_manager import TodoManager
from ..logic.settings import SettingsManager

class FloatingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.todo_manager = TodoManager()
        self.settings_manager = SettingsManager()
        self.oldPos = None
        self.is_expanded = False
        
        self.initUI()
        self.load_tasks_to_ui()

    def initUI(self):
        # Window Flags
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Main Layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        # Stacked Widget to swap between Pill and Expanded
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)
        
        # Widgets
        self.pill_widget = PillWidget()
        self.pill_widget.clicked.connect(self.expand_window)
        
        self.expanded_widget = ExpandedWidget()
        self.expanded_widget.close_requested.connect(self.collapse_window)
        self.expanded_widget.add_task_requested.connect(self.add_task)
        
        self.stack.addWidget(self.pill_widget)
        self.stack.addWidget(self.expanded_widget)
        
        # Start Collapsed
        self.resize(150, 50)
        self.apply_settings_features()
        self.update_pill_count()
        
        # Animation
        self.anim = QPropertyAnimation(self, b"size")
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.setDuration(400) # ms

    def apply_settings_features(self):
        opacity = self.settings_manager.get("opacity")
        color = self.settings_manager.get("theme_color")
        
        self.pill_widget.setStyleSheet(StyleManager.pill_style(opacity, color))
        self.expanded_widget.setStyleSheet(StyleManager.expanded_style(opacity))
        
        # Need to refresh text color if needed, but mainly bg
        
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background-color: #2d3436; color: white; border: 1px solid #636e72; } QMenu::item:selected { background-color: #6c5ce7; }")
        
        # Opacity Submenu
        opacity_menu = menu.addMenu("Opacity")
        for val in [0.2, 0.4, 0.6, 0.8, 1.0]:
            action = QAction(f"{int(val*100)}%", self)
            action.triggered.connect(lambda checked, v=val: self.change_opacity(v))
            opacity_menu.addAction(action)

        # Theme Color
        color_action = QAction("Change Theme Color", self)
        color_action.triggered.connect(self.change_theme_color)
        menu.addAction(color_action)
        
        menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        menu.addAction(quit_action)
        
        menu.exec(event.globalPos())

    def change_opacity(self, value):
        self.settings_manager.set("opacity", value)
        self.apply_settings_features()

    def change_theme_color(self):
        color = QColorDialog.getColor(initial=QColor(self.settings_manager.get("theme_color")), parent=self, title="Pick Theme Color")
        if color.isValid():
            self.settings_manager.set("theme_color", color.name())
            self.apply_settings_features()

    def update_pill_count(self):
        count = self.todo_manager.get_pending_count()
        text = f"{count} Tasks" if count > 0 else "Todo"
        self.pill_widget.set_text(text)

    def load_tasks_to_ui(self):
        self.expanded_widget.clear_tasks()
        for todo in self.todo_manager.todos:
            self.create_task_item(todo)
        self.update_pill_count()

    def create_task_item(self, todo):
        item = TaskItem(todo['id'], todo['text'], todo['done'])
        item.delete_requested.connect(self.delete_task)
        item.status_changed.connect(self.update_task_status)
        self.expanded_widget.add_task_widget(item)

    def add_task(self, text):
        new_todo = self.todo_manager.add_todo(text)
        self.create_task_item(new_todo)
        self.update_pill_count()

    def delete_task(self, task_id):
        self.todo_manager.remove_todo(task_id)
        self.load_tasks_to_ui()

    def update_task_status(self, task_id, is_done):
        self.todo_manager.update_todo(task_id, is_done)
        self.update_pill_count()

    def expand_window(self):
        if self.is_expanded: return
        self.is_expanded = True
        self.stack.setCurrentWidget(self.expanded_widget)
        
        self.anim.setStartValue(self.size())
        self.anim.setEndValue(QSize(320, 450))
        self.anim.start()

    def collapse_window(self):
        if not self.is_expanded: return
        self.is_expanded = False
        
        self.anim.setStartValue(self.size())
        self.anim.setEndValue(QSize(150, 50))
        self.anim.finished.connect(self.on_collapse_finished)
        self.anim.start()

    def on_collapse_finished(self):
        self.stack.setCurrentWidget(self.pill_widget)
        self.anim.finished.disconnect(self.on_collapse_finished)

    # Drag Logic
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if  self.oldPos and event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.oldPos
            self.move(self.pos() + delta)
            self.oldPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.oldPos = None
