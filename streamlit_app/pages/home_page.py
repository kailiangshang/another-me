"""
主页 - 概览和快速访问
"""

import streamlit as st
import sys
import os
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


def show():
    """显示主页"""
    
    st.title("🌟 Another Me")
    st.subheader("世界上另一个我")
    
    st.markdown("""
    欢迎使用 **Another Me** - 你的 AI 数字分身系统！
    
    通过先进的 RAG 技术和记忆模仿，创建一个真正理解你、能够代表你思考和表达的 AI 助手。
    """)
    
    st.markdown("---")
    
    # 快速开始指南
    st.markdown("## 🚀 快速开始")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📚 RAG 知识库")
        st.markdown("""
        1. 上传你的笔记、文档和资料
        2. AI 将学习并理解你的知识体系
        3. 随时检索和问答
        """)
        if st.button("🚀 开始上传知识", use_container_width=True):
            st.session_state.navigation = "📚 RAG 知识库"
            st.rerun()
    
    with col2:
        st.markdown("### 💬 MEM 记忆模仿")
        st.markdown("""
        1. 上传你的聊天记录和对话
        2. AI 学习你的说话风格和思维方式
        3. 让 AI 分身用你的方式说话
        """)
        if st.button("🚀 开始对话学习", use_container_width=True):
            st.session_state.navigation = "💬 MEM 对话"
            st.rerun()
    
    st.markdown("---")
    
    # 系统状态
    st.markdown("## 📊 系统状态")
    
    if st.session_state.get('is_configured', False):
        
        col1, col2, col3, col4 = st.columns(4)
        
        # RAG 统计
        if 'rag_kb' in st.session_state:
            stats = asyncio.run(st.session_state.rag_kb.get_statistics())
            with col1:
                st.metric("📚 知识库文档", stats.get('total_documents', 0))
            with col2:
                st.metric("🏷️ 知识来源", len(stats.get('sources', {})))
        else:
            with col1:
                st.metric("📚 知识库文档", 0)
            with col2:
                st.metric("🏷️ 知识来源", 0)
        
        # MEM 统计
        if 'mimic_engine' in st.session_state:
            mem_stats = asyncio.run(st.session_state.mimic_engine.vector_store.get_statistics())
            with col3:
                st.metric("💬 对话记忆", mem_stats.get('count', 0))
            with col4:
                st.metric("🧠 记忆来源", len(mem_stats.get('sources', {})))
        else:
            with col3:
                st.metric("💬 对话记忆", 0)
            with col4:
                st.metric("🧠 记忆来源", 0)
        
        st.markdown("---")
        
        # 快速访问
        st.markdown("## ⚡ 快速访问")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📂 知识库管理", use_container_width=True, type="primary"):
                st.session_state.navigation = "📂 知识库管理"
                st.rerun()
        
        with col2:
            if st.button("🧠 记忆管理", use_container_width=True, type="primary"):
                st.session_state.navigation = "🧠 记忆管理"
                st.rerun()
        
        with col3:
            if st.button("📊 分析报告", use_container_width=True, type="primary"):
                st.session_state.navigation = "📊 分析报告"
                st.rerun()
        
        with col4:
            if st.button("⚙️ 系统配置", use_container_width=True):
                st.session_state.navigation = "⚙️ 配置"
                st.rerun()
        
    else:
        st.warning("⚠️ 请先完成系统配置")
        if st.button("前往配置", type="primary"):
            st.session_state.navigation = "⚙️ 配置"
            st.rerun()
    
    st.markdown("---")
    
    # 功能介绍
    st.markdown("## 💡 核心功能")
    
    tab1, tab2, tab3 = st.tabs(["📚 知识管理", "💬 对话模仿", "📊 智能分析"])
    
    with tab1:
        st.markdown("""
        ### RAG 知识库系统
        
        - **文档上传**: 支持 TXT, MD, PDF, DOCX, JSON 等格式
        - **向量检索**: 高效的语义搜索和相关度排序
        - **混合检索**: 结合向量、关键词和时间权重
        - **来源管理**: 按来源分类和筛选知识
        - **统计分析**: 可视化知识库分布和增长趋势
        
        💡 让 AI 深入理解你的知识体系，成为你的第二大脑。
        """)
    
    with tab2:
        st.markdown("""
        ### MEM 记忆模仿引擎
        
        - **对话学习**: 从聊天记录中学习你的表达习惯
        - **风格模仿**: 复现你的语气、用词和思维方式
        - **流式对话**: 实时生成，自然流畅
        - **记忆管理**: 查看和管理所有学习记录
        - **时间线视图**: 按时间浏览对话历史
        
        💡 创建一个真正"像你"的 AI 分身。
        """)
    
    with tab3:
        st.markdown("""
        ### 智能分析报告
        
        - **个性分析**: 基于对话和知识的个性洞察
        - **知识图谱**: 可视化你的知识结构
        - **对话模式**: 分析你的表达特点和习惯
        - **多格式导出**: Markdown, PDF, HTML
        - **定制报告**: 按需生成专题分析
        
        💡 深入了解自己，发现更多可能。
        """)
    
    st.markdown("---")
    
    # 底部信息
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📖 技术栈**")
        st.markdown("""
        - Streamlit 前端
        - FastAPI 后端
        - AME 技术引擎
        - Memu 向量库
        """)
    
    with col2:
        st.markdown("**🔗 相关链接**")
        st.markdown("""
        - [GitHub 仓库](#)
        - [使用文档](#)
        - [问题反馈](#)
        """)
    
    with col3:
        st.markdown("**ℹ️ 版本信息**")
        st.markdown("""
        - 版本: v0.5.0
        - 更新: 2025-10-22
        - 许可: MIT License
        """)
