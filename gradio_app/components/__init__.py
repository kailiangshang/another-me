"""
组件模块初始化
"""

from .home_tab import create_home_tab
from .config_tab import create_config_tab
from .mem_tab import create_mem_tab

# 简化版本的其他tab（可后续扩展）
def create_rag_tab():
    import gradio as gr
    gr.Markdown("## 📚 RAG 知识库\n\n功能开发中...")

def create_knowledge_manager_tab():
    import gradio as gr
    gr.Markdown("## 📂 知识库管理\n\n功能开发中...")

def create_memory_manager_tab():
    import gradio as gr
    gr.Markdown("## 🧠 记忆管理\n\n功能开发中...")

def create_analysis_tab():
    import gradio as gr
    gr.Markdown("## 📊 分析报告\n\n功能开发中...")

__all__ = [
    'create_home_tab',
    'create_config_tab',
    'create_rag_tab',
    'create_mem_tab',
    'create_knowledge_manager_tab',
    'create_memory_manager_tab',
    'create_analysis_tab'
]
