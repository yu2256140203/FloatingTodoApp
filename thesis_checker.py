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
        self.root.geometry("620x620")
        self.root.resizable(False, False)

        self.running = False
        self.timer_thread = None
        self.stop_event = threading.Event()
        self.last_status = None  # 用于检测状态变化

        self._build_ui()

    def _build_ui(self):
        # --- 顶部：配置输入 ---
        frame_cfg = ttk.LabelFrame(self.root, text="配置", padding=10)
        frame_cfg.pack(fill="x", padx=10, pady=(10, 5))

        ttk.Label(frame_cfg, text="OPENCONF Cookie:").grid(row=0, column=0, sticky="w")
        self.cookie_var = tk.StringVar()
        ttk.Entry(frame_cfg, textvariable=self.cookie_var, width=55).grid(
            row=0, column=1, padx=(5, 0), sticky="ew")

        ttk.Label(frame_cfg, text="账号 (pid):").grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.pid_var = tk.StringVar()
        ttk.Entry(frame_cfg, textvariable=self.pid_var, width=55).grid(
            row=1, column=1, padx=(5, 0), sticky="w", pady=(8, 0))

        ttk.Label(frame_cfg, text="密码 (pwd):").grid(row=2, column=0, sticky="w", pady=(8, 0))
        self.pwd_var = tk.StringVar()
        ttk.Entry(frame_cfg, textvariable=self.pwd_var, width=55, show="*").grid(
            row=2, column=1, padx=(5, 0), sticky="w", pady=(8, 0))

        ttk.Label(frame_cfg, text="轮询间隔(分钟):").grid(row=3, column=0, sticky="w", pady=(8, 0))
        self.interval_var = tk.IntVar(value=5)
        ttk.Spinbox(frame_cfg, from_=1, to=60, textvariable=self.interval_var, width=10).grid(
            row=3, column=1, padx=(5, 0), sticky="w", pady=(8, 0))

        frame_cfg.columnconfigure(1, weight=1)

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

        self.log_text = tk.Text(frame_log, height=10, state="disabled", wrap="word",
                                font=("Consolas", 9))
        scrollbar = ttk.Scrollbar(frame_log, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def log(self, msg):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        def _append():
            self.log_text.configure(state="normal")
            self.log_text.insert("end", f"[{timestamp}] {msg}\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
        self.root.after(0, _append)

    def _check_inputs(self):
        if not self.cookie_var.get().strip():
            messagebox.showwarning("提示", "请填写 OPENCONF Cookie")
            return False
        if not self.pid_var.get().strip():
            messagebox.showwarning("提示", "请填写账号 (pid)")
            return False
        if not self.pwd_var.get().strip():
            messagebox.showwarning("提示", "请填写密码 (pwd)")
            return False
        return True

    def query_once(self):
        if not self._check_inputs():
            return
        threading.Thread(target=self._do_query, daemon=True).start()

    def start_monitoring(self):
        if not self._check_inputs():
            return

        self.running = True
        self.stop_event.clear()
        self.last_status = None
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        for w in [self.cookie_var, self.pid_var, self.pwd_var]:
            # disable entry widgets via their master
            pass
        self.status_label.configure(text="状态: 监控中…", foreground="green")
        self.log("开始监控")

        self.timer_thread = threading.Thread(target=self._polling_loop, daemon=True)
        self.timer_thread.start()

    def stop_monitoring(self):
        self.running = False
        self.stop_event.set()
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.status_label.configure(text="状态: 已停止", foreground="gray")
        self.log("已停止监控")

    def _polling_loop(self):
        while not self.stop_event.is_set():
            self._do_query()
            interval_sec = self.interval_var.get() * 60
            self.root.after(0, lambda: self.status_label.configure(
                text=f"状态: 等待 {self.interval_var.get()} 分钟后下次查询…"))
            for _ in range(interval_sec):
                if self.stop_event.is_set():
                    return
                time.sleep(1)

    def _do_query(self):
        """两步请求：GET 获取 token -> POST 提交表单"""
        cookie_val = self.cookie_var.get().strip()
        pid = self.pid_var.get().strip()
        pwd = self.pwd_var.get().strip()
        base_url = "http://219.216.65.57/author/status.php"

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,"
                      "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "cookie": f"OPENCONF={cookie_val}",
            "host": "219.216.65.57",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/148.0.0.0 Mobile Safari/537.36",
        }

        session = requests.Session()

        # 第一步：GET 表单页面，获取 hidden token
        try:
            self.log("正在获取表单 token…")
            resp_get = session.get(base_url, headers=headers, timeout=15)
            resp_get.encoding = "utf-8"
            html_form = resp_get.text
        except requests.RequestException as e:
            self.log(f"GET 请求失败: {e}")
            return

        token_match = re.search(r'name="token"\s+value="([^"]+)"', html_form)
        if not token_match:
            self.log("未能获取 token，请检查 Cookie 是否有效")
            return
        token = token_match.group(1)
        self.log(f"获取 token 成功: {token[:16]}…")

        # 第二步：POST 提交表单
        post_data = {
            "ocaction": "Check Status",
            "token": token,
            "pid": pid,
            "pwd": pwd,
        }

        post_headers = {
            **headers,
            "content-type": "application/x-www-form-urlencoded",
            "origin": "http://219.216.65.57",
            "referer": base_url,
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "1",
        }

        try:
            self.log("正在提交查询…")
            resp_post = session.post(base_url, headers=post_headers, data=post_data, timeout=15)
            resp_post.encoding = "utf-8"
            html_result = resp_post.text
        except requests.RequestException as e:
            self.log(f"POST 请求失败: {e}")
            return

        # 检查是否返回错误信息
        err_match = re.search(r'class="warn"[^>]*>(.*?)</span>', html_result)
        if err_match:
            err_msg = err_match.group(1).strip()
            self.log(f"查询失败: {err_msg}")
            self.root.after(0, lambda: self._update_result("—", "—", f"错误: {err_msg}"))
            return

        account = self._extract_field(html_result, r"账号:</strong>\s*(.*?)\s*</p>")
        title = self._extract_field(html_result, r"论文标题:</strong>\s*(.*?)\s*</p>")
        status = self._extract_field(html_result, r"状态:</strong>\s*(.*?)\s*</p>")

        if not status:
            self.log("未能解析到状态信息，请检查账号密码和 Cookie")
            self.root.after(0, lambda: self._update_result("解析失败", "解析失败", "解析失败"))
            return

        self.log(f"查询成功 → 账号: {account} | 状态: {status}")
        self.root.after(0, lambda: self._update_result(account, title, status))

        # 状态不再是"等待评阅"时弹窗提醒
        if status != "等待评阅" and self.last_status == "等待评阅":
            self.root.after(0, lambda: self._alert_changed(account, title, status))
        self.last_status = status

    def _extract_field(self, html, pattern):
        m = re.search(pattern, html)
        return m.group(1).strip() if m else None

    def _update_result(self, account, title, status):
        self.lbl_account.configure(text=f"账号: {account}")
        self.lbl_title.configure(text=f"论文标题: {title}")
        self.lbl_status.configure(text=f"状态: {status}")
        if status != "等待评阅":
            self.lbl_status.configure(foreground="red")
        else:
            self.lbl_status.configure(foreground="black")

    def _alert_changed(self, account, title, status):
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
    ThesisCheckerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
