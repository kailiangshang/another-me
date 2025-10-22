"""
配置页面
"""

import streamlit as st
from utils.session import save_config


def show():
    """显示配置页面"""
    
    st.title("⚙️ 系统配置")
    
    st.markdown("""
    配置 OpenAI 兼容的 API 以开始使用。支持 OpenAI、Azure OpenAI、本地模型（Ollama）等。
    """)
    
    st.markdown("---")
    
    # API Key 配置
    st.subheader("🔑 API 配置")
    
    api_key = st.text_input(
        "API Key",
        value=st.session_state.get('api_key', ''),
        type="password",
        help="OpenAI API Key 或兼容格式的 API Key"
    )
    
    api_base_url = st.text_input(
        "API Base URL",
        value=st.session_state.get('api_base_url', 'https://api.openai.com/v1'),
        help="API 端点地址，如使用本地模型可修改为 http://localhost:11434/v1"
    )
    
    model = st.text_input(
        "模型名称",
        value=st.session_state.get('model', 'gpt-3.5-turbo'),
        help="模型名称，如 gpt-4, gpt-3.5-turbo, llama2 等"
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("💾 保存配置", type="primary"):
            st.session_state.api_key = api_key
            st.session_state.api_base_url = api_base_url
            st.session_state.model = model
            save_config()
            st.success("✅ 配置已保存！")
            st.rerun()
    
    with col2:
        if st.button("🧪 测试连接"):
            if not api_key:
                st.error("❌ 请先输入 API Key")
            else:
                with st.spinner("测试连接中..."):
                    # 测试 API 连接
                    try:
                        import sys
                        import os
                        sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
                        from ame.llm_caller.caller import LLMCaller
                        
                        llm = LLMCaller(api_key=api_key, base_url=api_base_url, model=model)
                        # 简单测试
                        response = llm.generate(
                            messages=[{"role": "user", "content": "Hi"}],
                            temperature=0.7,
                            max_tokens=10
                        )
                        st.success("✅ 连接成功！")
                    except Exception as e:
                        st.error(f"❌ 连接失败: {str(e)}")
    
    st.markdown("---")
    
    # 数据存储配置
    st.subheader("💾 数据存储")
    
    st.info("""
    - 📁 数据目录: `./data/`
    - 📦 向量库: `./data/vector_store/`
    - 📝 上传文件: `./data/uploads/`
    - ⚙️ 配置文件: `./data/runtime_config.json`
    """)
    
    st.markdown("---")
    
    # 系统信息
    st.subheader("ℹ️ 系统信息")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("版本", "v0.4.0")
    
    with col2:
        st.metric("AME 引擎", "v0.4.0")
    
    with col3:
        status = "✅ 已配置" if st.session_state.is_configured else "⚠️ 未配置"
        st.metric("状态", status)
