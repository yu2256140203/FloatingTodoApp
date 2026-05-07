@echo off
echo ========================================
echo    Floating ToDo App - 启动脚本
echo ========================================
echo.

:: 检查是否安装了Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Node.js，请先安装Node.js
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)

:: 检查是否安装了依赖
if not exist "node_modules" (
    echo [信息] 首次运行，正在安装依赖...
    echo.
    npm install
    if %errorlevel% neq 0 (
        echo [错误] 安装依赖失败
        pause
        exit /b 1
    )
    echo.
    echo [信息] 依赖安装完成！
    echo.
)

:: 检查图标文件
if not exist "icon.png" (
    echo [警告] 未找到icon.png图标文件
    echo [提示] 请在项目目录放置一个256x256的PNG图标文件
    echo.
)

echo [信息] 正在启动应用...
echo.
npm start
