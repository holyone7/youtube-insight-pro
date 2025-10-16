from fpdf import FPDF
from datetime import datetime
import os

def create_pdf_report(channel_stats, df_videos, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "YouTube 채널 분석 보고서", ln=True, align="C")
    pdf.ln(8)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Generated: {datetime.utcnow().isoformat()} UTC", ln=True)
    pdf.ln(6)

    for k, v in channel_stats.items():
        pdf.cell(0, 8, f"{k}: {v}", ln=True)
    pdf.ln(6)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 8, "최근 영상 통계", ln=True)
    pdf.set_font("Arial", '', 12)
    for i, row in df_videos.iterrows():
        title = str(row.get('Title', ''))[:120]
        pdf.multi_cell(0, 6, f"{i+1}. {title}")
        pdf.multi_cell(0, 6, f"   Published: {row.get('Published')} | Views: {row.get('Views')} | Likes: {row.get('Likes')} | Comments: {row.get('Comments')}")
        pdf.ln(1)

    out_path = os.path.join(os.getcwd(), filename)
    pdf.output(out_path)
    return out_path
