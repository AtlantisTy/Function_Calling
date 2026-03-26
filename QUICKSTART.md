# 🌤️ AI 天气助手 - 快速开始指南

## 📋 第一步：安装依赖

### Windows 用户（推荐）
在 PowerShell 中运行：
```powershell
.\install.ps1
```

### 所有平台
```bash
pip install flask langchain langchain-core langchain-community httpx python-dotenv
```

或者：
```bash
pip install -r requirements.txt
```

---

## 🔑 第二步：配置 API 密钥

1. 复制配置文件：
   ```bash
   cp .env .env
   ```

2. 获取 DeepSeek API 密钥：
   - 访问 https://platform.deepseek.com/
   - 注册账号并获取 API Key

3. 编辑 `.env` 文件，填入你的 API 密钥：
   ```
   DEEPSEEK_API_KEY=sk-your-actual-api-key-here
   ```

---

## ✅ 第三步：测试系统（可选）

运行测试脚本验证所有组件是否正常工作：
```bash
python test.py
```

测试内容包括：
- ✅ 依赖包检查
- ✅ API 密钥验证
- ✅ 天气工具测试

---

## 🚀 第四步：启动应用

### 方式一：使用主启动文件（推荐）
```bash
python main.py
```

### 方式二：直接运行 Flask 应用
```bash
python app.py
```

启动成功后会显示：
```
==================================================
🌤️  天气助手服务启动中...
==================================================
📍 服务地址：http://localhost:5000
🤖 模型：DeepSeek-V3
🌡️  天气 API: wttr.in
==================================================
```

---

## 💬 第五步：开始对话

1. 打开浏览器访问：**http://localhost:5000**

2. 在聊天框中输入查询，例如：
   - "北京今天天气怎么样？"
   - "我想知道上海的天气"
   - "广州现在多少度？"

3. AI 助手会自动调用天气工具查询实时天气并回复你

---

## 🎯 示例对话

**你**: 北京今天天气怎么样？

**助手**: 
```
【北京 当前天气】
🌡️  温度：25°C
🔥 体感温度：27°C
💧 湿度：65%
🌤️  天气状况：晴
💨 风速：12 km/h
📊 气压：1013 mb
👁️ 能见度：10 km
☁️ 云量：20%

今天北京天气晴朗，温度适宜，非常适合户外活动！建议穿着轻薄的长袖衣物，记得涂抹防晒霜哦~
```

---

## ⚠️ 常见问题

### Q1: 提示找不到模块
**解决**: 确保已正确安装所有依赖
```bash
pip install flask langchain langchain-core langchain-community httpx python-dotenv
```

### Q2: API 密钥错误
**解决**: 
1. 检查 `.env` 文件是否存在
2. 确认 `DEEPSEEK_API_KEY` 已正确填写
3. 确保没有多余的空格或引号

### Q3: 端口被占用
**解决**: 修改 `app.py` 中的端口号（第 141 行）
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Q4: 天气查询失败
**解决**: 
1. 检查网络连接
2. 确认能访问 wttr.in（可访问 https://wttr.in/Beijing 测试）
3. 检查城市名称是否正确

---

## 🛠️ 开发说明

### 项目结构
```
Function_Calling/
├── main.py              # 主入口
├── start.py             # 启动脚本（带检查）
├── test.py              # 测试脚本
├── app.py               # Flask 后端
├── weather_tool.py      # 天气查询工具
├── weather_assistant.py # LangChain Agent
├── templates/
│   └── index.html       # 前端界面
└── .env                 # 环境变量配置
```

### 核心功能扩展

**添加新工具**：
1. 继承 `BaseTool` 类
2. 实现 `_run` 方法
3. 在 `weather_assistant.py` 中添加到 tools 列表

**更换模型**：
修改 `weather_assistant.py` 中的 LLM 配置

---

## 📞 技术支持

如遇到问题，请检查：
1. Python 版本 >= 3.8
2. 所有依赖是否正确安装
3. API 密钥是否有效
4. 网络连接是否正常

---

**祝你使用愉快！** 🎉
