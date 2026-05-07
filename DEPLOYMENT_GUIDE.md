# 🚀 快速部署指南 - Thesis 应用 EXE 版本

## 📥 一键获取 EXE 文件

### 选项 A：从 GitHub Releases 下载（推荐）✅

最简单的方式，无需任何技术知识：

1. **打开 Releases 页面**
   - 访问：https://github.com/yu2256140203/FloatingTodoApp/releases

2. **找到最新版本**
   - 查找标记为 "Latest" 的版本

3. **下载 EXE 文件**
   - 推荐下载：`ThesisChecker_Advanced.exe` ⭐
   - 或根据需要选择其他版本

4. **运行**
   - 双击 EXE 文件即可运行
   - 无需 Python 环境！

---

### 选项 B：从 GitHub Actions 下载

如果最新的 Release 还未发布：

1. **打开 Actions 页面**
   - 访问：https://github.com/yu2256140203/FloatingTodoApp/actions

2. **选择最新的构建**
   - 点击 "Build Thesis Apps & FloatingTodo"
   - 选择最上面的（最新）构建

3. **下载 Artifacts**
   - 向下滚动到 "Artifacts" 部分
   - 下载对应的 artifact（如 `ThesisChecker-Advanced`）

4. **解压和运行**
   - 解压下载的 ZIP 文件
   - 运行其中的 EXE 文件

---

## 📦 EXE 版本选择

### 🌟 ThesisChecker_Advanced.exe（推荐）
```
特点：最好看，功能最完整
大小：~170 MB
特性：
  ✅ 三种主题可切换
  ✅ 毛玻璃设计
  ✅ 流畅动画
  ✅ 二次元风格
推荐度：⭐⭐⭐⭐⭐
```

### 🎨 ThesisChecker_Modern.exe
```
特点：现代化设计
大小：~165 MB
特性：
  ✅ 毛玻璃设计
  ✅ 流畅动画
  ✅ 单一色彩主题
推荐度：⭐⭐⭐⭐
```

### 🚀 ThesisChecker.exe（启动器）
```
特点：智能启动器，自动选择最佳版本
大小：~165 MB
使用：
  双击运行 → 自动启动高级版
  或命令行: ThesisChecker.exe --ui modern
推荐度：⭐⭐⭐⭐⭐
```

### 📱 ThesisChecker_Classic.exe
```
特点：轻量级经典版本
大小：~40 MB（最小）
特性：
  ✅ 轻量级
  ✅ 启动快
  ✅ 功能完整
推荐度：⭐⭐✅
```

---

## ⚡ 快速开始（5 步）

### 第一步：下载
Download one of the EXE files from Releases

### 第二步：运行
双击下载的 EXE 文件

### 第三步：等待
首次启动需要 3-5 秒（第一次加载 PyQt6）

### 第四步：配置
```
OPENCONF Cookie: [从浏览器获取]
账号 (pid):      [你的账号]
密码 (pwd):      [你的密码]
轮询间隔:        [5-10 分钟]
```

### 第五步：开始监控
点击 "🚀 开始监控" 按钮

---

## 🔑 获取 Cookie（必需）

### 步骤

1. **打开浏览器**
   - 访问 NEUCSE 系统网址
   - 登录你的账号

2. **打开开发者工具**
   - 按键盘快捷键：`F12`
   - 或右键 → 检查元素

3. **找到 Cookie**
   - 选择 "Application" 标签
   - 点击左侧 "Cookies"
   - 选择 NEUCSE 网址
   - 在列表中找 "OPENCONF"

4. **复制值**
   - 点击该行，复制整个 "Value" 值
   - 粘贴到应用的 Cookie 输入框

---

## 💻 系统要求

| 需求 | 最低要求 |
|------|---------|
| 操作系统 | Windows 7 SP1 或更高 |
| 处理器 | Intel/AMD 1GHz+ |
| 内存 | 2 GB RAM |
| 磁盘 | 500 MB 空闲空间 |
| 网络 | 互联网连接 |

---

