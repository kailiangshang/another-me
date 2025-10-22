"""
报告导出工具 - 支持 Markdown、PDF、HTML
"""

from typing import Dict, Any
from pathlib import Path
from datetime import datetime
import markdown
import pdfkit


def export_to_markdown(report_data: Dict[str, Any], output_path: str = None) -> str:
    """
    导出为 Markdown 格式
    
    Args:
        report_data: 报告数据
        output_path: 输出路径（可选）
        
    Returns:
        Markdown 内容
    """
    # 构建 Markdown 内容
    md_content = f"""# {report_data.get('title', '分析报告')}

**生成时间**: {report_data.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}

---

## 📊 报告摘要

{report_data.get('summary', '暂无摘要')}

---

## 📈 详细数据

"""
    
    # 添加各个部分
    sections = report_data.get('sections', [])
    for section in sections:
        md_content += f"### {section.get('title', '未命名部分')}\n\n"
        md_content += f"{section.get('content', '')}\n\n"
        
        # 如果有数据表格
        if 'data' in section:
            md_content += "| 项目 | 值 |\n"
            md_content += "|------|----|\n"
            for key, value in section['data'].items():
                md_content += f"| {key} | {value} |\n"
            md_content += "\n"
    
    md_content += "---\n\n"
    md_content += f"*生成自 Another Me v0.4.0*\n"
    
    # 保存到文件
    if output_path:
        Path(output_path).write_text(md_content, encoding='utf-8')
    
    return md_content


def export_to_html(report_data: Dict[str, Any], output_path: str = None) -> str:
    """
    导出为 HTML 格式
    
    Args:
        report_data: 报告数据
        output_path: 输出路径（可选）
        
    Returns:
        HTML 内容
    """
    # 先生成 Markdown
    md_content = export_to_markdown(report_data)
    
    # 转换为 HTML
    html_body = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'codehilite']
    )
    
    # 完整的 HTML 文档
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_data.get('title', '分析报告')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Helvetica, Arial, sans-serif;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }}
        .container {{
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        h3 {{
            color: #7f8c8d;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #3498db;
            color: white;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ecf0f1;
            margin: 30px 0;
        }}
        .footer {{
            text-align: center;
            color: #95a5a6;
            font-size: 14px;
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_body}
        <div class="footer">
            <p><em>生成自 Another Me v0.4.0</em></p>
        </div>
    </div>
</body>
</html>"""
    
    # 保存到文件
    if output_path:
        Path(output_path).write_text(html_content, encoding='utf-8')
    
    return html_content


def export_to_pdf(report_data: Dict[str, Any], output_path: str) -> bool:
    """
    导出为 PDF 格式
    
    Args:
        report_data: 报告数据
        output_path: 输出路径
        
    Returns:
        是否成功
    """
    try:
        # 先生成 HTML
        html_content = export_to_html(report_data)
        
        # HTML 转 PDF
        options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': 'UTF-8',
            'enable-local-file-access': None
        }
        
        pdfkit.from_string(html_content, output_path, options=options)
        return True
    except Exception as e:
        print(f"PDF 导出失败: {e}")
        return False
