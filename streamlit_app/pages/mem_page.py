"""
MEM 对话页面 - 模仿用户说话风格
"""

import streamlit as st
import sys
import os
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from ame.mem.mimic_engine import MimicEngine
from ame.llm_caller.caller import LLMCaller


def show():
    """显示 MEM 对话页面"""
    
    st.title("💬 MEM 对话")
    
    st.markdown("""
    与 AI 分身对话，它会模仿你的说话风格。上传聊天记录让它学习，对话会被记录以持续改进。
    """)
    
    if not st.session_state.is_configured:
        st.warning("⚠️ 请先在配置页面设置 API Key")
        return
    
    # 创建模仿引擎
    if 'mimic_engine' not in st.session_state:
        llm_caller = LLMCaller(
            api_key=st.session_state.api_key,
            base_url=st.session_state.api_base_url,
            model=st.session_state.model
        )
        st.session_state.mimic_engine = MimicEngine(llm_caller=llm_caller)
    
    engine = st.session_state.mimic_engine
    
    # 快速统计卡片
    stats = asyncio.run(engine.vector_store.get_statistics())
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💬 总记忆数", stats.get('count', 0))
    
    with col2:
        st.metric("🏷️ 来源类型", len(stats.get('sources', {})))
    
    with col3:
        chat_count = len(st.session_state.get('mem_chat_history', []))
        st.metric("📝 当前对话", f"{chat_count} 条")
    
    with col4:
        if st.button("🧠 管理记忆", use_container_width=True):
            st.session_state.navigation = "🧠 记忆管理"
            st.rerun()
    
    st.markdown("---")
    
    # 标签页
    tab1, tab2 = st.tabs(["💬 对话", "📚 学习材料"])
    
    with tab1:
        show_chat_tab(engine)
    
    with tab2:
        show_learning_tab(engine)


def show_chat_tab(engine):
    """对话标签页"""
    
    st.subheader("💬 与 AI 分身对话")
    
    # 显示对话历史
    if 'mem_chat_history' not in st.session_state:
        st.session_state.mem_chat_history = []
    
    # 聊天容器
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.mem_chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # 输入框
    user_input = st.chat_input("输入消息...")
    
    if user_input:
        # 添加用户消息到历史
        st.session_state.mem_chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # 显示用户消息
        with chat_container:
            with st.chat_message("user"):
                st.markdown(user_input)
        
        # 生成回复（流式）
        with chat_container:
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # 流式生成
                async def generate_stream():
                    nonlocal full_response
                    async for chunk in engine.generate_response_stream(
                        prompt=user_input,
                        temperature=0.8,
                        use_history=True
                    ):
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                    
                    message_placeholder.markdown(full_response)
                    return full_response
                
                # 运行异步生成
                response = asyncio.run(generate_stream())
        
        # 添加助手消息到历史
        st.session_state.mem_chat_history.append({
            "role": "assistant",
            "content": response
        })
        
        # 学习这次对话
        asyncio.run(engine.learn_from_conversation(
            user_message=user_input,
            context=response
        ))
        
        st.rerun()
    
    # 清空对话历史按钮
    if st.button("🗑️ 清空对话"):
        st.session_state.mem_chat_history = []
        st.rerun()


def show_learning_tab(engine):
    """学习材料标签页"""
    
    st.subheader("📚 上传聊天记录")
    
    st.markdown("""
    上传你的聊天记录文本文件，让 AI 学习你的说话风格。
    支持格式：
    - 纯文本（每行一条消息）
    - JSON 格式的聊天记录
    """)
    
    uploaded_file = st.file_uploader(
        "选择聊天记录文件",
        type=['txt', 'json'],
        help="上传聊天记录文本文件"
    )
    
    if uploaded_file:
        content = uploaded_file.read().decode('utf-8')
        
        st.text_area(
            "预览内容",
            value=content[:500] + "..." if len(content) > 500 else content,
            height=200,
            disabled=True
        )
        
        if st.button("📚 开始学习", type="primary"):
            with st.spinner("学习中..."):
                # 简单处理：按行分割
                lines = content.split('\n')
                messages = [line.strip() for line in lines if line.strip()]
                
                progress_bar = st.progress(0)
                
                for idx, msg in enumerate(messages):
                    asyncio.run(engine.learn_from_conversation(
                        user_message=msg,
                        metadata={"source": "uploaded_chat"}
                    ))
                    progress_bar.progress((idx + 1) / len(messages))
                
                progress_bar.empty()
                st.success(f"✅ 已学习 {len(messages)} 条消息！")
    
    st.markdown("---")
    
    # 手动输入学习材料
    st.subheader("✍️ 手动输入")
    
    manual_text = st.text_area(
        "输入一段你说过的话",
        height=150,
        placeholder="输入你的聊天记录、日记、想法..."
    )
    
    if st.button("💾 保存并学习"):
        if manual_text.strip():
            asyncio.run(engine.learn_from_conversation(
                user_message=manual_text,
                metadata={"source": "manual_input"}
            ))
            st.success("✅ 已学习！")
        else:
            st.error("请输入内容")
