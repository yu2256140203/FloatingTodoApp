#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyInstaller 打包配置脚本
用于正确打包 PyQt6 应用
"""

import os
import sys
from pathlib import Path

def get_pyinstaller_args(app_name, main_script):
    """获取 PyInstaller 参数"""
    args = [
        '--onefile',
        '--noconsole',
        f'--name={app_name}',
        '--collect-all=PyQt6',
        '--collect-all=Qt6',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=PyQt6.sip',
        '--hidden-import=thesis_themes',
        main_script
    ]
    return args

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python build_exe.py <app_name> <main_script>")
        print("示例: python build_exe.py ThesisChecker_Advanced thesis_app_advanced.py")
        sys.exit(1)
    
    import subprocess
    app_name = sys.argv[1]
    main_script = sys.argv[2]
    
    args = ['pyinstaller'] + get_pyinstaller_args(app_name, main_script)
    
    print(f"构建 {app_name}...")
    print(f"命令: {' '.join(args)}")
    
    result = subprocess.run(args)
    sys.exit(result.returncode)
