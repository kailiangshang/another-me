"""
主页组件
"""

import gradio as gr
import sys
import os
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.session import get_session_state


def get_system_stats():
    """获取系统统计信息"""
    state = get_session_state()
    
    rag_docs = 0
    rag_sources = 0
    mem_count = 0
    mem_sources = 0
    
    try:
        if state.get('rag_kb'):
            stats = asyncio.run(state['rag_kb'].get_statistics())
            rag_docs = stats.get('total_documents', 0)
            rag_sources = len(stats.get('sources', {}))
    except:
        pass
    
    try:
        if state.get('mimic_engine'):
            stats = asyncio.run(state['mimic_engine'].vector_store.get_statistics())
            mem_count = stats.get('count', 0)
            mem_sources = len(stats.get('sources', {}))
    except:
        pass
    
    return rag_docs, rag_sources, mem_count, mem_sources


def create_home_tab():
    """创建主页"""
    
    state = get_session_state()
    
    with gr.Column():
        # 欢迎区域
        gr.HTML(
            """
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 40px; border-radius: 20px; text-align: center; color: white;
                        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3); margin-bottom: 30px;">
                <h2 style="font-size: 2em; margin-bottom: 15px;">🌟 欢迎使用 Another Me</h2>
                <p style="font-size: 1.2em; opacity: 0.95; margin-bottom: 10px;">世界上另一个我 - 你的 AI 数字分身系统</p>
                <p style="opacity: 0.85;">通过先进的 RAG 技术和记忆模仿，创建一个真正理解你、能够代表你思考和表达的 AI 助手</p>
            </div>
            """
        )
    
    # 系统状态
    if state.get('is_configured'):
        gr.HTML(
            """
            <div style="text-align: center; margin-bottom: 25px;">
                <h3 style="color: #667eea; margin-bottom: 15px;">📊 系统状态</h3>
            </div>
            """
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML(
                    """
                    <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                                padding: 25px; border-radius: 15px; text-align: center;
                                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <div style="font-size: 2.5em; margin-bottom: 10px;">📚</div>
                        <div style="font-size: 1.1em; font-weight: 600; color: #333;">知识库文档</div>
                    </div>
                    """
                )
                rag_docs_num = gr.Number(label="", value=0, interactive=False, container=False)
            
            with gr.Column(scale=1):
                gr.HTML(
                    """
                    <div style="background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
                                padding: 25px; border-radius: 15px; text-align: center;
                                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <div style="font-size: 2.5em; margin-bottom: 10px;">🏷️</div>
                        <div style="font-size: 1.1em; font-weight: 600; color: #333;">知识来源</div>
                    </div>
                    """
                )
                rag_sources_num = gr.Number(label="", value=0, interactive=False, container=False)
            
            with gr.Column(scale=1):
                gr.HTML(
                    """
                    <div style="background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
                                padding: 25px; border-radius: 15px; text-align: center;
                                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <div style="font-size: 2.5em; margin-bottom: 10px;">💬</div>
                        <div style="font-size: 1.1em; font-weight: 600; color: #333;">对话记忆</div>
                    </div>
                    """
                )
                mem_count_num = gr.Number(label="", value=0, interactive=False, container=False)
            
            with gr.Column(scale=1):
                gr.HTML(
                    """
                    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                                padding: 25px; border-radius: 15px; text-align: center;
                                box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                        <div style="font-size: 2.5em; margin-bottom: 10px;">🧠</div>
                        <div style="font-size: 1.1em; font-weight: 600; color: #fff;">记忆来源</div>
                    </div>
                    """
                )
                mem_sources_num = gr.Number(label="", value=0, interactive=False, container=False)
        
        with gr.Row():
            refresh_btn = gr.Button("🔄 刷新统计", variant="primary", size="sm")
        
        refresh_btn.click(
            fn=get_system_stats,
            outputs=[rag_docs_num, rag_sources_num, mem_count_num, mem_sources_num]
        )
    else:
        gr.HTML(
            """
            <div style="background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
                        padding: 30px; border-radius: 15px; text-align: center;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin: 20px 0;">
                <div style="font-size: 3em; margin-bottom: 15px;">⚠️</div>
                <h3 style="color: #d63031; margin-bottom: 10px;">请先在配置页面设置 API Key</h3>
                <p style="color: #666;">点击上方 "⚙️ 配置" 标签页开始设置</p>
            </div>
            """
        )
    
    gr.HTML("<div style='margin: 30px 0; border-top: 2px solid #e0e0e0;'></div>")
    
    # 快速开始
    gr.HTML(
        """
        <div style="text-align: center; margin-bottom: 25px;">
            <h3 style="color: #667eea; font-size: 1.8em;">🚀 快速开始</h3>
            <p style="color: #888;">选择一个功能开始你的 AI 分身之旅</p>
        </div>
        """
    )
    
    with gr.Row(equal_height=True):
        with gr.Column(scale=1):
            gr.HTML(
                """
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            padding: 30px; border-radius: 15px; color: white; height: 100%;
                            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
                            transition: transform 0.3s ease;">
                    <div style="font-size: 3em; text-align: center; margin-bottom: 15px;">📚</div>
                    <h3 style="text-align: center; margin-bottom: 15px;">📚 RAG 知识库</h3>
                    <p style="opacity: 0.95; line-height: 1.6;">
                        • 上传你的笔记、文档和资料<br>
                        • AI 将学习并理解你的知识体系<br>
                        • 随时检索和问答
                    </p>
                    <p style="opacity: 0.8; font-size: 0.9em; margin-top: 15px;">
                        <strong>支持格式</strong>: TXT, MD, PDF, DOCX, JSON
                    </p>
                </div>
                """
            )
        
        with gr.Column(scale=1):
            gr.HTML(
                """
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                            padding: 30px; border-radius: 15px; color: white; height: 100%;
                            box-shadow: 0 8px 20px rgba(240, 147, 251, 0.3);
                            transition: transform 0.3s ease;">
                    <div style="font-size: 3em; text-align: center; margin-bottom: 15px;">💬</div>
                    <h3 style="text-align: center; margin-bottom: 15px;">💬 MEM 记忆模仿</h3>
                    <p style="opacity: 0.95; line-height: 1.6;">
                        • 上传你的聊天记录和对话<br>
                        • AI 学习你的说话风格和思维方式<br>
                        • 让 AI 分身用你的方式说话
                    </p>
                    <p style="opacity: 0.8; font-size: 0.9em; margin-top: 15px;">
                        <strong>特点</strong>: 实时流式对话，自然流畅
                    </p>
                </div>
                """
            )
    
    gr.HTML("<div style='margin: 30px 0; border-top: 2px solid #e0e0e0;'></div>")
    
    # 核心功能介绍
    gr.HTML(
        """
        <div style="text-align: center; margin-bottom: 25px;">
            <h3 style="color: #667eea; font-size: 1.8em;">💡 核心功能</h3>
        </div>
        """
    )
    
    with gr.Accordion("📚 知识管理", open=False):
        gr.Markdown(
            """
            - **文档上传**: 支持 TXT, MD, PDF, DOCX, JSON 等格式
            - **向量检索**: 高效的语义搜索和相关度排序
            - **混合检索**: 结合向量、关键词和时间权重
            - **来源管理**: 按来源分类和筛选知识
            - **统计分析**: 可视化知识库分布和增长趋势
            """
        )
    
    with gr.Accordion("💬 对话模仿", open=False):
        gr.Markdown(
            """
            - **对话学习**: 从聊天记录中学习你的表达习惯
            - **风格模仿**: 复现你的语气、用词和思维方式
            - **流式对话**: 实时生成，自然流畅
            - **记忆管理**: 查看和管理所有学习记录
            - **时间线视图**: 按时间浏览对话历史
            """
        )
    
    with gr.Accordion("📊 智能分析", open=False):
        gr.Markdown(
            """
            - **个性分析**: 基于对话和知识的个性洞察
            - **知识图谱**: 可视化你的知识结构
            - **对话模式**: 分析你的表达特点和习惯
            - **多格式导出**: Markdown, HTML
            """
        )
    
    gr.HTML("<div style='margin: 30px 0; border-top: 2px solid #e0e0e0;'></div>")
    
    # 技术栈信息
    gr.HTML(
        """
        <div style="text-align: center; margin-bottom: 20px;">
            <h3 style="color: #667eea;">📖 技术栈 & 版本信息</h3>
        </div>
        """
    )
    
    with gr.Row():
        with gr.Column():
            gr.HTML(
                """
                <div style="background: #f8f9fa; padding: 25px; border-radius: 15px;
                            border-left: 4px solid #667eea; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                    <h4 style="color: #667eea; margin-bottom: 15px;">📖 技术栈</h4>
                    <ul style="line-height: 2; color: #555; list-style: none; padding-left: 0;">
                        <li>• <strong>Gradio 4.0</strong> - 现代化前端框架</li>
                        <li>• <strong>AME v0.7.0</strong> - 技术引擎</li>
                        <li>• <strong>Memu</strong> - 向量数据库</li>
                        <li>• <strong>流式输出</strong> - 实时对话体验</li>
                    </ul>
                </div>
                """
            )
        
        with gr.Column():
            gr.HTML(
                """
                <div style="background: #f8f9fa; padding: 25px; border-radius: 15px;
                            border-left: 4px solid #f5576c; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                    <h4 style="color: #f5576c; margin-bottom: 15px;">ℹ️ 版本信息</h4>
                    <ul style="line-height: 2; color: #555; list-style: none; padding-left: 0;">
                        <li>• <strong>版本</strong>: v0.7.0</li>
                        <li>• <strong>更新</strong>: 2025-10-23</li>
                        <li>• <strong>许可</strong>: MIT License</li>
                        <li>• <strong>前端</strong>: Gradio</li>
                    </ul>
                </div>
                """
            )
