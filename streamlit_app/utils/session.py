"""
会话状态管理
"""

import streamlit as st
import os
import json
from pathlib import Path


def init_session_state():
    """初始化会话状态"""
    
    # API 配置
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    
    if 'api_base_url' not in st.session_state:
        st.session_state.api_base_url = "https://api.openai.com/v1"
    
    if 'model' not in st.session_state:
        st.session_state.model = "gpt-3.5-turbo"
    
    if 'is_configured' not in st.session_state:
        st.session_state.is_configured = False
        # 尝试从配置文件加载
        load_config()
    
    # RAG 知识库状态
    if 'rag_documents' not in st.session_state:
        st.session_state.rag_documents = []
    
    # MEM 对话历史
    if 'mem_chat_history' not in st.session_state:
        st.session_state.mem_chat_history = []
    
    # 分析报告
    if 'analysis_reports' not in st.session_state:
        st.session_state.analysis_reports = {}


def load_config():
    """从文件加载配置"""
    config_file = Path("./data/runtime_config.json")
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                st.session_state.api_key = config.get('OPENAI_API_KEY', '')
                st.session_state.api_base_url = config.get('OPENAI_BASE_URL', 'https://api.openai.com/v1')
                st.session_state.model = config.get('OPENAI_MODEL', 'gpt-3.5-turbo')
                st.session_state.is_configured = bool(st.session_state.api_key)
        except:
            pass


def save_config():
    """保存配置到文件"""
    config_file = Path("./data/runtime_config.json")
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    config = {
        'OPENAI_API_KEY': st.session_state.api_key,
        'OPENAI_BASE_URL': st.session_state.api_base_url,
        'OPENAI_MODEL': st.session_state.model
    }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    st.session_state.is_configured = bool(st.session_state.api_key)
