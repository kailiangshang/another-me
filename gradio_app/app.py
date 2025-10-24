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
    
    # 自定义 CSS - 更现代化的设计
    custom_css = """
    /* 全局样式 */
    .gradio-container {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Logo 容器 */
    .logo-container {
        text-align: center;
        padding: 30px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.2);
    }
    .logo-container img {
        max-width: 180px;
        border-radius: 15px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        transition: transform 0.3s ease;
    }
    .logo-container img:hover {
        transform: scale(1.05);
    }
    
    /* 标题样式 */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    /* 标签页样式 */
    .tab-nav button {
        font-size: 15px;
        font-weight: 600;
        padding: 12px 20px;
        border-radius: 10px 10px 0 0;
        transition: all 0.3s ease;
    }
    .tab-nav button:hover {
        transform: translateY(-2px);
    }
    .tab-nav button[aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* 卡片样式 */
    .stat-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    /* 按钮样式 */
    .primary-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .primary-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* 输入框样式 */
    .input-box {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    .input-box:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* 聊天界面样式 */
    .chatbot-container {
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    /* Accordion 样式 */
    .accordion-header {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .accordion-header:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* 底部信息栏 */
    .footer-info {
        text-align: center;
        padding: 20px;
        background: #f8f9fa;
        border-radius: 10px;
        margin-top: 30px;
        color: #6c757d;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .gradio-container {
            padding: 10px;
        }
        .logo-container img {
            max-width: 120px;
        }
    }
    """
    
    # 创建主应用
    with gr.Blocks(
        title="Another Me - 世界上另一个我",
        theme=gr.themes.Soft(
            primary_hue="indigo",
            secondary_hue="purple",
            neutral_hue="slate",
            font=gr.themes.GoogleFont("Inter"),
        ).set(
            button_primary_background_fill="*primary_500",
            button_primary_background_fill_hover="*primary_600",
            button_primary_border_color="*primary_500",
        ),
        css=custom_css,
        analytics_enabled=False
    ) as app:
        
        # Logo 和标题
        logo_path = Path(__file__).parent.parent / "another me logo.jpg"
        if logo_path.exists():
            with gr.Row():
                with gr.Column(scale=1):
                    gr.HTML("")  # 占位
                with gr.Column(scale=2):
                    gr.Image(
                        str(logo_path),
                        label=None,
                        show_label=False,
                        container=False,
                        elem_classes=["logo-container"],
                        height=150
                    )
                with gr.Column(scale=1):
                    gr.HTML("")  # 占位
        
        gr.Markdown(
            """
            <div style="text-align: center;">
                <h1 class="main-title" style="font-size: 2.5em; margin-bottom: 10px;">🌟 Another Me - 世界上另一个我</h1>
                <p style="font-size: 1.2em; color: #666; margin-bottom: 5px;"><strong>AI 数字分身系统</strong></p>
                <p style="color: #888;">用你的知识和对话训练专属 AI，创造属于你的数字分身</p>
            </div>
            """
        )
        
        # 创建标签页
        with gr.Tabs(elem_classes=["tab-nav"]) as tabs:
            
            # MEM 对话（首页）
            with gr.TabItem("💬 对话", id=0):
                create_mem_tab()
            
            # 主页
            with gr.TabItem("🏠 主页", id=1):
                create_home_tab()
            
            # 配置
            with gr.TabItem("⚙️ 配置", id=2):
                create_config_tab()
            
            # RAG 知识库
            with gr.TabItem("📚 RAG 知识库", id=3):
                create_rag_tab()
            
            # 知识库管理
            with gr.TabItem("📂 知识库管理", id=4):
                create_knowledge_manager_tab()
            
            # 记忆管理
            with gr.TabItem("🧠 记忆管理", id=5):
                create_memory_manager_tab()
            
            # 分析报告
            with gr.TabItem("📊 分析报告", id=6):
                create_analysis_tab()
        
        # 底部信息
        gr.HTML(
            """
            <div class="footer-info">
                <p style="margin: 5px 0; font-size: 14px;">
                    <strong>Another Me v0.7.0</strong> | 
                    <a href="https://github.com" target="_blank" style="color: #667eea; text-decoration: none;">GitHub</a> | 
                    MIT License
                </p>
                <p style="margin: 5px 0; color: #999; font-size: 13px;">
                    Powered by <strong>Gradio 4.0</strong> & <strong>AME Engine</strong>
                </p>
            </div>
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
