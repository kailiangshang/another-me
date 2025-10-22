"""
分析报告页面
"""

import streamlit as st
import sys
import os
from datetime import datetime
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from utils.export import export_to_markdown, export_to_pdf, export_to_html, PDF_AVAILABLE


def show():
    """显示分析报告页面"""
    
    st.title("📊 分析报告")
    
    st.markdown("""
    生成自我认知分析报告，包括情绪分析、关键词提取、人际关系等。
    支持导出为 Markdown、HTML、PDF 格式。
    """)
    
    if not st.session_state.is_configured:
        st.warning("⚠️ 请先在配置页面设置 API Key")
        return
    
    st.markdown("---")
    
    # 报告类型选择
    report_type = st.selectbox(
        "选择报告类型",
        ["综合分析", "情绪分析", "关键词分析", "对话统计"]
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        if st.button("📊 生成报告", type="primary"):
            with st.spinner("生成中..."):
                report_data = generate_report(report_type)
                st.session_state.current_report = report_data
                st.success("✅ 报告生成完成！")
                st.rerun()
    
    # 显示报告
    if 'current_report' in st.session_state:
        report_data = st.session_state.current_report
        
        st.markdown("---")
        
        # 报告内容显示
        st.subheader(f"📄 {report_data['title']}")
        st.caption(f"生成时间: {report_data['timestamp']}")
        
        st.markdown(f"### 📊 {report_data['summary']}")
        
        for section in report_data.get('sections', []):
            with st.expander(f"📌 {section['title']}", expanded=True):
                st.markdown(section['content'])
                
                if 'data' in section:
                    st.dataframe(section['data'], use_container_width=True)
        
        st.markdown("---")
        
        # 导出选项
        st.subheader("📥 导出报告")
        
        # 根据 PDF 是否可用选择格式
        export_formats = ["Markdown (.md)", "HTML (.html)"]
        if PDF_AVAILABLE:
            export_formats.append("PDF (.pdf)")
        else:
            st.info("💡 PDF 导出不可用：缺少 wkhtmltopdf。可导出 HTML 后在浏览器中打印为 PDF。")
        
        export_format = st.radio(
            "选择格式",
            export_formats,
            horizontal=True
        )
        
        output_filename = st.text_input(
            "文件名",
            value=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        if st.button("💾 导出", type="primary"):
            export_report(report_data, export_format, output_filename)


def generate_report(report_type: str) -> dict:
    """生成报告数据"""
    
    # 模拟报告数据
    report_data = {
        "title": f"{report_type}报告",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary": f"这是一份{report_type}，包含了详细的数据分析和洞察。",
        "sections": []
    }
    
    if report_type == "综合分析":
        report_data["sections"] = [
            {
                "title": "整体概况",
                "content": "基于您的对话记录和知识库，我们发现了以下特点...",
                "data": {
                    "总对话数": 156,
                    "知识文档数": 42,
                    "活跃天数": 28
                }
            },
            {
                "title": "情绪趋势",
                "content": "您的情绪整体保持稳定，积极情绪占比较高。",
                "data": {
                    "积极": "65%",
                    "中性": "25%",
                    "消极": "10%"
                }
            },
            {
                "title": "关键主题",
                "content": "您最常讨论的主题包括：技术、学习、工作等。"
            }
        ]
    
    elif report_type == "情绪分析":
        report_data["sections"] = [
            {
                "title": "情绪分布",
                "content": "根据对话内容分析的情绪分布...",
                "data": {
                    "快乐": 45,
                    "平静": 30,
                    "兴奋": 15,
                    "焦虑": 8,
                    "沮丧": 2
                }
            },
            {
                "title": "情绪变化趋势",
                "content": "近一个月的情绪变化呈现上升趋势。"
            }
        ]
    
    elif report_type == "关键词分析":
        report_data["sections"] = [
            {
                "title": "高频词汇",
                "content": "您最常使用的词汇...",
                "data": {
                    "技术": 89,
                    "学习": 67,
                    "项目": 54,
                    "思考": 43,
                    "分享": 32
                }
            },
            {
                "title": "话题聚类",
                "content": "主要话题集中在技术开发、个人成长等方面。"
            }
        ]
    
    else:  # 对话统计
        report_data["sections"] = [
            {
                "title": "对话量统计",
                "content": "对话活跃度分析...",
                "data": {
                    "本周": 45,
                    "上周": 38,
                    "本月": 156,
                    "总计": 892
                }
            },
            {
                "title": "对话时段",
                "content": "您最活跃的时段是晚上 20:00-23:00"
            }
        ]
    
    return report_data


def export_report(report_data: dict, format: str, filename: str):
    """导出报告"""
    
    export_dir = Path("./data/reports")
    export_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        if format == "Markdown (.md)":
            output_path = export_dir / f"{filename}.md"
            content = export_to_markdown(report_data, str(output_path))
            
            st.success(f"✅ 已导出到: {output_path}")
            st.download_button(
                "📥 下载 Markdown",
                data=content,
                file_name=f"{filename}.md",
                mime="text/markdown"
            )
        
        elif format == "HTML (.html)":
            output_path = export_dir / f"{filename}.html"
            content = export_to_html(report_data, str(output_path))
            
            st.success(f"✅ 已导出到: {output_path}")
            st.download_button(
                "📥 下载 HTML",
                data=content,
                file_name=f"{filename}.html",
                mime="text/html"
            )
        
        elif format == "PDF (.pdf)":
            output_path = export_dir / f"{filename}.pdf"
            success = export_to_pdf(report_data, str(output_path))
            
            if success:
                st.success(f"✅ 已导出到: {output_path}")
                with open(output_path, 'rb') as f:
                    st.download_button(
                        "📥 下载 PDF",
                        data=f.read(),
                        file_name=f"{filename}.pdf",
                        mime="application/pdf"
                    )
            else:
                st.error("❌ PDF 导出失败，请确保已安装 wkhtmltopdf")
                st.info("您可以先导出为 HTML，然后在浏览器中打印为 PDF")
    
    except Exception as e:
        st.error(f"导出失败: {str(e)}")
