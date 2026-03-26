# 🌤️ AI 天气助手 - LangChain Function Calling Demo

这是一个基于 LangChain + DeepSeek + wttr.in API 的天气查询助手，支持网页流式对话。

## ✨ 功能特性

- 🤖 **智能对话**：基于 DeepSeek-V3 大模型的强大理解能力
- 🌡️ **实时天气**：使用 wttr.in API 获取全球城市实时天气数据
- 💬 **流式响应**：网页端实时流式显示回复，体验更佳
- 🎨 **精美界面**：现代化的 UI 设计，支持移动端
- 🧠 **对话记忆**：自动保存对话历史，上下文更连贯
- 🔧 **Function Calling**：LangChain Agent 自动调用天气查询工具

## 📁 项目结构

```
Function_Calling/
├── app.py                 # Flask 后端服务器
├── weather_tool.py        # 天气查询工具（wttr.in API 封装）
├── weather_assistant.py   # LangChain 天气助手核心逻辑
├── start.py              # 启动脚本（带依赖检查）
├── requirements.txt      # Python 依赖列表
├── .env.example          # 环境变量配置示例
├── templates/
│   └── index.html        # 前端对话界面
└── README.md             # 项目说明文档
```

## 🚀 快速开始

### 1. 安装依赖

确保你的 Python 版本 >= 3.8，然后安装依赖：

```bash
pip install flask langchain langchain-core langchain-community httpx python-dotenv
```

或者使用 requirements.txt：

```bash
pip install -r requirements.txt
```

### 2. 配置 API 密钥

复制环境变量配置文件：

```bash
cp .env .env
```

编辑 `.env` 文件，填入你的 DeepSeek API 密钥：

```
DEEPSEEK_API_KEY=your_actual_api_key_here
```

**获取 API 密钥**：访问 [DeepSeek 开放平台](https://platform.deepseek.com/) 注册并获取 API Key。

### 3. 运行应用

#### 方式一：使用启动脚本（推荐）

```bash
python start.py
```

启动脚本会自动检查依赖和配置是否正确。

#### 方式二：直接运行 Flask 应用

```bash
python app.py
```

### 4. 访问网页

打开浏览器访问：http://localhost:5000

## 💡 使用示例

在网页聊天框中输入：

```
北京今天天气怎么样？
```

或者

```
我想知道上海的天气情况
```

助手的回复示例：

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

## 🛠️ 技术栈

- **后端框架**：Flask 3.0.0
- **AI 框架**：LangChain 0.1.0
- **大模型**：DeepSeek-V3 (通过 DeepInfra)
- **天气 API**：wttr.in
- **HTTP 客户端**：httpx
- **前端**：原生 HTML + CSS + JavaScript

## 🔍 代码说明

### 核心组件

1. **weather_tool.py** - 天气查询工具
   - 封装 wttr.in API
   - 实现 LangChain BaseTool 接口
   - 支持异步调用

2. **weather_assistant.py** - 天气助手
   - LangChain Agent 核心逻辑
   - 对话记忆管理
   - 工具调用协调

3. **app.py** - Flask 服务器
   - RESTful API 接口
   - 流式响应支持
   - 前端页面渲染

4. **templates/index.html** - 前端界面
   - 现代化 UI 设计
   - 实时流式对话
   - 打字机效果

## ⚙️ 配置选项

你可以在 `weather_assistant.py` 中调整以下参数：

```python
self.llm = DeepInfra(
    model="deepseek-ai/DeepSeek-V3",  # 模型名称
    deepinfra_api_key=self.api_key,
    temperature=0.7,    # 温度参数（0-1，越高越随机）
    max_tokens=2048,    # 最大生成长度
    streaming=True      # 启用流式输出
)
```

## 🌐 API 端点

- `GET /` - 主页
- `POST /api/chat` - 普通聊天接口（非流式）
- `POST /api/chat/stream` - 流式聊天接口
- `POST /api/clear` - 清空对话历史

## 📝 注意事项

1. **API 密钥安全**：不要将 `.env` 文件提交到 Git 仓库
2. **网络要求**：需要能够访问 wttr.in 和 DeepInfra API
3. **速率限制**：注意 API 的调用频率限制
4. **生产部署**：建议使用 Gunicorn 等 WSGI 服务器部署

## 🐛 故障排除

### 问题 1：无法导入模块

确保已正确安装所有依赖：
```bash
pip install -r requirements.txt
```

### 问题 2：API 密钥错误

检查 `.env` 文件是否存在且配置正确：
```bash
print(os.getenv("DEEPSEEK_API_KEY"))
```

### 问题 3：天气查询失败

检查网络连接，确保能访问 wttr.in：
```bash
curl https://wttr.in/Beijing?format=j1
```

### 问题 4：端口被占用

如果 5000 端口被占用，修改 `app.py` 中的端口号：
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

## 🔄 扩展功能

你可以轻松扩展此项目：

1. **添加更多工具**：继承 `BaseTool` 类创建新工具
2. **更换模型**：修改 `weather_assistant.py` 中的 LLM 配置
3. **持久化存储**：添加数据库保存对话历史
4. **多用户支持**：为每个用户创建独立的会话

## 📄 License

MIT License

## 👏 致谢

- [LangChain](https://github.com/langchain-ai/langchain)
- [DeepSeek](https://www.deepseek.com/)
- [wttr.in](https://wttr.in/)
- [Flask](https://flask.palletsprojects.com/)

---

**祝你使用愉快！** 🎉

如有问题，欢迎反馈。
