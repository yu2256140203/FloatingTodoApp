# Thesis 应用 - EXE 打包和发布指南 📦

## 📌 概述

本项目使用 **PyInstaller** 将 Python 应用打包为 Windows EXE 文件，通过 **GitHub Actions** 自动构建和发布。

用户无需安装 Python 环境，就可以直接运行应用。

---

## 🚀 快速使用

### 获取 EXE 文件

#### 方式1：从 GitHub Releases 下载（推荐）
1. 访问 [Releases 页面](../../releases)
2. 选择最新版本
3. 下载对应的 EXE 文件

#### 方式2：从 GitHub Actions 下载
1. 访问 [Actions 页面](../../actions)
2. 选择最新的 Build 工作流
3. 在 Artifacts 中下载 EXE 文件

#### 方式3：本地构建（Windows）
```batch
pip install pyinstaller
build.bat
:: EXE 文件将生成在 dist/ 文件夹
```

#### 方式4：本地构建（Linux/Mac）
```bash
pip install pyinstaller
chmod +x build.sh
./build.sh
# 可执行文件将生成在 dist/ 文件夹
```

---

## 📁 EXE 文件说明

### 🌟 ThesisChecker_Advanced.exe（推荐）
- **特点**：高级现代版本，最好看
- **功能**：
  - 三种主题可切换（深色、樱花粉、青幽）
  - 毛玻璃设计，优雅美观
  - 流畅动画效果
  - 所有功能完整
- **文件大小**：~150-200 MB
- **首次启动**：3-5 秒（加载 PyQt6）

### 🎨 ThesisChecker_Modern.exe
- **特点**：现代化版本
- **功能**：
  - 毛玻璃设计
  - 流畅动画
  - 单一色彩主题
- **文件大小**：~150-200 MB

### 🚀 ThesisChecker.exe（启动器）
- **特点**：智能启动器
- **功能**：
  - 自动启动最新推荐版本
  - 支持命令行参数选择版本
  - 推荐默认使用
- **使用**：
  ```batch
  ThesisChecker.exe            # 自动启动高级版
  ThesisChecker.exe --ui modern # 启动现代版
  ThesisChecker.exe --ui classic # 启动经典版
  ```

### 📱 ThesisChecker_Classic.exe
- **特点**：轻量级经典版
- **功能**：原始 Tkinter 界面，功能完整
- **文件大小**：~30-50 MB
- **优点**：较小文件，启动快速

### 💫 FloatingTodo.exe
- **特点**：悬浮任务管理应用
- **功能**：实时任务跟踪
- **文件大小**：~150-200 MB

---

## 🔧 本地构建指南

### Windows 用户

#### 前置条件
```batch
python --version  # 需要 Python 3.10+
pip install pyinstaller
```

#### 编译所有应用
```batch
REM 方式1：使用编译脚本（推荐）
build.bat

REM 方式2：手动编译单个应用
pyinstaller --noconsole --onefile ^
    --name "ThesisChecker_Advanced" ^
    --collect-all PyQt6 ^
    thesis_app_advanced.py
```

#### 输出文件
```
dist/
├── ThesisChecker_Advanced.exe
├── ThesisChecker_Modern.exe
├── ThesisChecker.exe
├── ThesisChecker_Classic.exe
└── FloatingTodo.exe
```

### Linux / macOS 用户

#### 前置条件
```bash
python3 --version  # 需要 Python 3.10+
pip install pyinstaller
```

#### 编译所有应用
```bash
chmod +x build.sh
./build.sh
```

#### 输出文件
```
dist/
├── ThesisChecker_Advanced
├── ThesisChecker_Modern
├── ThesisChecker
├── ThesisChecker_Classic
└── FloatingTodo
```

---

## 🔄 GitHub Actions 自动构建

### 工作流触发条件

自动构建会在以下情况触发：

1. **代码推送到 main 分支**
   ```bash
   git push origin main
   ```

2. **手动触发工作流**
   - 在 GitHub Actions 中选择 "Run workflow"

### 查看构建状态

1. 访问 [Actions 页面](../../actions)
2. 选择最新的 "Build Thesis Apps & FloatingTodo" 工作流
3. 查看构建进度

### 下载构建产物

1. 工作流完成后，点击工作流
2. 在页面下方找到 "Artifacts" 部分
3. 下载对应的 ZIP 文件

### 创建 Release

工作流支持自动创建 Release（当推送 tag 时）：

```bash
git tag -a v2.0.0 -m "Release version 2.0.0"
git push origin v2.0.0
```

---

## ⚙️ 打包配置详解

### PyInstaller 参数

