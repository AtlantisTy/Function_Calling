"""
LangChain + DeepSeek 天气助手主应用逻辑
"""
import os
from typing import List, Optional
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import create_agent

# 加载环境变量
load_dotenv()


class WeatherAssistant:
    """天气助手类 - 使用 LangChain 和 DeepSeek 模型"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化天气助手
        
        Args:
            api_key: DeepSeek API 密钥，如果为 None 则从环境变量读取
        """
        # 获取 API 密钥
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("未找到 DeepSeek API 密钥，请设置 DEEPSEEK_API_KEY 环境变量")
        
        # 导入天气工具
        from weather_tool import WeatherTool
        
        # 初始化工具列表
        self.tools = [WeatherTool()]
        
        # 初始化 LLM (使用 DeepSeek OpenAI 兼容 API)
        self.llm = ChatOpenAI(
            model="deepseek-chat",
            openai_api_key=self.api_key,
            openai_api_base="https://api.deepseek.com",
            temperature=0.7,
            max_tokens=2048,
            streaming=True
        )
        
        # 创建 system prompt
        self.system_prompt = """你是一个友好的天气助手，专门帮助用户查询天气信息。
你可以：
1. 查询任何城市的当前天气
2. 提供温度、湿度、风速等详细天气数据
3. 给出基于天气的穿衣和活动建议

请使用中文与用户交流。在调用天气查询工具之前，先确认用户要查询的城市名称。
如果用户没有指定城市，请礼貌地询问他们想查询哪个城市。

记住要保持友好、专业的态度，并在提供天气信息后给出一些实用的建议。"""
        
        # 创建 agent (使用新版 LangChain API)
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt
        )
        
        # 简单的对话历史存储
        self.chat_history = []
    
    def chat(self, user_input: str) -> str:
        """
        与助手进行对话
        
        Args:
            user_input: 用户输入
            
        Returns:
            助手的回复
        """
        try:
            # 使用新版 API 调用 agent
            response = self.agent.invoke(
                {"messages": [HumanMessage(content=user_input)]},
                config={"configurable": {"system_prompt": self.system_prompt}}
            )
            
            # 提取回复
            if isinstance(response, dict) and "messages" in response:
                last_message = response["messages"][-1]
                reply = last_message.content if hasattr(last_message, 'content') else str(last_message)
            else:
                reply = str(response)
            
            # 更新对话历史
            self.chat_history.append(HumanMessage(content=user_input))
            self.chat_history.append(AIMessage(content=reply))
            
            return reply
        except Exception as e:
            return f"发生错误：{str(e)}"
    
    def clear_memory(self):
        """清除对话历史"""
        self.chat_history = []
    
    def get_conversation_history(self) -> List:
        """获取对话历史"""
        return self.chat_history


def create_assistant(api_key: Optional[str] = None) -> WeatherAssistant:
    """
    创建天气助手实例的工厂函数
    
    Args:
        api_key: DeepSeek API 密钥
        
    Returns:
        WeatherAssistant 实例
    """
    return WeatherAssistant(api_key)


if __name__ == "__main__":
    # 测试代码
    print("欢迎使用天气助手！输入 'quit' 退出。")
    
    assistant = create_assistant()
    
    while True:
        user_input = input("\n你：").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("再见！")
            break
        
        if not user_input:
            continue
            
        response = assistant.chat(user_input)
        print(f"\n助手：{response}")
