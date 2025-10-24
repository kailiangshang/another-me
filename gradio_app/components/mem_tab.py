"""
MEM 对话页面组件 - 支持流式输出
"""

import gradio as gr
import sys
import os
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from ame.mem.mimic_engine import MimicEngine
from ame.llm_caller.caller import LLMCaller
from utils.session import get_session_state, update_session_state


def init_mimic_engine():
    """初始化模仿引擎"""
    state = get_session_state()
    
    if state.get('mimic_engine') is None:
        llm_caller = LLMCaller(
            api_key=state.get('api_key'),
            base_url=state.get('api_base_url'),
            model=state.get('model')
        )
        engine = MimicEngine(llm_caller=llm_caller)
        update_session_state('mimic_engine', engine)
        return engine
    
    return state.get('mimic_engine')


def get_statistics():
    """获取统计信息"""
    try:
        engine = init_mimic_engine()
        stats = asyncio.run(engine.vector_store.get_statistics())
        return (
            stats.get('count', 0),
            len(stats.get('sources', {})),
            "✅ 正常"
        )
    except:
        return 0, 0, "⚠️ 未初始化"


def chat_response(message, history):
    """生成对话响应（流式）"""
    state = get_session_state()
    
    if not state.get('is_configured'):
        gr.Warning("⚠️ 请先在配置页面设置 API Key")
        return history
    
    if not message or not message.strip():
        return history
    
    try:
        engine = init_mimic_engine()
        
        # 添加用户消息
        history = history + [{"role": "user", "content": message}]
        
        # 流式生成助手回复
        assistant_message = ""
        
        # 定义异步生成器
        async def async_generate():
            nonlocal assistant_message
            async for chunk in engine.generate_response_stream(
                prompt=message,
                temperature=0.8,
                use_history=True
            ):
                assistant_message += chunk
                # 更新历史记录，显示当前生成的内容
                current_history = history + [{"role": "assistant", "content": assistant_message}]
                yield current_history
        
        # 运行异步生成器
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        final_history = history
        try:
            gen = async_generate()
            while True:
                try:
                    current_history = loop.run_until_complete(gen.__anext__())
                    final_history = current_history
                    yield current_history
                except StopAsyncIteration:
                    break
        finally:
            loop.close()
        
        # 学习这次对话
        if assistant_message:
            asyncio.run(engine.learn_from_conversation(
                user_message=message,
                context=assistant_message
            ))
        
        return final_history
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        gr.Error(f"生成失败: {str(e)}")
        return history


def upload_and_learn(file):
    """上传并学习聊天记录"""
    state = get_session_state()
    
    if not state.get('is_configured'):
        gr.Warning("⚠️ 请先在配置页面设置 API Key")
        return "⚠️ 请先配置 API Key", None
    
    if file is None:
        gr.Warning("请先上传文件")
        return "请先上传文件", None
    
    try:
        engine = init_mimic_engine()
        
        # 读取文件内容
        if hasattr(file, 'name'):
            file_path = file.name
        else:
            file_path = file
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按行分割
        lines = content.split('\n')
        messages = [line.strip() for line in lines if line.strip()]
        
        # 学习每条消息
        for msg in messages:
            asyncio.run(engine.learn_from_conversation(
                user_message=msg,
                metadata={"source": "uploaded_chat"}
            ))
        
        gr.Info(f"✅ 已学习 {len(messages)} 条消息！")
        return f"✅ 已学习 {len(messages)} 条消息！", None  # 清空文件输入
    
    except Exception as e:
        gr.Error(f"学习失败: {str(e)}")
        return f"❌ 学习失败: {str(e)}", None


