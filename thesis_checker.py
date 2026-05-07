# -*- coding: utf-8 -*-
"""
NEUCSE 毕业论文盲审状态检查工具
自动轮询论文审核状态，状态变化时弹窗提醒
"""

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import re
import threading
import time
from datetime import datetime


class ThesisCheckerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NEUCSE 论文盲审状态检查工具")
        self.root.geometry("620x580")
        self.root.resizable(False, False)

        self.running = False
        self.timer_thread = None
        self.stop_event = threading.Event()

        self._build_ui()

    def _build_ui(self):
        # --- 顶部：Cookie 输入 ---
        frame_cookie = ttk.LabelFrame(self.root, text="配置", padding=10)
        frame_cookie.pack(fill="x", padx=10, pady=(10, 5))

        ttk.Label(frame_cookie, text="OPENCONF Cookie:").grid(row=0, column=0, sticky="w")
        self.cookie_var = tk.StringVar()
        self.cookie_entry = ttk.Entry(frame_cookie, textvariable=self.cookie_var, width=50)
        self.cookie_entry.grid(row=0, column=1, padx=(5, 0), sticky="ew")

        ttk.Label(frame_cookie, text="轮询间隔(分钟):").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.interval_var = tk.IntVar(value=5)
        self.interval_spin = ttk.Spinbox(
            frame_cookie, from_=1, to=60, textvariable=self.interval_var, width=10
        )
        self.interval_spin.grid(row=1, column=1, padx=(5, 0), sticky="w", pady=(8, 0))

        frame_cookie.columnconfigure(1, weight=1)

        # --- 控制按钮 ---
        frame_ctrl = ttk.Frame(self.root, padding=(10, 5))
        frame_ctrl.pack(fill="x")

        self.btn_start = ttk.Button(frame_ctrl, text="开始监控", command=self.start_monitoring)
        self.btn_start.pack(side="left")

        self.btn_stop = ttk.Button(frame_ctrl, text="停止", command=self.stop_monitoring, state="disabled")
        self.btn_stop.pack(side="left", padx=(10, 0))

        self.btn_once = ttk.Button(frame_ctrl, text="立即查询一次", command=self.query_once)
        self.btn_once.pack(side="left", padx=(10, 0))

        self.status_label = ttk.Label(frame_ctrl, text="状态: 未运行", foreground="gray")
        self.status_label.pack(side="right")

        # --- 结果展示 ---
        frame_result = ttk.LabelFrame(self.root, text="查询结果", padding=10)
        frame_result.pack(fill="x", padx=10, pady=5)

        self.lbl_account = ttk.Label(frame_result, text="账号: —")
        self.lbl_account.pack(anchor="w")

        self.lbl_title = ttk.Label(frame_result, text="论文标题: —")
        self.lbl_title.pack(anchor="w", pady=(4, 0))

        self.lbl_status = ttk.Label(frame_result, text="状态: —", font=("Microsoft YaHei", 11, "bold"))
        self.lbl_status.pack(anchor="w", pady=(4, 0))

        # --- 日志区域 ---
        frame_log = ttk.LabelFrame(self.root, text="日志", padding=5)
        frame_log.pack(fill="both", expand=True, padx=10, pady=(5, 10))

        self.log_text = tk.Text(frame_log, height=12, state="disabled", wrap="word",
                                font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(frame_log, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def log(self, msg):
        """向日志区域追加一行"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        def _append():
            self.log_text.configure(state="normal")
            self.log_text.insert("end", f"[{timestamp}] {msg}\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
        self.root.after(0, _append)

    def query_once(self):
        """立即执行一次查询（不启动轮询）"""
        cookie = self.cookie_var.get().strip()
        if not cookie:
            messagebox.showwarning("提示", "请先填写 OPENCONF Cookie")
            return
        threading.Thread(target=self._do_query, daemon=True).start()

    def start_monitoring(self):
        """开始轮询监控"""
        cookie = self.cookie_var.get().strip()
        if not cookie:
            messagebox.showwarning("提示", "请先填写 OPENCONF Cookie")
            return

        self.running = True
        self.stop_event.clear()
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.cookie_entry.configure(state="disabled")
        self.interval_spin.configure(state="disabled")
        self.status_label.configure(text="状态: 监控中…", foreground="green")
        self.log("开始监控")

        self.timer_thread = threading.Thread(target=self._polling_loop, daemon=True)
        self.timer_thread.start()

    def stop_monitoring(self):
        """停止轮询"""
        self.running = False
        self.stop_event.set()
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.cookie_entry.configure(state="normal")
        self.interval_spin.configure(state="normal")
        self.status_label.configure(text="状态: 已停止", foreground="gray")
        self.log("已停止监控")

    def _polling_loop(self):
        """轮询循环"""
        while not self.stop_event.is_set():
            self._do_query()
            # 等待指定间隔，但每秒检查一次停止信号
            interval_sec = self.interval_var.get() * 60
            self.root.after(0, lambda: self.status_label.configure(
                text=f"状态: 等待 {self.interval_var.get()} 分钟后下次查询…"))
            for _ in range(interval_sec):
                if self.stop_event.is_set():
                    return
                time.sleep(1)

    def _do_query(self):
        """执行一次 POST 请求并解析结果"""
        cookie_val = self.cookie_var.get().strip()
        url = "http://219.216.65.57/author/status.php"

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                      "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "connection": "keep-alive",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": f"OPENCONF={cookie_val}",
            "host": "219.216.65.57",
            "origin": "http://219.216.65.57",
            "referer": "http://219.216.65.57/author/status.php",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/148.0.0.0 Mobile Safari/537.36",
        }

        try:
            resp = requests.post(url, headers=headers, data="", timeout=15)
            resp.encoding = "utf-8"
            html = resp.text
        except requests.RequestException as e:
            self.log(f"请求失败: {e}")
            return

        account = self._extract_field(html, r"账号:</strong>\s*(.*?)\s*</p>")
        title = self._extract_field(html, r"论文标题:</strong>\s*(.*?)\s*</p>")
        status = self._extract_field(html, r"状态:</strong>\s*(.*?)\s*</p>")

        if not status:
            self.log("未能解析到状态信息，请检查 Cookie 是否有效")
            self.root.after(0, lambda: self._update_result("解析失败", "解析失败", "解析失败"))
            return

        self.log(f"查询成功 → 账号: {account} | 状态: {status}")
        self.root.after(0, lambda: self._update_result(account, title, status))

        # 状态不再是"等待评阅"时弹窗提醒
        if status != "等待评阅":
            self.root.after(0, lambda: self._alert_changed(account, title, status))

    def _extract_field(self, html, pattern):
        """用正则从 HTML 中提取字段"""
        m = re.search(pattern, html)
        return m.group(1).strip() if m else None

    def _update_result(self, account, title, status):
        """更新界面显示"""
        self.lbl_account.configure(text=f"账号: {account}")
        self.lbl_title.configure(text=f"论文标题: {title}")
        self.lbl_status.configure(text=f"状态: {status}")

        if status != "等待评阅":
            self.lbl_status.configure(foreground="red")
        else:
            self.lbl_status.configure(foreground="black")

    def _alert_changed(self, account, title, status):
        """状态变化时弹窗提醒"""
        self.log("!!! 状态已变化，弹窗提醒 !!!")
        messagebox.showinfo(
            "论文状态更新",
            f"您的论文状态已发生变化！\n\n"
            f"账号: {account}\n"
            f"论文标题: {title}\n"
            f"当前状态: {status}\n\n"
            f"请尽快登录系统查看。"
        )


def main():
    root = tk.Tk()
    app = ThesisCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
