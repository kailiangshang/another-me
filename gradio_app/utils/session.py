"""
会话状态管理
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


# 全局状态存储
_session_state = {}


def init_session_state():
    """初始化会话状态"""
    global _session_state
    
    # 默认配置
    _session_state = {
        'is_configured': False,
        'api_key': '',
        'api_base_url': 'https://api.openai.com/v1',
        'model': 'gpt-3.5-turbo',
        'rag_kb': None,
        'mimic_engine': None,
        'mem_chat_history': []
    }
    
    # 尝试加载已保存的配置
    load_config()


def get_session_state() -> Dict[str, Any]:
    """获取会话状态"""
    return _session_state


def update_session_state(key: str, value: Any):
    """更新会话状态"""
    _session_state[key] = value


def save_config():
    """保存配置到文件"""
    config_dir = Path("/app/data") if os.path.exists("/app/data") else Path("./data")
    config_dir.mkdir(parents=True, exist_ok=True)
    
    config_file = config_dir / "runtime_config.json"
    
    config = {
        'api_key': _session_state.get('api_key', ''),
        'api_base_url': _session_state.get('api_base_url', 'https://api.openai.com/v1'),
        'model': _session_state.get('model', 'gpt-3.5-turbo')
    }
    
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    # 更新配置状态
    if config['api_key']:
        _session_state['is_configured'] = True


def load_config():
    """从文件加载配置"""
    config_dir = Path("/app/data") if os.path.exists("/app/data") else Path("./data")
    config_file = config_dir / "runtime_config.json"
    
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            _session_state['api_key'] = config.get('api_key', '')
            _session_state['api_base_url'] = config.get('api_base_url', 'https://api.openai.com/v1')
            _session_state['model'] = config.get('model', 'gpt-3.5-turbo')
            
            if config.get('api_key'):
                _session_state['is_configured'] = True
        except Exception as e:
            print(f"加载配置失败: {e}")
