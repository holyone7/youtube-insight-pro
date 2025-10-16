import os
import streamlit as st
from utils.report_generator import create_pdf_report
from utils.youtube_utils import get_channel_stats, get_video_stats
from utils.stripe_handler import start_checkout
from utils.api_diagnose import test_youtube_api_key

st.set_page_config(page_title="YouTube Insight Pro v2", page_icon="🎥", layout="wide")
st.title("🎬 YouTube Insight Pro v2")

menu = st.sidebar.radio("메뉴", ["YouTube 분석", "PDF 리포트", "API Key 진단"])

if menu == "API Key 진단":
    test_youtube_api_key()

if menu == "YouTube 분석":
    channel_id = st.text_input("분석할 YouTube 채널 ID 입력 (예: UC_x5XG1OV2P6uZZ5FSM9Ttw)")
    if st.button("데이터 분석 시작") and channel_id:
        with st.spinner("데이터 수집 중..."):
            try:
                stats = get_channel_stats(channel_id)
                df_videos = get_video_stats(channel_id, max_results=10)
            except Exception as e:
                st.error(f"데이터 수집 실패: {e}")
                st.stop()

        st.subheader("📊 채널 요약")
        st.json(stats)
        st.subheader("최근 영상 통계")
        st.dataframe(df_videos)

if menu == "PDF 리포트":
    st.write("PDF 리포트 생성 (데모)")
    channel_id = st.text_input("보고서용 채널 ID 입력")
    if st.button("샘플 리포트 생성") and channel_id:
        try:
            stats = get_channel_stats(channel_id)
            df_videos = get_video_stats(channel_id, max_results=5)
            out = create_pdf_report(stats, df_videos, filename=f"report_{channel_id}.pdf")
            st.success(f"PDF 생성 완료: {out}")
            with open(out, "rb") as f:
                st.download_button("Download PDF", data=f, file_name=os.path.basename(out), mime='application/pdf')
        except Exception as e:
            st.error(f"리포트 생성 실패: {e}")
