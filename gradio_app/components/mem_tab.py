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


def chat_response(message, history, temperature):
    """生成对话响应（流式）"""
    state = get_session_state()
    
    if not state.get('is_configured'):
        yield "⚠️ 请先在配置页面设置 API Key"
        return
    
    if not message.strip():
        yield "请输入消息..."
        return
    
    try:
        engine = init_mimic_engine()
        
        # 流式生成
        full_response = ""
        
        async def generate():
            nonlocal full_response
            async for chunk in engine.generate_response_stream(
                prompt=message,
                temperature=temperature,
                use_history=True
            ):
                full_response += chunk
                yield full_response
        
        # 运行异步生成器
        for response in asyncio.run(generate()):
            yield response
        
        # 学习这次对话
        asyncio.run(engine.learn_from_conversation(
            user_message=message,
            context=full_response
        ))
        
    except Exception as e:
        yield f"❌ 生成失败: {str(e)}"


def upload_and_learn(file, progress=gr.Progress()):
    """上传并学习聊天记录"""
    state = get_session_state()
    
    if not state.get('is_configured'):
        return "⚠️ 请先在配置页面设置 API Key"
    
    if file is None:
        return "请先上传文件"
    
    try:
        engine = init_mimic_engine()
        
        # 读取文件内容
        with open(file.name, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按行分割
        lines = content.split('\n')
        messages = [line.strip() for line in lines if line.strip()]
        
        # 学习每条消息
        for i, msg in enumerate(messages):
            progress((i + 1) / len(messages), desc=f"学习中 {i+1}/{len(messages)}")
            asyncio.run(engine.learn_from_conversation(
                user_message=msg,
                metadata={"source": "uploaded_chat"}
            ))
        
        return f"✅ 已学习 {len(messages)} 条消息！"
    
    except Exception as e:
        return f"❌ 学习失败: {str(e)}"


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
                avatar_images=(None, "🤖"),
                bubble_full_width=False
            )
            
            with gr.Row():
                with gr.Column(scale=4):
                    msg_input = gr.Textbox(
                        placeholder="输入消息...",
                        show_label=False,
                        container=False
                    )
                with gr.Column(scale=1):
                    temperature_slider = gr.Slider(
                        minimum=0.0,
                        maximum=2.0,
                        value=0.8,
                        step=0.1,
                        label="温度",
                        info="控制回复的随机性"
                    )
            
            with gr.Row():
                send_btn = gr.Button("📤 发送", variant="primary")
                clear_btn = gr.Button("🗑️ 清空对话")
            
            # 绑定事件
            msg_input.submit(
                fn=chat_response,
                inputs=[msg_input, chatbot, temperature_slider],
                outputs=[chatbot],
            )
            
            send_btn.click(
                fn=chat_response,
                inputs=[msg_input, chatbot, temperature_slider],
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
                outputs=[upload_status]
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
                    return "请输入内容"
                
                try:
                    engine = init_mimic_engine()
                    asyncio.run(engine.learn_from_conversation(
                        user_message=text,
                        metadata={"source": "manual_input"}
                    ))
                    return "✅ 已学习！"
                except Exception as e:
                    return f"❌ 失败: {str(e)}"
            
            manual_btn.click(
                fn=learn_manual,
                inputs=[manual_text],
                outputs=[manual_status]
            )
    
    # 加载时刷新统计
    gr.on(
        triggers=[],
        fn=get_statistics,
        outputs=[memory_count, source_count, status_text]
    )