```bash
--onefile                  # 生成单一可执行文件
--noconsole               # 不显示控制台窗口
--name NAME               # 指定输出文件名
--collect-all PyQt6       # 收集所有 PyQt6 资源
--collect-all Qt6         # 收集所有 Qt6 资源
--hidden-import MODNAME   # 指定隐式导入的模块
```

### 文件大小优化

当前生成的 EXE 文件大小较大（~150-200 MB），主要原因：

1. **PyQt6 库** - 包含所有 Qt6 核心库
2. **Python 运行时** - Python 解释器
3. **依赖库** - requests 等网络库

#### 减小文件大小的方法

```bash
# 1. 使用 UPX 压缩（可选）
pyinstaller ... --upx-dir=/path/to/upx

# 2. 移除不必要的数据文件
pyinstaller ... --exclude-module=matplotlib

# 3. 分离式打包（多个文件）
pyinstaller --onedir ...  # 生成文件夹而不是单一文件
```

---

## ✅ 测试清单

运行 EXE 前，确保满足以下条件：

### 系统要求
- [ ] Windows 10 或更高版本（对于 EXE）
- [ ] 至少 500 MB 磁盘空间
- [ ] 至少 2 GB RAM
- [ ] 网络连接（查询状态）

### 功能测试
- [ ] 应用正常启动
- [ ] 界面显示正确
- [ ] 输入框可编辑
- [ ] 按钮可点击
- [ ] 日志正常显示
- [ ] 主题切换有效（高级版）

### 打包测试
- [ ] EXE 文件可执行
- [ ] 无依赖 Python 安装
- [ ] 配置自动保存
- [ ] 跨网络查询成功

---

## 🐛 故障排除

### EXE 无法运行

**症状**：点击 EXE 无反应或闪退

**解决方案**：
1. 确保系统是 Windows 10 或更高
2. 检查是否需要安装 Visual C++ 运行库
   ```bash
   # 下载并安装：
   # https://aka.ms/vs/17/release/vc_redist.x64.exe
   ```
3. 尝试在命令行运行查看错误信息
   ```batch
   ThesisChecker_Advanced.exe
   ```

### 启动缓慢

**症状**：EXE 需要 5-10 秒才能启动

**原因**：
- PyQt6 库加载需要时间
- 首次启动需要初始化

**解决方案**：
- 这是正常现象，第一次启动会慢一些
- 后续启动会快一些（系统缓存）

### 运行时错误

**症状**：应用报告 DLL 或模块缺失

**解决方案**：
1. 重新下载 EXE 文件
2. 检查文件是否完整
3. 尝试从源代码重新构建

### PyQt6 相关错误

**症状**：".../qt66core.dll 文件未找到"

**解决方案**：
1. 确保完整下载了 EXE
2. 不要剪切或移动 EXE
3. 重新构建或下载最新版本

---

## 📊 构建统计

### 构建时间

| 应用 | 构建时间 |
|------|---------|
| ThesisChecker_Advanced | ~2-3 分钟 |
| ThesisChecker_Modern | ~2-3 分钟 |
| ThesisChecker (Launcher) | ~2-3 分钟 |
| ThesisChecker_Classic | ~1 分钟 |
| FloatingTodo | ~1-2 分钟 |
| **总计** | **~10-15 分钟** |

### 文件大小

| 应用 | 大小 |
|------|------|
| ThesisChecker_Advanced | ~170 MB |
| ThesisChecker_Modern | ~165 MB |
| ThesisChecker.exe | ~165 MB |
| ThesisChecker_Classic | ~40 MB |
| FloatingTodo | ~160 MB |

---

## 🎯 针对最终用户的说明

### 给非技术用户

如果您是最终用户，只需要：

1. **下载 EXE**
   - 访问 [Releases 页面](../../releases)
   - 下载 `ThesisChecker_Advanced.exe`（推荐）

2. **安装 EXE**
   - 双击下载的 EXE 文件
   - 等待 3-5 秒首次启动

3. **使用应用**
   - 填写配置信息
   - 点击开始监控

就这么简单！无需安装 Python 或配置任何环境。

---

## 📚 相关文档

- [使用指南](THESIS_QUICK_START.md)
- [完整文档](THESIS_APP_README.md)
- [升级说明](THESIS_UPGRADE_NOTICE.md)

---

## 📝 更新日志

### v2.0.0 - UI 升级版本
- ✅ 新增高级版本（三种主题）
- ✅ 新增现代版本（毛玻璃设计）
- ✅ 优化构建流程
- ✅ 完整的 exe 打包支持

### v1.0.0 - 初始版本
- ✅ 基础功能实现
- ✅ 原始 Tkinter 界面

---

**最后更新**: 2024年  
**当前版本**: 2.0.0
