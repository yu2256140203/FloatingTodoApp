# 项目总览 📦

这是一个包含两个主要应用的项目：

1. **🎨 Thesis 论文盲审检查工具** - 高级现代版本 ⭐ 推荐
2. **💫 FloatingTodo 悬浮待办清单** - 桌面浮窗应用

---

## 🎨 Thesis 论文盲审检查工具

### 快速获取 EXE

#### 最简单方式：下载现成的 EXE
👉 **[前往 Releases 页面下载 EXE](../../releases)**

推荐下载 **ThesisChecker_Advanced.exe** ⭐

#### 使用 GitHub Actions 自动构建
1. 代码自动构建（每次 push）
2. 在 [Actions 页面](../../actions) 下载 artifacts

#### 本地构建
```bash
pip install -r requirements.txt
# Windows
build.bat

# Linux/Mac
./build.sh
```

### 📱 Thesis 应用版本

| 版本 | 推荐度 | 特点 | 大小 |
|------|--------|------|------|
| **ThesisChecker_Advanced.exe** ⭐ | ⭐⭐⭐⭐⭐ | 高级、3主题、毛玻璃、最好看 | 170MB |
| **ThesisChecker_Modern.exe** | ⭐⭐⭐⭐ | 现代化、毛玻璃、流畅动画 | 165MB |
| **ThesisChecker.exe** | ⭐⭐⭐⭐⭐ | 智能启动器 | 165MB |
| **ThesisChecker_Classic.exe** | ⭐⭐ | 轻量级、经典界面 | 40MB |

### 🎯 快速开始

1. 下载 `ThesisChecker_Advanced.exe`
2. 双击运行
3. 填写配置（Cookie、账号、密码）
4. 点击"开始监控"

📖 **[详细使用指南 →](DEPLOYMENT_GUIDE.md)**

---

## 💫 FloatingTodo 悬浮待办清单

一款简约、美观的桌面悬浮待办事项软件。支持半透明玻璃拟态、颜色自定义，轻量级。

### ✨ 功能特点

- **桌面悬浮胶囊**：默认只显示一个小胶囊，不占用桌面空间。
- **展开式清单**：点击胶囊展开完整待办列表。
- **个性化设置**：
  - 右键菜单调节 **透明度** (20% - 100%)。
  - 右键菜单调节 **主题色** (任意颜色)。
- **数据持久化**：自动保存即使关闭程序也不会丢失数据。

### 🚀 获取 FloatingTodo EXE

👉 **[下载 FloatingTodo.exe(Releases 页面)](../../releases)**

或使用 GitHub Actions 构建后在 Artifacts 下载

---

## 🛠️ 本地开发

### 前置要求
- Python 3.10+
- pip

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行应用

**Thesis 应用**
```bash
# 自动选择最佳版本
python run_thesis.py

# 或选择特定版本
python thesis_app_advanced.py   # 高级版
python thesis_app_modern.py     # 现代版
python thesis_checker.py        # 经典版
```

**FloatingTodo**
```bash
python main.py
```

---

## 📦 自动构建与发布

### GitHub Actions 工作流

每次 push 到 main 分支时自动构建：

1. **自动构建触发**
   - `git push origin main` 自动构建 EXE

2. **下载构建产物**
   - 在 [Actions](../../actions) 页面查看构建进度
   - 完成后在 Artifacts 中下载

3. **创建 Release**
   ```bash
   git tag -a v2.0.0 -m "Release v2.0.0"
   git push origin v2.0.0
   # EXE 将自动上传到 Releases 页面
   ```

### 构建文件说明

| 文件 | 说明 |
|------|------|
| `.github/workflows/build.yml` | GitHub Actions 工作流配置 |
| `build.bat` | Windows 本地构建脚本 |
| `build.sh` | Linux/Mac 本地构建脚本 |
| `requirements.txt` | 运行时依赖 |
| `requirements-build.txt` | 构建时依赖 |

---

## 📚 文档导航

### Thesis 应用文档
- **[快速开始 ]( THESIS_QUICK_START.md)** - 5分钟快速入门
- **[完整使用指南](THESIS_APP_README.md)** - 所有功能详解
- **[升级说明](THESIS_UPGRADE_NOTICE.md)** - UI 升级详情
- **[部署指南](DEPLOYMENT_GUIDE.md)** - EXE 获取和使用
- **[构建和发布](BUILD_AND_RELEASE.md)** - 开发者构建指南

---

## 🎯 项目结构

```
FloatingTodoApp/
├── 📋 Thesis应用
│   ├── thesis_app_advanced.py      # 高级版（推荐）
│   ├── thesis_app_modern.py        # 现代版
│   ├── thesis_themes.py            # 主题系统
│   ├── thesis_checker.py           # 经典版
│   └── run_thesis.py               # 启动器
├── 💫 FloatingTodo应用
│   ├── main.py
│   └── FloatingTodoApp/
├── 🔨 构建脚本
│   ├── build.bat                   # Windows 构建
│   ├── build.sh                    # Linux/Mac 构建
│   └── build_exe.py                # Python 构建工具
├── ⚙️ 配置
│   ├── requirements.txt            # 依赖
│   ├── requirements-build.txt      # 构建依赖
│   └── .github/workflows/build.yml # CI/CD
└── 📖 文档
    ├── README.md                   # 本文件
    ├── DEPLOYMENT_GUIDE.md         # 部署指南
    └── BUILD_AND_RELEASE.md        # 构建指南
```

---

## ✅ 快速清单

- [ ] 下载 EXE 文件？👉 **[Releases 页面](../../releases)**
- [ ] 想了解 Thesis 应用？👉 **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**
- [ ] 想本地构建？👉 **[BUILD_AND_RELEASE.md](BUILD_AND_RELEASE.md)**
- [ ] 遇到问题？👉 **[THESIS_QUICK_START.md](THESIS_QUICK_START.md#快速帮助)**

---

## 🎉 推荐版本

### 最好的体验
👉 **下载 ThesisChecker_Advanced.exe**
- 三种主题可选
- 毛玻璃设计
- 流畅动画
- 二次元风格

### 最轻量的选择
👉 **下载 ThesisChecker_Classic.exe**
- 仅 40MB
- 功能完整
- 启动快速

---

## 📞 获取帮助

- **使用问题** → [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#️-常见问题)
- **构建问题** → [BUILD_AND_RELEASE.md](BUILD_AND_RELEASE.md#-故障排除)
- **Thesis 使用** → [THESIS_QUICK_START.md](THESIS_QUICK_START.md)

---

**版本**: 2.0.0  
**最后更新**: 2024年  
**推荐版本**: Thesis Advanced Edition ⭐⭐⭐⭐⭐
