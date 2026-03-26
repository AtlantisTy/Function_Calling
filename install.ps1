# AI 天气助手 - 快速安装脚本 (PowerShell)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🌤️  AI 天气助手 - 安装向导" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python 版本
Write-Host "📦 检查 Python 版本..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 错误：未找到 Python，请确保已安装 Python 3.8+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📦 开始安装依赖包..." -ForegroundColor Yellow
Write-Host ""

# 安装依赖
$packages = @("flask", "langchain", "langchain-core", "langchain-community", "httpx", "python-dotenv")

foreach ($package in $packages) {
    Write-Host "正在安装 $package ..." -ForegroundColor Yellow
    try {
        pip install $package --quiet
        Write-Host "✅ $package 安装成功" -ForegroundColor Green
    } catch {
        Write-Host "❌ $package 安装失败" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "✅ 所有依赖安装完成！" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 检查 .env 文件
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  未找到 .env 文件，正在创建..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✅ 已创建 .env 文件" -ForegroundColor Green
    Write-Host ""
    Write-Host "💡 下一步：" -ForegroundColor Cyan
    Write-Host "1. 编辑 .env 文件，填入你的 DeepSeek API 密钥" -ForegroundColor White
    Write-Host "2. 运行 python main.py 启动应用" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "✅ .env 文件已存在" -ForegroundColor Green
    Write-Host ""
    Write-Host "💡 下一步：" -ForegroundColor Cyan
    Write-Host "运行 python main.py 启动应用" -ForegroundColor White
    Write-Host ""
}

Write-Host "按任意键继续..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
