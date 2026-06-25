@echo off
echo ====================================
echo  营销风洞智能体沙盘平台 - Python后端
echo ====================================
echo.

cd /d "%~dp0"

echo [1/3] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [2/3] 安装依赖...
pip install -r requirements.txt

if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo [3/3] 启动服务...
echo.
echo 服务地址: http://localhost:3000
echo API文档: http://localhost:3000/docs
echo.
echo 按 Ctrl+C 停止服务
echo.

python main.py

pause