## ⚠️ 常见问题

### Q: 无需 Python 环境吗？
**A**: 是的！EXE 文件包含了所有需要的 Python 环境，完全独立运行。

### Q: 文件这么大（170 MB）为什么？
**A**: 包含了 Python 解释器、PyQt6 库和所有依赖。这是正常的。

### Q: 首次启动为什么这么慢？
**A**: 首次启动需要初始化 PyQt6 库，通常需要 3-5 秒。这是正常的。

### Q: 能在公司电脑上使用吗？
**A**: 通常可以。只要是 Windows 7 或更高版本，就可以运行。如果遇到IT限制，联系 IT 部门。

### Q: 密码安全吗？
**A**: 密码只保存在你的电脑本地（`thesis_settings.json`），不会上传到网络。

### Q: 能运行在 Mac 或 Linux 上吗？
**A**: 当前提供 Windows EXE。Mac/Linux 用户需要从源代码运行或请求支持。

---

## 🚨 故障排除

### 问题：EXE 无法运行

**检查清单**：
- [ ] 是否是 Windows 7 或更高版本？
- [ ] 是否有足够的磁盘空间？
- [ ] 是否需要安装 C++ 运行库？

**解决方案**：
```
1. 下载 Visual C++ Runtime：
   https://aka.ms/vs/17/release/vc_redist.x64.exe

2. 安装后重试运行 EXE
```

### 问题：启动后立即闪退

**尝试**：
1. 在命令行中运行 EXE 查看错误信息
2. 重新下载最新版本
3. 检查病毒软件是否阻止

### 问题：运行时出错

**解决方案**：
1. 更新 Windows 系统
2. 重新下载 EXE
3. 查看错误信息并反馈

---

## 📱 使用建议

### 对于学生用户
1. 下载 **ThesisChecker_Advanced.exe**（最好看）
2. 配置好后后台运行
3. 等待状态变化提醒

### 对于技术用户
1. 可以选择 **ThesisChecker_Modern.exe**（轻量现代）
2. 或 **ThesisChecker.exe**（启动器，灵活）
3. 或 **ThesisChecker_Classic.exe**（最轻量）

### 对于所有用户
- 建议轮询间隔设为 5-10 分钟
- 安全妥善保管密码
- 定期更新到最新版本

---

## 🔄 更新应用

### 自动更新
当前版本不支持自动更新，需要手动下载最新版本。

### 手动更新步骤
1. 访问 [Releases 页面](../../releases)
2. 下载最新版本的 EXE
3. 替换旧版本的 EXE

旧的配置会自动保留（保存在 `thesis_settings.json`）。

---

## 📞 获取帮助

如果遇到问题：

1. **查看文档**
   - [完整使用指南](THESIS_QUICK_START.md)
   - [详细文档](THESIS_APP_README.md)

2. **检查日志**
   - 应用内的日志面板会显示详细错误信息

3. **提交问题**
   - 在 [Issues 页面](../../issues) 报告问题
   - 提供错误信息和系统信息

---

## ✅ 验证安装成功

安装完成后，验证以下事项：

- [ ] EXE 文件可双击运行
- [ ] 应用界面显示正常
- [ ] 输入框可以输入文本
- [ ] 按钮可以点击
- [ ] 日志面板显示信息
- [ ] 能够保存配置（下次启动时配置仍存在）

**如果以上都成功，恭喜！你已经可以开始使用了！** 🎉

---

## 📊 版本对比

| 特性 | Advanced ⭐ | Modern | Classic | 启动器 |
|------|-----------|--------|---------|--------|
| 美观度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | N/A |
| 主题 | 3种 | 1种 | 1种 | 自选 |
| 文件大小 | 170M | 165M | 40M | 165M |
| 启动速度 | 3-5s | 3-5s | 1-2s | 3-5s |
| 推荐 | ✅ | ✅ | ✅ | ✅ |

---

**准备好了吗？**

👉 [下载最新版本](../../releases)

**立即开始使用 Thesis 应用！** 🚀
