"""
项目启动脚本
"""
import os
import sys

def check_dependencies():
    """检查依赖包是否已安装"""
    required_packages = {
        'flask': 'Flask',
        'langchain': 'langchain',
        'langchain_core': 'langchain-core',
        'langchain_community': 'langchain-community',
        'httpx': 'httpx',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    for package_name, pip_name in required_packages.items():
        try:
            __import__(package_name)
        except ImportError:
            missing.append(pip_name)
    
    if missing:
        print("❌ 缺少以下依赖包：")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n请运行以下命令安装依赖：")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True


def check_api_key():
    """检查 API 密钥是否已配置"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    
    if not api_key or api_key == "your_api_key_here":
        print("⚠️  警告：未找到有效的 DeepSeek API 密钥")
        print("\n请按以下步骤配置：")
        print("1. 复制 .env 文件为 .env")
        print("2. 在 .env 文件中填写你的 DeepSeek API 密钥")
        print("3. 获取 API 密钥地址：https://platform.deepseek.com/")
        return False
    
    return True


def main():
    """主函数"""
    print("=" * 60)
    print("🌤️  AI 天气助手 - 启动检查")
    print("=" * 60)
    
    # 检查依赖
    print("\n📦 检查依赖包...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ 依赖包检查通过")
    
    # 检查 API 密钥
    print("\n🔑 检查 API 密钥...")
    if not check_api_key():
        print("\n💡 提示：配置完 API 密钥后请重新启动程序")
        sys.exit(1)
    print("✅ API 密钥检查通过")
    
    # 启动应用
    print("\n" + "=" * 60)
    print("🚀 启动服务...")
    print("=" * 60)
    
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == "__main__":
    main()
