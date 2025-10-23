"""
主页组件
"""

import gradio as gr
import sys
import os
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.session import get_session_state


def get_system_stats():
    """获取系统统计信息"""
    state = get_session_state()
    
    rag_docs = 0
    rag_sources = 0
    mem_count = 0
    mem_sources = 0
    
    try:
        if state.get('rag_kb'):
            stats = asyncio.run(state['rag_kb'].get_statistics())
            rag_docs = stats.get('total_documents', 0)
            rag_sources = len(stats.get('sources', {}))
    except:
        pass
    
    try:
        if state.get('mimic_engine'):
            stats = asyncio.run(state['mimic_engine'].vector_store.get_statistics())
            mem_count = stats.get('count', 0)
            mem_sources = len(stats.get('sources', {}))
    except:
        pass
    
    return rag_docs, rag_sources, mem_count, mem_sources


def create_home_tab():
    """创建主页"""
    
    state = get_session_state()
    
    gr.Markdown(
        """
        ## 🏠 欢迎使用 Another Me
        
        **世界上另一个我** - 你的 AI 数字分身系统
        
        通过先进的 RAG 技术和记忆模仿，创建一个真正理解你、能够代表你思考和表达的 AI 助手。
        """
    )
    
    # 系统状态
    if state.get('is_configured'):
        gr.Markdown("### 📊 系统状态")
        
        with gr.Row():
            rag_docs_num = gr.Number(label="📚 知识库文档", value=0, interactive=False)
            rag_sources_num = gr.Number(label="🏷️ 知识来源", value=0, interactive=False)
            mem_count_num = gr.Number(label="💬 对话记忆", value=0, interactive=False)
            mem_sources_num = gr.Number(label="🧠 记忆来源", value=0, interactive=False)
        
        refresh_btn = gr.Button("🔄 刷新统计", size="sm")
        
        refresh_btn.click(
            fn=get_system_stats,
            outputs=[rag_docs_num, rag_sources_num, mem_count_num, mem_sources_num]
        )
    else:
        gr.Warning("⚠️ 请先在配置页面设置 API Key")
    
    gr.Markdown("---")
    
    # 快速开始
    gr.Markdown("## 🚀 快速开始")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown(
                """
                ### 📚 RAG 知识库
                
                1. 上传你的笔记、文档和资料
                2. AI 将学习并理解你的知识体系
                3. 随时检索和问答
                
                **支持格式**: TXT, MD, PDF, DOCX, JSON
                """
            )
            gr.Button("🚀 开始上传知识", link="/", size="sm")
        
        with gr.Column():
            gr.Markdown(
                """
                ### 💬 MEM 记忆模仿
                
                1. 上传你的聊天记录和对话
                2. AI 学习你的说话风格和思维方式
                3. 让 AI 分身用你的方式说话
                
                **特点**: 实时流式对话，自然流畅
                """
            )
            gr.Button("🚀 开始对话学习", link="/", size="sm")
    
    gr.Markdown("---")
    
    # 核心功能介绍
    gr.Markdown("## 💡 核心功能")
    
    with gr.Accordion("📚 知识管理", open=False):
        gr.Markdown(
            """
            - **文档上传**: 支持 TXT, MD, PDF, DOCX, JSON 等格式
            - **向量检索**: 高效的语义搜索和相关度排序
            - **混合检索**: 结合向量、关键词和时间权重
            - **来源管理**: 按来源分类和筛选知识
            - **统计分析**: 可视化知识库分布和增长趋势
            """
        )
    
    with gr.Accordion("💬 对话模仿", open=False):
        gr.Markdown(
            """
            - **对话学习**: 从聊天记录中学习你的表达习惯
            - **风格模仿**: 复现你的语气、用词和思维方式
            - **流式对话**: 实时生成，自然流畅
            - **记忆管理**: 查看和管理所有学习记录
            - **时间线视图**: 按时间浏览对话历史
            """
        )
    
    with gr.Accordion("📊 智能分析", open=False):
        gr.Markdown(
            """
            - **个性分析**: 基于对话和知识的个性洞察
            - **知识图谱**: 可视化你的知识结构
            - **对话模式**: 分析你的表达特点和习惯
            - **多格式导出**: Markdown, HTML
            """
        )
    
    gr.Markdown("---")
    
    # 技术栈信息
    with gr.Row():
        with gr.Column():
            gr.Markdown(
                """
                **📖 技术栈**
                - Gradio 前端
                - AME 技术引擎
                - Memu 向量库
                - 流式输出支持
                """
            )
        
        with gr.Column():
            gr.Markdown(
                """
                **ℹ️ 版本信息**
                - 版本: v0.7.0
                - 更新: 2025-10-23
                - 许可: MIT License
                - 前端: Gradio
                """
            )
