import sys
import os
from PyQt6.QtWidgets import QApplication
from src.ui.floating_window import FloatingWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Floating Todo")
    
    # Create and show the main floating window
    window = FloatingWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
