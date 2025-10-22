"""
记忆管理页面 - 查看和管理 MEM 学习的历史记录
"""

import streamlit as st
import sys
import os
import asyncio
from datetime import datetime, timedelta
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


def show():
    """显示记忆管理页面"""
    
    st.title("🧠 记忆管理")
    
    st.markdown("""
    查看和管理 AI 分身学习的所有对话记忆和交互历史。
    """)
    
    if not st.session_state.is_configured:
        st.warning("⚠️ 请先在配置页面设置 API Key")
        return
    
    # 确保引擎已初始化
    if 'mimic_engine' not in st.session_state:
        from ame.mem.mimic_engine import MimicEngine
        from ame.llm_caller.caller import LLMCaller
        
        llm_caller = LLMCaller(
            api_key=st.session_state.api_key,
            base_url=st.session_state.api_base_url,
            model=st.session_state.model
        )
        st.session_state.mimic_engine = MimicEngine(llm_caller=llm_caller)
    
    engine = st.session_state.mimic_engine
    
    st.markdown("---")
    
    # 标签页
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 所有记忆",
        "📅 时间线",
        "🏷️ 按来源查看",
        "📊 统计分析"
    ])
    
    with tab1:
        show_all_memories(engine)
    
    with tab2:
        show_timeline(engine)
    
    with tab3:
        show_by_source(engine)
    
    with tab4:
        show_analytics(engine)


def show_all_memories(engine):
    """显示所有记忆"""
    
    st.subheader("💬 所有对话记忆")
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        search_query = st.text_input(
            "搜索记忆",
            placeholder="输入关键词...",
            key="mem_search"
        )
    
    with col2:
        sort_by = st.selectbox(
            "排序",
            ["最新", "最旧"],
            key="mem_sort"
        )
    
    with col3:
        if st.button("🔄 刷新", use_container_width=True):
            st.rerun()
    
    # 获取所有记忆
    with st.spinner("加载记忆中..."):
        all_memories = asyncio.run(engine.vector_store.get_all_documents())
    
    if not all_memories:
        st.info("暂无记忆数据，开始与 AI 分身对话或上传聊天记录吧！")
        return
    
    # 搜索过滤
    if search_query:
        all_memories = [
            mem for mem in all_memories
            if search_query.lower() in mem.get('content', '').lower()
        ]
    
    # 排序
    if sort_by == "最新":
        all_memories.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    else:
        all_memories.sort(key=lambda x: x.get('timestamp', ''))
    
    # 显示统计
    st.info(f"共有 **{len(all_memories)}** 条记忆")
    
    # 分页
    items_per_page = 15
    total_pages = (len(all_memories) - 1) // items_per_page + 1
    
    if 'mem_current_page' not in st.session_state:
        st.session_state.mem_current_page = 0
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        page_num = st.selectbox(
            "页码",
            range(total_pages),
            index=st.session_state.mem_current_page,
            format_func=lambda x: f"第 {x+1} 页 / 共 {total_pages} 页",
            key="mem_page_select"
        )
        st.session_state.mem_current_page = page_num
    
    # 显示当前页
    start_idx = page_num * items_per_page
    end_idx = min(start_idx + items_per_page, len(all_memories))
    
    for idx, mem in enumerate(all_memories[start_idx:end_idx], start=start_idx + 1):
        timestamp = mem.get('timestamp', 'N/A')
        try:
            dt = datetime.fromisoformat(timestamp)
            time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            time_str = timestamp
        
        with st.expander(f"💭 #{idx} - {time_str}"):
            # 内容
            st.markdown("**对话内容**:")
            st.text_area(
                "memory_content",
                value=mem.get('content', ''),
                height=120,
                disabled=True,
                key=f"mem_{idx}",
                label_visibility="collapsed"
            )
            
            # 元数据
            metadata = mem.get('metadata', {})
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**来源**: {mem.get('source', 'unknown')}")
                context = metadata.get('context', '')
                if context:
                    st.markdown("**上下文**:")
                    st.caption(context[:100] + "..." if len(context) > 100 else context)
            
            with col2:
                if metadata:
                    st.markdown("**完整元数据**:")
                    st.json(metadata, expanded=False)
            
            # 操作
            if st.button(f"🗑️ 删除此记忆", key=f"del_mem_{idx}"):
                if mem.get('id'):
                    asyncio.run(engine.vector_store.delete_documents([mem['id']]))
                    st.success("已删除")
                    st.rerun()


