"""
Another Me - Streamlit 前端应用
主界面：RAG 知识管理 + MEM 记忆模仿
"""

import streamlit as st
import sys
import os

# 添加 AME 模块到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pages import (
    home_page,
    config_page,
    rag_page,
    mem_page,
    analysis_page,
    knowledge_manager_page,
    memory_manager_page
)
from utils.session import init_session_state

# 页面配置
st.set_page_config(
    page_title="Another Me - 世界上另一个我",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化会话状态
init_session_state()

# 侧边栏
with st.sidebar:
    # Logo
    logo_path = os.path.join(os.path.dirname(__file__), '..', 'another me logo.jpg')
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    
    st.title("🌟 Another Me")
    st.markdown("**世界上另一个我**")
    st.markdown("---")
    
    # 导航菜单
    page = st.radio(
        "导航",
        [
            "🏠 主页",
            "⚙️ 配置",
            "📚 RAG 知识库",
            "📂 知识库管理",
            "💬 MEM 对话",
            "🧠 记忆管理",
            "📊 分析报告"
        ],
        key="navigation"
    )
    
    st.markdown("---")
    
    # 配置状态
    if st.session_state.get('is_configured', False):
        st.success("✅ 已配置")
    else:
        st.warning("⚠️ 请先配置 API Key")
    
    st.markdown("---")
    st.markdown("v0.4.0 | MIT License")

# 主内容区域
if page == "🏠 主页":
    home_page.show()
elif page == "⚙️ 配置":
    config_page.show()
elif page == "📚 RAG 知识库":
    rag_page.show()
elif page == "📂 知识库管理":
    knowledge_manager_page.show()
elif page == "💬 MEM 对话":
    mem_page.show()
elif page == "🧠 记忆管理":
    memory_manager_page.show()
elif page == "📊 分析报告":
    analysis_page.show()
