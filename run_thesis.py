#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEUCSE 毕业论文盲审状态检查工具 - 启动器
支持经典、现代和高级三种UI风格
"""

import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="论文盲审检查工具")
    parser.add_argument("--ui", choices=["advanced", "modern", "classic"], default="advanced",
                        help="选择UI风格: advanced(高级版-推荐), modern(现代版), classic(经典版)")
    
    args = parser.parse_args()
    
    if args.ui == "advanced":
        print("启动高级现代版本（支持主题切换）...")
        try:
            from thesis_app_advanced import main as run_advanced
            run_advanced()
        except Exception as e:
            print(f"启动高级版本失败: {e}")
            print("尝试启动现代版本...")
            from thesis_app_modern import main as run_modern
            run_modern()
    elif args.ui == "modern":
        print("启动现代化UI版本...")
        from thesis_app_modern import main as run_modern
        run_modern()
    else:
        print("启动经典版本...")
        from thesis_checker import main as run_classic
        run_classic()

if __name__ == "__main__":
    main()
