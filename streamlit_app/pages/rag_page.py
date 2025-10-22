"""
RAG 知识库页面
"""

import streamlit as st
import sys
import os
import asyncio
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from ame.rag.knowledge_base import KnowledgeBase


def show():
    """显示 RAG 知识库页面"""
    
    st.title("📚 RAG 知识库")
    
    st.markdown("""
    上传个人笔记、文档、资料，构建专属知识库。支持问答检索和知识管理。
    """)
    
    if not st.session_state.is_configured:
        st.warning("⚠️ 请先在配置页面设置 API Key")
        return
    
    # 创建知识库实例
    if 'rag_kb' not in st.session_state:
        st.session_state.rag_kb = KnowledgeBase()
    
    kb = st.session_state.rag_kb
    
    # 快速统计卡片
    stats = asyncio.run(kb.get_statistics())
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📚 总文档数", stats.get('total_documents', 0))
    
    with col2:
        st.metric("🏷️ 来源类型", len(stats.get('sources', {})))
    
    with col3:
        st.metric("📅 最后更新", stats.get('last_updated', 'N/A')[:10])
    
    with col4:
        if st.button("📂 管理知识库", use_container_width=True):
            st.session_state.navigation = "📂 知识库管理"
            st.rerun()
    
    st.markdown("---")
    
    # 标签页
    tab1, tab2, tab3 = st.tabs(["📤 上传文档", "🔍 知识检索", "📊 知识库统计"])
    
    with tab1:
        show_upload_tab(kb)
    
    with tab2:
        show_search_tab(kb)
    
    with tab3:
        show_stats_tab(kb)


def show_upload_tab(kb):
    """上传文档标签页"""
    
    st.subheader("📤 上传文档")
    
    # 文件上传
    uploaded_files = st.file_uploader(
        "选择文件",
        type=['txt', 'md', 'pdf', 'docx', 'json'],
        accept_multiple_files=True,
        help="支持文本、Markdown、PDF、Word 文档"
    )
    
    # 文本输入
    st.markdown("**或者直接输入文本**")
    text_input = st.text_area(
        "输入文本内容",
        height=150,
        placeholder="输入笔记、想法、知识点..."
    )
    
    text_source = st.text_input(
        "来源标签",
        value="manual_input",
        help="标记这段文本的来源"
    )
    
    col1, col2 = st.columns([1, 5])
    
    with col1:
        if st.button("💾 保存文本", type="primary"):
            if text_input.strip():
                with st.spinner("保存中..."):
                    result = asyncio.run(kb.add_text(
                        text=text_input,
                        source=text_source
                    ))
                    if result['success']:
                        st.success("✅ 文本已保存到知识库！")
                        st.rerun()
            else:
                st.error("请输入文本内容")
    
    with col2:
        if st.button("📁 上传文件"):
            if uploaded_files:
                upload_dir = Path("./data/rag_uploads")
                upload_dir.mkdir(parents=True, exist_ok=True)
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for idx, uploaded_file in enumerate(uploaded_files):
                    # 保存文件
                    file_path = upload_dir / uploaded_file.name
                    with open(file_path, 'wb') as f:
                        f.write(uploaded_file.getbuffer())
                    
                    status_text.text(f"处理中: {uploaded_file.name}")
                    
                    # 添加到知识库
                    result = asyncio.run(kb.add_document(str(file_path)))
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                status_text.empty()
                progress_bar.empty()
                st.success(f"✅ 已成功上传 {len(uploaded_files)} 个文件！")
                st.rerun()
            else:
                st.error("请选择要上传的文件")


def show_search_tab(kb):
    """知识检索标签页"""
    
    st.subheader("🔍 知识检索")
    
    query = st.text_input(
        "输入查询",
        placeholder="搜索知识库中的内容...",
        key="rag_search_query"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        top_k = st.slider("返回结果数量", min_value=1, max_value=20, value=5)
    
    with col2:
        if st.button("🔍 搜索", type="primary"):
            if query.strip():
                with st.spinner("检索中..."):
                    results = asyncio.run(kb.search(query=query, top_k=top_k))
                    
                    if results:
                        st.success(f"找到 {len(results)} 条相关结果")
                        
                        for idx, result in enumerate(results, 1):
                            with st.expander(f"结果 {idx} - 相关度: {result['score']:.2%}"):
                                st.markdown(f"**内容**: {result['content'][:200]}...")
                                st.markdown(f"**来源**: {result.get('source', 'unknown')}")
                                
                                metadata = result.get('metadata', {})
                                if metadata:
                                    st.json(metadata)
                    else:
                        st.info("未找到相关结果")
            else:
                st.error("请输入查询内容")


def show_stats_tab(kb):
    """知识库统计标签页"""
    
    st.subheader("📊 知识库统计")
    
    if st.button("🔄 刷新统计"):
        st.rerun()
    
    stats = asyncio.run(kb.get_statistics())
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("总文档数", stats.get('total_documents', 0))
    
    with col2:
        st.metric("最后更新", stats.get('last_updated', 'N/A'))
    
    with col3:
        sources = stats.get('sources', {})
        st.metric("来源类型", len(sources))
    
    if sources:
        st.markdown("### 来源分布")
        st.bar_chart(sources)