def create_mem_tab():
    """创建 MEM 对话页面"""
    
    with gr.Column():
        gr.HTML(
            """
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                        padding: 30px; border-radius: 15px; text-align: center; color: white;
                        box-shadow: 0 8px 20px rgba(240, 147, 251, 0.3); margin-bottom: 25px;">
                <h2 style="font-size: 1.8em; margin-bottom: 10px;">💬 MEM 对话</h2>
                <p style="opacity: 0.95;">与 AI 分身对话，它会模仿你的说话风格。上传聊天记录让它学习，对话会被记录以持续改进。</p>
            </div>
            """
        )
    
    # 统计信息卡片
    gr.HTML(
        """
        <div style="text-align: center; margin-bottom: 15px;">
            <h3 style="color: #667eea;">📊 记忆统计</h3>
        </div>
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML(
                """
                <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
                            border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    <div style="font-size: 2em; margin-bottom: 5px;">💬</div>
                    <div style="font-weight: 600; color: #333;">总记忆数</div>
                </div>
                """
            )
            memory_count = gr.Number(label="", value=0, interactive=False, container=False)
        
        with gr.Column(scale=1):
            gr.HTML(
                """
                <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%);
                            border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    <div style="font-size: 2em; margin-bottom: 5px;">🏷️</div>
                    <div style="font-weight: 600; color: #333;">来源类型</div>
                </div>
                """
            )
            source_count = gr.Number(label="", value=0, interactive=False, container=False)
        
        with gr.Column(scale=1):
            gr.HTML(
                """
                <div style="text-align: center; padding: 15px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                            border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    <div style="font-size: 2em; margin-bottom: 5px; color: white;">🟢</div>
                    <div style="font-weight: 600; color: white;">系统状态</div>
                </div>
                """
            )
            status_text = gr.Textbox(label="", value="", interactive=False, container=False)
    
    with gr.Row():
        refresh_btn = gr.Button("🔄 刷新统计", variant="primary", size="sm")
    
    refresh_btn.click(
        fn=get_statistics,
        outputs=[memory_count, source_count, status_text]
    )
    
    gr.HTML("<div style='margin: 25px 0; border-top: 2px solid #e0e0e0;'></div>")
    
    # 主要内容区域
    with gr.Tabs():
        
        # 对话标签页
        with gr.TabItem("💬 对话"):
            
            # 聊天界面
            chatbot = gr.Chatbot(
                label="AI 分身对话",
                height=500,
                type="messages",
                avatar_images=(None, "🤖")
            )
            
            msg_input = gr.Textbox(
                placeholder="输入消息...",
                show_label=False,
                container=False
            )
            
            with gr.Row():
                send_btn = gr.Button("📤 发送", variant="primary")
                clear_btn = gr.Button("🗑️ 清空对话")
            
            # 绑定事件 - 添加清空输入框
            def submit_and_clear(message, history):
                # 返回空字符串清空输入框
                return "", history
            
            msg_input.submit(
                fn=submit_and_clear,
                inputs=[msg_input, chatbot],
                outputs=[msg_input, chatbot],
            ).then(
                fn=chat_response,
                inputs=[msg_input, chatbot],
                outputs=[chatbot],
            )
            
            send_btn.click(
                fn=submit_and_clear,
                inputs=[msg_input, chatbot],
                outputs=[msg_input, chatbot],
            ).then(
                fn=chat_response,
                inputs=[msg_input, chatbot],
                outputs=[chatbot],
            )
            
            clear_btn.click(
                fn=lambda: [],
                outputs=[chatbot]
            )
        
        # 学习材料标签页
        with gr.TabItem("📚 学习材料"):
            
            gr.HTML(
                """
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;
                            border-left: 4px solid #667eea;">
                    <h3 style="color: #667eea; margin-bottom: 10px;">📚 上传聊天记录</h3>
                    <p style="color: #666; line-height: 1.6;">
                        上传你的聊天记录文本文件，让 AI 学习你的说话风格。
                    </p>
                    <p style="color: #667eea; margin-top: 10px; font-weight: 600;">
                        • 支持格式：纯文本（每行一条消息）、JSON 格式的聊天记录
                    </p>
                </div>
                """
            )
            
            file_upload = gr.File(
                label="选择聊天记录文件",
                file_types=[".txt", ".json"],
                type="filepath"
            )
            
            upload_btn = gr.Button("📚 开始学习", variant="primary")
            upload_status = gr.Textbox(label="状态", interactive=False)
            
            upload_btn.click(
                fn=upload_and_learn,
                inputs=[file_upload],
                outputs=[upload_status, file_upload]  # 清空文件输入
            )
            
            gr.HTML("<div style='margin: 20px 0; border-top: 1px solid #e0e0e0;'></div>")
            
            gr.HTML(
                """
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;
                            border-left: 4px solid #f5576c;">
                    <h3 style="color: #f5576c; margin-bottom: 10px;">✍️ 手动输入</h3>
                    <p style="color: #666;">直接输入你的聊天记录、日记或想法，让 AI 学习</p>
                </div>
                """
            )
            
            manual_text = gr.Textbox(
                label="输入一段你说过的话",
                placeholder="输入你的聊天记录、日记、想法...",
                lines=5
            )
            
            manual_btn = gr.Button("💾 保存并学习")
            manual_status = gr.Textbox(label="状态", interactive=False, show_label=False)
            
            def learn_manual(text):
                if not text.strip():
                    gr.Warning("请输入内容")
                    return "请输入内容", text
                
                try:
                    engine = init_mimic_engine()
                    asyncio.run(engine.learn_from_conversation(
                        user_message=text,
                        metadata={"source": "manual_input"}
                    ))
                    gr.Info("✅ 已学习！")
                    return "✅ 已学习！", ""  # 清空输入框
                except Exception as e:
                    gr.Error(f"失败: {str(e)}")
                    return f"❌ 失败: {str(e)}", text
            
            manual_btn.click(
                fn=learn_manual,
                inputs=[manual_text],
                outputs=[manual_status, manual_text]  # 清空文本输入
            )
    
    # 加载时刷新统计
    gr.on(
        triggers=[],
        fn=get_statistics,
        outputs=[memory_count, source_count, status_text]
    )
