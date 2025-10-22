"""
知识库管理页面 - 查看和管理已上传的知识
"""

import streamlit as st
import sys
import os
import asyncio
from datetime import datetime
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


def show():
    """显示知识库管理页面"""
    
    st.title("📂 知识库管理")
    
    st.markdown("""
    查看、搜索和管理你上传的所有知识库内容。
    """)
    
    if not st.session_state.is_configured:
        st.warning("⚠️ 请先在配置页面设置 API Key")
        return
    
    # 确保知识库已初始化
    if 'rag_kb' not in st.session_state:
        from ame.rag.knowledge_base import KnowledgeBase
        st.session_state.rag_kb = KnowledgeBase()
    
    kb = st.session_state.rag_kb
    
    st.markdown("---")
    
    # 标签页
    tab1, tab2, tab3 = st.tabs(["📚 所有知识", "🔍 按来源筛选", "📊 统计分析"])
    
    with tab1:
        show_all_documents(kb)
    
    with tab2:
        show_by_source(kb)
    
    with tab3:
        show_analytics(kb)


def show_all_documents(kb):
    """显示所有文档"""
    
    st.subheader("📚 所有知识库内容")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        search_query = st.text_input(
            "搜索内容",
            placeholder="输入关键词搜索...",
            key="km_search"
        )
    
    with col2:
        sort_by = st.selectbox(
            "排序方式",
            ["最新", "最旧", "来源"],
            key="km_sort"
        )
    
    with col3:
        if st.button("🔄 刷新", use_container_width=True):
            st.rerun()
    
    # 获取所有文档
    with st.spinner("加载中..."):
        all_docs = asyncio.run(kb.vector_store.get_all_documents())
    
    if not all_docs:
        st.info("知识库为空，请先上传一些内容")
        return
    
    # 搜索过滤
    if search_query:
        all_docs = [
            doc for doc in all_docs
            if search_query.lower() in doc.get('content', '').lower()
        ]
    
    # 排序
    if sort_by == "最新":
        all_docs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    elif sort_by == "最旧":
        all_docs.sort(key=lambda x: x.get('timestamp', ''))
    elif sort_by == "来源":
        all_docs.sort(key=lambda x: x.get('source', ''))
    
    # 显示统计
    st.info(f"共找到 **{len(all_docs)}** 条知识")
    
    # 分页
    items_per_page = 10
    total_pages = (len(all_docs) - 1) // items_per_page + 1
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    
    # 分页控制
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        page_num = st.selectbox(
            "页码",
            range(total_pages),
            index=st.session_state.current_page,
            format_func=lambda x: f"第 {x+1} 页 / 共 {total_pages} 页"
        )
        st.session_state.current_page = page_num
    
    # 显示当前页的文档
    start_idx = page_num * items_per_page
    end_idx = min(start_idx + items_per_page, len(all_docs))
    
    for idx, doc in enumerate(all_docs[start_idx:end_idx], start=start_idx + 1):
        with st.expander(
            f"📄 #{idx} - {doc.get('source', 'unknown')} - {doc.get('timestamp', 'N/A')[:10]}"
        ):
            # 内容
            st.markdown("**内容**:")
            st.text_area(
                "content",
                value=doc.get('content', ''),
                height=150,
                disabled=True,
                key=f"doc_content_{idx}",
                label_visibility="collapsed"
            )
            
            # 元数据
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**来源**: {doc.get('source', 'unknown')}")
                st.markdown(f"**时间**: {doc.get('timestamp', 'N/A')}")
            
            with col2:
                metadata = doc.get('metadata', {})
                if metadata:
                    st.markdown("**元数据**:")
                    st.json(metadata, expanded=False)
            
            # 操作按钮
            if st.button(f"🗑️ 删除", key=f"delete_{idx}"):
                if doc.get('id'):
                    asyncio.run(kb.vector_store.delete_documents([doc['id']]))
                    st.success("已删除")
                    st.rerun()


def show_by_source(kb):
    """按来源筛选"""
    
    st.subheader("🔍 按来源筛选")
    
    # 获取统计信息
    stats = asyncio.run(kb.get_statistics())
    sources = stats.get('sources', {})
    
    if not sources:
        st.info("暂无数据")
        return
    
    # 来源选择
    selected_source = st.selectbox(
        "选择来源",
        list(sources.keys()),
        format_func=lambda x: f"{x} ({sources[x]} 条)"
    )
    
    if selected_source:
        # 获取该来源的所有文档
        all_docs = asyncio.run(kb.vector_store.get_all_documents())
        filtered_docs = [
            doc for doc in all_docs
            if doc.get('source') == selected_source
        ]
        
        st.info(f"来源 **{selected_source}** 共有 **{len(filtered_docs)}** 条知识")
        
        # 显示文档
        for idx, doc in enumerate(filtered_docs, 1):
            with st.expander(f"📄 {idx}. {doc.get('timestamp', 'N/A')[:10]}"):
                st.text_area(
                    "content",
                    value=doc.get('content', ''),
                    height=100,
                    disabled=True,
                    key=f"src_doc_{idx}",
                    label_visibility="collapsed"
                )


def show_analytics(kb):
    """统计分析"""
    
    st.subheader("📊 知识库统计分析")
    
    stats = asyncio.run(kb.get_statistics())
    
    # 总体统计
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("总文档数", stats.get('total_documents', 0))
    
    with col2:
        st.metric("来源类型", len(stats.get('sources', {})))
    
    with col3:
        st.metric("最后更新", stats.get('last_updated', 'N/A')[:10])
    
    st.markdown("---")
    
    # 来源分布
    sources = stats.get('sources', {})
    if sources:
        st.markdown("### 📈 来源分布")
        
        # 转换为 DataFrame
        df = pd.DataFrame(
            list(sources.items()),
            columns=['来源', '数量']
        )
        df = df.sort_values('数量', ascending=False)
        
        # 柱状图
        st.bar_chart(df.set_index('来源'))
        
        # 详细表格
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    
    st.markdown("---")
    
    # 时间分布
    st.markdown("### 📅 时间分布")
    
    all_docs = asyncio.run(kb.vector_store.get_all_documents())
    
    if all_docs:
        # 提取日期
        dates = []
        for doc in all_docs:
            timestamp = doc.get('timestamp', '')
            if timestamp:
                try:
                    date = datetime.fromisoformat(timestamp).date()
                    dates.append(date)
                except:
                    pass
        
        if dates:
            df_dates = pd.DataFrame({'日期': dates})
            df_dates['数量'] = 1
            df_dates = df_dates.groupby('日期').count().reset_index()
            df_dates = df_dates.sort_values('日期')
            
            st.line_chart(df_dates.set_index('日期'))
        else:
            st.info("暂无时间数据")
    
    st.markdown("---")
    
    # 危险操作
    st.markdown("### ⚠️ 危险操作")
    
    if st.button("🗑️ 清空整个知识库", type="secondary"):
        if st.checkbox("我确认要清空所有知识库数据"):
            asyncio.run(kb.vector_store.clear())
            st.success("知识库已清空")
            st.rerun()
