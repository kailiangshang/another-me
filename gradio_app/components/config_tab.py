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
    
    gr.Markdown(
        """
        ## ⚙️ 系统配置
        
        配置 OpenAI 兼容的 API 以开始使用。支持 OpenAI、Azure OpenAI、本地模型（Ollama）等。
        """
    )
    
    with gr.Row():
        with gr.Column(scale=2):
            gr.Markdown("### 🔑 API 配置")
            
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
            gr.Markdown("### 💾 数据存储")
            
            gr.Markdown(
                """
                - 📁 数据目录: `/app/data/`
                - 📦 RAG 向量库: `/app/data/rag_vector_store/`
                - 💬 MEM 向量库: `/app/data/mem_vector_store/`
                - ⚙️ 配置文件: `/app/data/runtime_config.json`
                """
            )
            
            gr.Markdown("### ℹ️ 系统信息")
            
            status_label = "✅ 已配置" if state.get('is_configured') else "⚠️ 未配置"
            
            gr.Markdown(
                f"""
                - **版本**: v0.7.0
                - **AME 引擎**: v0.7.0
                - **前端框架**: Gradio
                - **状态**: {status_label}
                """
            )
