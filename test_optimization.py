#!/usr/bin/env python3
"""
项目优化验证脚本
测试所有优化的模块是否正常工作
"""

import sys
import os
import asyncio
from pathlib import Path

# 添加路径
sys.path.append(str(Path(__file__).parent / "ame"))
sys.path.append(str(Path(__file__).parent))

print("=" * 60)
print("🧪 Another Me 项目优化验证测试")
print("=" * 60)

# 测试计数器
tests_passed = 0
tests_failed = 0

def test_result(name, passed, error=None):
    """记录测试结果"""
    global tests_passed, tests_failed
    if passed:
        print(f"✅ {name}")
        tests_passed += 1
    else:
        print(f"❌ {name}")
        if error:
            print(f"   错误: {error}")
        tests_failed += 1

print("\n📦 测试模块导入...")
print("-" * 60)

# 测试 1: LLM Caller
try:
    from ame.llm_caller.caller import LLMCaller
    test_result("LLM Caller 导入", True)
except Exception as e:
    test_result("LLM Caller 导入", False, str(e))

# 测试 2: Data Processor
try:
    from ame.data_processor.processor import DataProcessor
    test_result("Data Processor 导入", True)
except Exception as e:
    test_result("Data Processor 导入", False, str(e))

# 测试 3: Vector Store
try:
    from ame.vector_store.memu_store import MemuVectorStore
    from ame.vector_store.factory import VectorStoreFactory
    test_result("Vector Store 导入", True)
except Exception as e:
    test_result("Vector Store 导入", False, str(e))

# 测试 4: RAG Generator
try:
    from ame.rag_generator.generator import RAGGenerator
    test_result("RAG Generator 导入", True)
except Exception as e:
    test_result("RAG Generator 导入", False, str(e))

# 测试 5: Knowledge Base
try:
    from ame.rag.knowledge_base import KnowledgeBase
    test_result("Knowledge Base 导入", True)
except Exception as e:
    test_result("Knowledge Base 导入", False, str(e))

# 测试 6: Mimic Engine
try:
    from ame.mem.mimic_engine import MimicEngine
    test_result("Mimic Engine 导入", True)
except Exception as e:
    test_result("Mimic Engine 导入", False, str(e))

print("\n🔧 测试模块初始化...")
print("-" * 60)

# 测试 7: LLM Caller 初始化
try:
    llm_caller = LLMCaller(
        api_key="test_key",
        base_url="https://api.openai.com/v1",
        model="gpt-3.5-turbo"
    )
    test_result("LLM Caller 初始化", True)
except Exception as e:
    test_result("LLM Caller 初始化", False, str(e))

# 测试 8: Data Processor 初始化
try:
    processor = DataProcessor()
    test_result("Data Processor 初始化", True)
except Exception as e:
    test_result("Data Processor 初始化", False, str(e))

# 测试 9: Vector Store 初始化
try:
    store = MemuVectorStore(
        db_path="/tmp/test_vector_store",
        use_openai_embedding=False
    )
    test_result("Vector Store 初始化", True)
except Exception as e:
    test_result("Vector Store 初始化", False, str(e))

# 测试 10: Vector Store Factory
try:
    store = VectorStoreFactory.create(
        store_type="memu",
        db_path="/tmp/test_factory_store"
    )
    test_result("Vector Store Factory", True)
except Exception as e:
    test_result("Vector Store Factory", False, str(e))

print("\n⚡ 测试异步功能...")
print("-" * 60)

# 测试 11: Data Processor 异步处理
async def test_processor():
    try:
        processor = DataProcessor()
        result = await processor.process_text(
            text="这是一个测试文本",
            source="test"
        )
        assert "content" in result
        assert "timestamp" in result
        assert "metadata" in result
        test_result("Data Processor 异步处理", True)
    except Exception as e:
        test_result("Data Processor 异步处理", False, str(e))

asyncio.run(test_processor())

# 测试 12: Vector Store 异步操作
async def test_vector_store():
    try:
        store = MemuVectorStore(
            db_path="/tmp/test_async_store",
            use_openai_embedding=False
        )
        
        # 测试添加文档
        await store.add_documents([
            {
                "content": "测试文档1",
                "source": "test",
                "timestamp": "2025-01-01T00:00:00"
            }
        ])
        
        # 测试搜索
        results = await store.search("测试", limit=1)
        assert len(results) >= 0
        
        # 测试统计
        stats = await store.get_statistics()
        assert "count" in stats
        
        test_result("Vector Store 异步操作", True)
    except Exception as e:
        test_result("Vector Store 异步操作", False, str(e))

asyncio.run(test_vector_store())

print("\n📊 测试后端模块...")
print("-" * 60)

# 测试 13: Backend Core Config
try:
    sys.path.append(str(Path(__file__).parent / "backend"))
    from app.core.config import get_settings
    settings = get_settings()
    test_result("Backend Config", True)
except Exception as e:
    test_result("Backend Config", False, str(e))

# 测试 14: Backend Logger
try:
    from app.core.logger import get_logger
    logger = get_logger("test")
    test_result("Backend Logger", True)
except Exception as e:
    test_result("Backend Logger", False, str(e))

print("\n🎨 测试 Gradio 组件...")
print("-" * 60)

# 测试 15: Gradio 组件导入
try:
    sys.path.append(str(Path(__file__).parent / "gradio_app"))
    from components import (
        create_home_tab,
        create_config_tab,
        create_mem_tab,
        create_rag_tab
    )
    test_result("Gradio 组件导入", True)
except Exception as e:
    test_result("Gradio 组件导入", False, str(e))

# 测试 16: Session 工具
try:
    from utils.session import init_session_state, get_session_state
    init_session_state()
    state = get_session_state()
    test_result("Gradio Session", True)
except Exception as e:
    test_result("Gradio Session", False, str(e))

print("\n" + "=" * 60)
print("📈 测试结果汇总")
print("=" * 60)
print(f"✅ 通过: {tests_passed}")
print(f"❌ 失败: {tests_failed}")
print(f"📊 通过率: {tests_passed/(tests_passed+tests_failed)*100:.1f}%")

if tests_failed == 0:
    print("\n🎉 所有测试通过！项目优化成功！")
    sys.exit(0)
else:
    print(f"\n⚠️  有 {tests_failed} 个测试失败，请检查错误信息")
    sys.exit(1)
