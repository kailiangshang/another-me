"""
配置页面组件
"""

import gradio as gr
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from ame.llm_caller.caller import LLMCaller
from utils.session import get_session_state, update_session_state, save_config


def test_api_connection(api_key, api_base_url, model):
    """测试 API 连接"""
    if not api_key:
        return "❌ 请先输入 API Key"
    
    try:
        llm = LLMCaller(api_key=api_key, base_url=api_base_url, model=model)
        # 简单测试
        import asyncio
        response = asyncio.run(llm.generate(
            messages=[{"role": "user", "content": "Hi"}],
            temperature=0.7,
            max_tokens=10
        ))
        return "✅ 连接成功！"
    except Exception as e:
        return f"❌ 连接失败: {str(e)}"


def save_api_config(api_key, api_base_url, model):
    """保存 API 配置"""
    state = get_session_state()
    
    update_session_state('api_key', api_key)
    update_session_state('api_base_url', api_base_url)
    update_session_state('model', model)
    
    save_config()
    
    return "✅ 配置已保存！"


def create_config_tab():
    """创建配置页面"""
    
    state = get_session_state()
    
    with gr.Column():
        gr.HTML(
            """
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 30px; border-radius: 15px; text-align: center; color: white;
                        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3); margin-bottom: 30px;">
                <h2 style="font-size: 1.8em; margin-bottom: 10px;">⚙️ 系统配置</h2>
                <p style="opacity: 0.95;">配置 OpenAI 兼容的 API 以开始使用。支持 OpenAI、Azure OpenAI、本地模型（Ollama）等。</p>
            </div>
            """
        )
    
    with gr.Row():
        with gr.Column(scale=2):
            gr.HTML(
                """
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;
                            border-left: 4px solid #667eea; margin-bottom: 20px;">
                    <h3 style="color: #667eea; margin-bottom: 10px;">🔑 API 配置</h3>
                    <p style="color: #666; font-size: 0.95em;">请填写你的 API 信息，数据将安全存储在本地</p>
                </div>
                """
            )
            
            api_key_input = gr.Textbox(
                label="API Key",
                value=state.get('api_key', ''),
                type="password",
                placeholder="输入你的 OpenAI API Key 或兼容格式的 API Key",
                info="API Key 将保存在本地，不会上传到任何服务器"
            )
            
            api_base_url_input = gr.Textbox(
                label="API Base URL",
                value=state.get('api_base_url', 'https://api.openai.com/v1'),
                placeholder="https://api.openai.com/v1",
                info="如使用本地模型可修改为 http://localhost:11434/v1"
            )
            
            model_input = gr.Textbox(
                label="模型名称",
                value=state.get('model', 'gpt-3.5-turbo'),
                placeholder="gpt-3.5-turbo",
                info="模型名称，如 gpt-4, gpt-3.5-turbo, llama2 等"
            )
            
            with gr.Row():
                save_btn = gr.Button("💾 保存配置", variant="primary")
                test_btn = gr.Button("🧪 测试连接")
            
            status_output = gr.Textbox(
                label="状态",
                interactive=False,
                show_label=False
            )
            
            # 绑定事件
            save_btn.click(
                fn=save_api_config,
                inputs=[api_key_input, api_base_url_input, model_input],
                outputs=[status_output]
            )
            
            test_btn.click(
                fn=test_api_connection,
                inputs=[api_key_input, api_base_url_input, model_input],
                outputs=[status_output]
            )
        
        with gr.Column(scale=1):
            gr.HTML(
                """
                <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                            padding: 20px; border-radius: 15px; margin-bottom: 20px;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <h3 style="color: #333; margin-bottom: 15px; text-align: center;">💾 数据存储</h3>
                    <div style="background: white; padding: 15px; border-radius: 10px; font-size: 0.9em; color: #555;">
                        <p style="margin: 8px 0;"><strong>📁 数据目录</strong></p>
                        <p style="margin: 5px 0; padding-left: 15px; color: #667eea;">/app/data/</p>
                        <p style="margin: 8px 0; margin-top: 15px;"><strong>📦 RAG 向量库</strong></p>
                        <p style="margin: 5px 0; padding-left: 15px; color: #667eea;">/app/data/rag_vector_store/</p>
                        <p style="margin: 8px 0; margin-top: 15px;"><strong>💬 MEM 向量库</strong></p>
                        <p style="margin: 5px 0; padding-left: 15px; color: #667eea;">/app/data/mem_vector_store/</p>
                        <p style="margin: 8px 0; margin-top: 15px;"><strong>⚙️ 配置文件</strong></p>
                        <p style="margin: 5px 0; padding-left: 15px; color: #667eea;">/app/data/runtime_config.json</p>
                    </div>
                </div>
                """
            )
            
            status_label = "✅ 已配置" if state.get('is_configured') else "⚠️ 未配置"
            status_color = "#27ae60" if state.get('is_configured') else "#e74c3c"
            
            gr.HTML(
                f"""
                <div style="background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
                            padding: 20px; border-radius: 15px;
                            box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <h3 style="color: #333; margin-bottom: 15px; text-align: center;">ℹ️ 系统信息</h3>
                    <div style="background: white; padding: 15px; border-radius: 10px; font-size: 0.9em; color: #555;">
                        <p style="margin: 8px 0;"><strong>💻 版本</strong>: v0.7.0</p>
                        <p style="margin: 8px 0;"><strong>🔧 AME 引擎</strong>: v0.7.0</p>
                        <p style="margin: 8px 0;"><strong>🌐 前端框架</strong>: Gradio 4.0</p>
                        <p style="margin: 8px 0;"><strong>🟢 状态</strong>: <span style="color: {status_color}; font-weight: 600;">{status_label}</span></p>
                    </div>
                </div>
                """
            )
