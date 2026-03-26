"""
天气工具模块 - 封装 wttr.in 天气 API
"""
import httpx
from typing import Optional, Dict, Any
from langchain.tools import BaseTool


class WeatherTool(BaseTool):
    """查询天气信息的工具"""
    
    name: str = "weather_query"
    description: str = "查询指定城市的当前天气信息。使用此工具获取任何城市的实时天气数据。"
    
    def _run(self, city: str) -> str:
        """
        查询城市天气
        
        Args:
            city: 城市名称
            
        Returns:
            天气信息的文本描述
        """
        try:
            # 使用 wttr.in API 获取天气信息
            url = f"https://wttr.in/{city}?format=j1"
            
            with httpx.Client() as client:
                response = client.get(url, timeout=10.0)
                response.raise_for_status()
                data = response.json()
            
            # 解析天气数据
            if "current_condition" in data and len(data["current_condition"]) > 0:
                current = data["current_condition"][0]
                
                weather_info = {
                    "city": city,
                    "temperature": f"{current.get('temp_C', 'N/A')}°C",
                    "feels_like": f"{current.get('FeelsLikeC', 'N/A')}°C",
                    "humidity": f"{current.get('humidity', 'N/A')}%",
                    "weather_desc": current.get("weatherDesc", [{}])[0].get("value", "N/A"),
                    "wind_speed": f"{current.get('windspeedKmph', 'N/A')} km/h",
                    "pressure": f"{current.get('pressure', 'N/A')} mb",
                    "visibility": f"{current.get('visibility', 'N/A')} km",
                    "cloud_cover": f"{current.get('cloudcover', 'N/A')}%",
                }
                
                # 格式化输出
                result = f"""
【{city} 当前天气】
🌡️  温度：{weather_info['temperature']}
🔥 体感温度：{weather_info['feels_like']}
💧 湿度：{weather_info['humidity']}
🌤️  天气状况：{weather_info['weather_desc']}
💨 风速：{weather_info['wind_speed']}
📊 气压：{weather_info['pressure']}
👁️ 能见度：{weather_info['visibility']}
☁️ 云量：{weather_info['cloud_cover']}
"""
                return result.strip()
            else:
                return f"抱歉，无法获取 {city} 的天气信息。请检查城市名称是否正确。"
                
        except httpx.TimeoutException:
            return f"查询 {city} 天气超时，请稍后重试。"
        except httpx.HTTPError as e:
            return f"查询天气时发生错误：{str(e)}"
        except Exception as e:
            return f"发生未知错误：{str(e)}"
    
    async def _arun(self, city: str) -> str:
        """异步版本"""
        return self._run(city)


def get_weather(city: str) -> str:
    """
    便捷函数：直接调用天气查询
    
    Args:
        city: 城市名称
        
    Returns:
        天气信息字符串
    """
    tool = WeatherTool()
    return tool.run(city)


if __name__ == "__main__":
    # 测试
    print(get_weather("Beijing"))
