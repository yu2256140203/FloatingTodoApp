# -*- mode: python ; coding: utf-8 -*-
# PyInstaller hook for PyQt6

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks.qt import qtbase_library_info

# Collect PyQt6 data files
datas = collect_data_files('PyQt6')

# Ensure plugins are included
from PyInstaller.utils.hooks import get_module_file_attribute
import os

pyqt6_path = os.path.dirname(get_module_file_attribute('PyQt6'))
plugins_path = os.path.join(pyqt6_path, 'Qt6', 'plugins')

if os.path.exists(plugins_path):
    datas.append((plugins_path, os.path.join('PyQt6', 'Qt6', 'plugins')))

# Hidden imports
hiddenimports = [
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'PyQt6.QtSql',
    'PyQt6.QtNetwork',
    'PyQt6.QtWebEngineWidgets',
    'PyQt6.sip',
]
