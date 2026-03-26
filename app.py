"""
Flask 后端服务器 - 支持流式响应
"""
import os
import json

import jsonify
from flask import Flask, render_template, request, Response, stream_with_context
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 全局变量存储助手实例
assistant = None


def get_assistant():
    """获取或创建天气助手实例"""
    global assistant
    if assistant is None:
        from weather_assistant import create_assistant
        api_key = os.getenv("DEEPSEEK_API_KEY")
        assistant = create_assistant(api_key)
    return assistant


@app.route('/')
def index():
    """渲染主页"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """处理聊天请求（非流式）"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': '消息不能为空'}), 400
        
        # 获取助手并发送消息
        assistant_instance = get_assistant()
        response = assistant_instance.chat(user_message)
        
        return json.dumps({
            'success': True,
            'response': response
        }), 200, {'Content-Type': 'application/json; charset=utf-8'}
        
    except Exception as e:
        return json.dumps({
            'success': False,
            'error': str(e)
        }), 500, {'Content-Type': 'application/json; charset=utf-8'}


@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """处理流式聊天请求"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            def error_generator():
                yield json.dumps({'error': '消息不能为空'}, ensure_ascii=False)
            return Response(stream_with_context(error_generator()), 
                          mimetype='application/json')
        
        # 获取助手
        assistant_instance = get_assistant()
        
        # 由于 LangChain 的流式输出需要特殊处理，这里使用简单方式
        # 先获取完整回复，然后模拟流式传输
        full_response = assistant_instance.chat(user_message)
        
        def generate():
            # 将完整回复分成小段模拟流式效果
            chunks = [full_response[i:i+50] for i in range(0, len(full_response), 50)]
            for chunk in chunks:
                yield json.dumps({
                    'chunk': chunk,
                    'done': False
                }, ensure_ascii=False) + '\n'
            
            # 发送完成信号
            yield json.dumps({
                'done': True
            }, ensure_ascii=False) + '\n'
        
        return Response(stream_with_context(generate()), 
                       mimetype='application/json')
        
    except Exception as e:
        error_message = str(e)
        def error_generator():
            yield json.dumps({
                'error': error_message
            }, ensure_ascii=False)
        return Response(stream_with_context(error_generator()), 
                       mimetype='application/json')


@app.route('/api/clear', methods=['POST'])
def clear_memory():
    """清除对话历史"""
    try:
        assistant_instance = get_assistant()
        assistant_instance.clear_memory()
        
        return json.dumps({
            'success': True
        }), 200, {'Content-Type': 'application/json; charset=utf-8'}
        
    except Exception as e:
        return json.dumps({
            'success': False,
            'error': str(e)
        }), 500, {'Content-Type': 'application/json; charset=utf-8'}


if __name__ == '__main__':
    # 检查 API 密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("警告：未找到 DEEPSEEK_API_KEY 环境变量")
        print("请设置环境变量后重新启动服务")
    
    print("=" * 50)
    print("🌤️  天气助手服务启动中...")
    print("=" * 50)
    print(f"📍 服务地址：http://localhost:5000")
    print(f"🤖 模型：DeepSeek-V3")
    print(f"🌡️  天气 API: wttr.in")
    print("=" * 50)
    
    # 启动 Flask 应用
    app.run(host='0.0.0.0', port=5000, debug=True)