def show_timeline(engine):
    """时间线视图"""
    
    st.subheader("📅 记忆时间线")
    
    # 日期范围选择
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input(
            "开始日期",
            value=datetime.now().date() - timedelta(days=30),
            key="timeline_start"
        )
    
    with col2:
        end_date = st.date_input(
            "结束日期",
            value=datetime.now().date(),
            key="timeline_end"
        )
    
    # 获取时间范围内的记忆
    start_datetime = datetime.combine(start_date, datetime.min.time()).isoformat()
    end_datetime = datetime.combine(end_date, datetime.max.time()).isoformat()
    
    memories = asyncio.run(
        engine.vector_store.get_documents_by_date_range(
            start_date=start_datetime,
            end_date=end_datetime
        )
    )
    
    if not memories:
        st.info("该时间段内没有记忆")
        return
    
    st.info(f"找到 **{len(memories)}** 条记忆")
    
    # 按日期分组
    memories_by_date = {}
    for mem in memories:
        timestamp = mem.get('timestamp', '')
        try:
            dt = datetime.fromisoformat(timestamp)
            date_key = dt.date()
            if date_key not in memories_by_date:
                memories_by_date[date_key] = []
            memories_by_date[date_key].append(mem)
        except:
            pass
    
    # 按日期显示
    for date in sorted(memories_by_date.keys(), reverse=True):
        st.markdown(f"### 📆 {date}")
        
        for idx, mem in enumerate(memories_by_date[date], 1):
            timestamp = mem.get('timestamp', '')
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%H:%M:%S")
            except:
                time_str = "未知时间"
            
            with st.expander(f"⏰ {time_str} - {mem.get('content', '')[:50]}..."):
                st.text_area(
                    "content",
                    value=mem.get('content', ''),
                    height=100,
                    disabled=True,
                    key=f"timeline_{date}_{idx}",
                    label_visibility="collapsed"
                )
        
        st.markdown("---")


def show_by_source(engine):
    """按来源查看"""
    
    st.subheader("🏷️ 按来源查看")
    
    # 获取统计
    stats = asyncio.run(engine.vector_store.get_statistics())
    sources = stats.get('sources', {})
    
    if not sources:
        st.info("暂无数据")
        return
    
    # 来源选择
    selected_source = st.selectbox(
        "选择来源",
        list(sources.keys()),
        format_func=lambda x: f"{x} ({sources[x]} 条)",
        key="mem_source_select"
    )
    
    if selected_source:
        all_memories = asyncio.run(engine.vector_store.get_all_documents())
        filtered = [
            mem for mem in all_memories
            if mem.get('source') == selected_source
        ]
        
        # 按时间排序
        filtered.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        st.info(f"来源 **{selected_source}** 共有 **{len(filtered)}** 条记忆")
        
        for idx, mem in enumerate(filtered, 1):
            timestamp = mem.get('timestamp', 'N/A')
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime("%Y-%m-%d %H:%M")
            except:
                time_str = timestamp[:16]
            
            with st.expander(f"{idx}. {time_str}"):
                st.text_area(
                    "content",
                    value=mem.get('content', ''),
                    height=100,
                    disabled=True,
                    key=f"src_mem_{idx}",
                    label_visibility="collapsed"
                )


def show_analytics(engine):
    """统计分析"""
    
    st.subheader("📊 记忆统计分析")
    
    stats = asyncio.run(engine.vector_store.get_statistics())
    
    # 总体统计
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("总记忆数", stats.get('count', 0))
    
    with col2:
        st.metric("来源类型", len(stats.get('sources', {})))
    
    with col3:
        st.metric("最后更新", stats.get('last_updated', 'N/A')[:10])
    
    st.markdown("---")
    
    # 来源分布
    sources = stats.get('sources', {})
    if sources:
        st.markdown("### 📈 来源分布")
        
        df = pd.DataFrame(
            list(sources.items()),
            columns=['来源', '数量']
        )
        df = df.sort_values('数量', ascending=False)
        
        st.bar_chart(df.set_index('来源'))
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    
    st.markdown("---")
    
    # 时间分布
    st.markdown("### 📅 记忆时间分布")
    
    all_memories = asyncio.run(engine.vector_store.get_all_documents())
    
    if all_memories:
        dates = []
        for mem in all_memories:
            timestamp = mem.get('timestamp', '')
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
            
            # 最活跃的日期
            most_active = df_dates.nlargest(5, '数量')
            st.markdown("### 🔥 最活跃的日期")
            st.dataframe(
                most_active,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("暂无时间数据")
    
    st.markdown("---")
    
    # 导出功能
    st.markdown("### 📥 导出记忆")
    
    if st.button("📦 导出为 JSON"):
        import json
        
        all_memories = asyncio.run(engine.vector_store.get_all_documents())
        
        export_data = {
            "export_date": datetime.now().isoformat(),
            "total_memories": len(all_memories),
            "memories": all_memories
        }
        
        json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
        
        st.download_button(
            label="⬇️ 下载 JSON 文件",
            data=json_str,
            file_name=f"memories_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    st.markdown("---")
    
    # 危险操作
    st.markdown("### ⚠️ 危险操作")
    
    if st.button("🗑️ 清空所有记忆", type="secondary"):
        if st.checkbox("我确认要清空所有记忆数据", key="confirm_clear_mem"):
            asyncio.run(engine.vector_store.clear())
            st.success("所有记忆已清空")
            st.rerun()
