"""
Another Me - Gradio 前端应用
基于 Gradio 构建的 AI 数字分身系统
"""

import gradio as gr
import sys
import os
from pathlib import Path

# 添加 AME 模块到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from components import (
    create_home_tab,
    create_config_tab,
    create_rag_tab,
    create_mem_tab,
    create_knowledge_manager_tab,
    create_memory_manager_tab,
    create_analysis_tab
)
from utils.session import init_session_state, get_session_state


# 全局状态初始化
init_session_state()


def create_app():
    """创建 Gradio 应用"""
    
    # 自定义 CSS
    custom_css = """
    .gradio-container {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    .logo-container {
        text-align: center;
        padding: 20px;
    }
    .logo-container img {
        max-width: 200px;
        border-radius: 10px;
    }
    .tab-nav button {
        font-size: 16px;
    }
    """
    
    # 创建主应用
    with gr.Blocks(
        title="Another Me - 世界上另一个我",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="purple",
        ),
        css=custom_css
    ) as app:
        
        # Logo 和标题
        logo_path = Path(__file__).parent.parent / "another me logo.jpg"
        if logo_path.exists():
            gr.Image(
                str(logo_path),
                label=None,
                show_label=False,
                container=False,
                elem_classes=["logo-container"]
            )
        
        gr.Markdown(
            """
            # 🌟 Another Me - 世界上另一个我
            
            **AI 数字分身系统** - 用你的知识和对话训练专属 AI
            
            ---
            """
        )
        
        # 创建标签页
        with gr.Tabs(elem_classes=["tab-nav"]) as tabs:
            
            # 主页
            with gr.TabItem("🏠 主页", id=0):
                create_home_tab()
            
            # 配置
            with gr.TabItem("⚙️ 配置", id=1):
                create_config_tab()
            
            # RAG 知识库
            with gr.TabItem("📚 RAG 知识库", id=2):
                create_rag_tab()
            
            # 知识库管理
            with gr.TabItem("📂 知识库管理", id=3):
                create_knowledge_manager_tab()
            
            # MEM 对话
            with gr.TabItem("💬 MEM 对话", id=4):
                create_mem_tab()
            
            # 记忆管理
            with gr.TabItem("🧠 记忆管理", id=5):
                create_memory_manager_tab()
            
            # 分析报告
            with gr.TabItem("📊 分析报告", id=6):
                create_analysis_tab()
        
        # 底部信息
        gr.Markdown(
            """
            ---
            
            **Another Me v0.7.0** | MIT License | Powered by Gradio & AME Engine
            """
        )
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
