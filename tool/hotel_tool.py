"""
酒店工具模块，使用模拟数据返回
"""
from langchain_core.tools import BaseTool


class HotelTool(BaseTool):
    name: str = "hotel_query"
    description: str = "查询指定城市的当前酒店入住信息。使用此工具获取任何城市的实时酒店数据。"

    def _run(self, city: str) -> str:
        return f"""
            城市：{city}    
            如家酒店：剩余3间，大床房399，双人床299，单间100
            喜来登酒店：剩余4间，大床房799，双人床199，单间266
            7天假日酒店：剩余1间，标间99
        """
