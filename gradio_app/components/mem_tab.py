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
    
    gr.Markdown(
        """
        ## 💬 MEM 对话
        
        与 AI 分身对话，它会模仿你的说话风格。上传聊天记录让它学习，对话会被记录以持续改进。
        """
    )
    
    # 统计信息卡片
    with gr.Row():
        memory_count = gr.Number(label="💬 总记忆数", value=0, interactive=False)
        source_count = gr.Number(label="🏷️ 来源类型", value=0, interactive=False)
        status_text = gr.Textbox(label="📊 状态", value="", interactive=False)
        refresh_btn = gr.Button("🔄 刷新统计", size="sm")
    
    refresh_btn.click(
        fn=get_statistics,
        outputs=[memory_count, source_count, status_text]
    )
    
    gr.Markdown("---")
    
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
            
            gr.Markdown(
                """
                ### 上传聊天记录
                
                上传你的聊天记录文本文件，让 AI 学习你的说话风格。
                
                **支持格式**：
                - 纯文本（每行一条消息）
                - JSON 格式的聊天记录
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
            
            gr.Markdown("---")
            
            gr.Markdown("### ✍️ 手动输入")
            
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
