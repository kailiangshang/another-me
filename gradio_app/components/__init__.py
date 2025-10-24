"""
组件模块初始化
"""

from .home_tab import create_home_tab
from .config_tab import create_config_tab
from .mem_tab import create_mem_tab

# 简化版本的其他tab（可后续扩展）
def create_rag_tab():
    import gradio as gr
    gr.HTML(
        """
        <div style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 5em; margin-bottom: 20px;">📚</div>
            <h2 style="color: #667eea; margin-bottom: 15px;">RAG 知识库</h2>
            <p style="color: #888; font-size: 1.1em;">功能开发中...</p>
            <p style="color: #aaa; margin-top: 10px;">敬请期待下个版本更新</p>
        </div>
        """
    )

def create_knowledge_manager_tab():
    import gradio as gr
    gr.HTML(
        """
        <div style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 5em; margin-bottom: 20px;">📂</div>
            <h2 style="color: #667eea; margin-bottom: 15px;">知识库管理</h2>
            <p style="color: #888; font-size: 1.1em;">功能开发中...</p>
            <p style="color: #aaa; margin-top: 10px;">敬请期待下个版本更新</p>
        </div>
        """
    )

def create_memory_manager_tab():
    import gradio as gr
    gr.HTML(
        """
        <div style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 5em; margin-bottom: 20px;">🧠</div>
            <h2 style="color: #667eea; margin-bottom: 15px;">记忆管理</h2>
            <p style="color: #888; font-size: 1.1em;">功能开发中...</p>
            <p style="color: #aaa; margin-top: 10px;">敬请期待下个版本更新</p>
        </div>
        """
    )

def create_analysis_tab():
    import gradio as gr
    gr.HTML(
        """
        <div style="text-align: center; padding: 60px 20px;">
            <div style="font-size: 5em; margin-bottom: 20px;">📊</div>
            <h2 style="color: #667eea; margin-bottom: 15px;">分析报告</h2>
            <p style="color: #888; font-size: 1.1em;">功能开发中...</p>
            <p style="color: #aaa; margin-top: 10px;">敬请期待下个版本更新</p>
        </div>
        """
    )

__all__ = [
    'create_home_tab',
    'create_config_tab',
    'create_rag_tab',
    'create_mem_tab',
    'create_knowledge_manager_tab',
    'create_memory_manager_tab',
    'create_analysis_tab'
]
