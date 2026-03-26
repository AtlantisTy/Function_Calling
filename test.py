"""
测试脚本 - 验证项目组件是否正常工作
"""
import sys


def test_imports():
    """测试依赖包导入"""
    print("=" * 60)
    print("📦 测试依赖包导入")
    print("=" * 60)
    
    tests = [
        ("Flask", "flask"),
        ("LangChain", "langchain"),
        ("LangChain Core", "langchain_core"),
        ("LangChain Community", "langchain_community"),
        ("httpx", "httpx"),
        ("python-dotenv", "dotenv"),
    ]
    
    failed = []
    for name, module in tests:
        try:
            __import__(module)
            print(f"✅ {name}: OK")
        except ImportError as e:
            print(f"❌ {name}: FAILED - {e}")
            failed.append(name)
    
    print()
    return len(failed) == 0, failed


def test_weather_tool():
    """测试天气工具"""
    print("=" * 60)
    print("🌡️  测试天气查询工具")
    print("=" * 60)
    
    try:
        from tool.weather_tool import get_weather
        
        print("正在查询北京天气...")
        result = get_weather("Beijing")
        
        if result and "温度" in result:
            print("✅ 天气工具工作正常")
            print("\n示例输出:")
            print("-" * 60)
            print(result)
            print("-" * 60)
            return True
        else:
            print("⚠️  天气工具返回结果异常")
            return False
            
    except Exception as e:
        print(f"❌ 天气工具测试失败：{e}")
        return False


def test_env_setup():
    """测试环境变量配置"""
    print("=" * 60)
    print("🔑 测试环境变量配置")
    print("=" * 60)
    
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        api_key = os.getenv("DEEPSEEK_API_KEY")
        
        if not api_key:
            print("❌ 未找到 DEEPSEEK_API_KEY")
            print("\n请配置 .env 文件:")
            print("1. 复制 .env 为 .env")
            print("2. 在 .env 中填写你的 API 密钥")
            return False
        elif api_key == "your_api_key_here":
            print("⚠️  API 密钥仍为默认值，请修改 .env 文件")
            return False
        else:
            print("✅ API 密钥已正确配置")
            print(f"   (密钥格式：{api_key[:10]}...)")
            return True
            
    except Exception as e:
        print(f"❌ 环境变量测试失败：{e}")
        return False


def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "🌤️  AI 天气助手 - 系统测试" + " " * 15 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = {}
    
    # 测试 1: 依赖包
    results["dependencies"], failed_deps = test_imports()
    print()
    
    # 测试 2: 环境变量
    results["env"] = test_env_setup()
    print()
    
    # 测试 3: 天气工具（可选，需要网络）
    if results["dependencies"]:
        print("提示：天气工具测试需要网络连接，按 Ctrl+C 可跳过")
        try:
            results["weather"] = test_weather_tool()
        except KeyboardInterrupt:
            print("\n⏭️  跳过天气工具测试")
            results["weather"] = None
    else:
        print("⏭️  跳过天气工具测试（依赖包未安装）")
        results["weather"] = None
    
    print()
    
    # 汇总结果
    print("=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    total = len([r for r in results.values() if r is not None])
    passed = len([r for r in results.values() if r is True])
    
    print(f"\n通过：{passed}/{total}")
    
    if all(v is True for v in results.values()):
        print("\n✅ 所有测试通过！可以运行应用了。")
        print("\n启动命令：python main.py")
        return 0
    else:
        print("\n⚠️  部分测试未通过，请先解决上述问题。")
        
        if not results["dependencies"]:
            print("\n需要安装的依赖:")
            for dep in failed_deps:
                print(f"  - {dep}")
            print("\n安装命令：pip install flask langchain langchain-core langchain-community httpx python-dotenv")
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
