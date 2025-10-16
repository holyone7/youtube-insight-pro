import os
import streamlit as st
from youtube_service import get_channel_stats, get_video_stats
from report_generator import create_pdf_report
from stripe_checkout import start_checkout, verify_checkout_session
from dotenv import load_dotenv
from utils.report_generator import generate_pdf_report
from utils.youtube_utils import get_channel_stats
from utils.stripe_handler import handle_payment
from googleapiclient.discovery import build

load_dotenv()  # loads .env in working dir for local testing

# --- Sidebar Navigation ---
menu = st.sidebar.radio("메뉴 선택", ["YouTube 분석", "리포트 생성", "API Key 진단"])

if menu == "API Key 진단":
    from utils.api_diagnose import test_youtube_api_key
    test_youtube_api_key()
 # ---   
st.set_page_config(page_title="YouTube Insight Pro", page_icon="🎥", layout="wide")
st.title("🎬 YouTube Insight Pro")
st.write("AI 기반 YouTube 채널 분석 및 자동 보고서 생성 서비스 (데모)")

st.sidebar.header("설정 (로컬 테스트)")
if "STRIPE_PUBLISHABLE_KEY" in os.environ:
    st.sidebar.write("Stripe 설정이 감지됨 — 실제 결제 흐름 테스트 가능")
else:
    st.sidebar.write("환경변수에 Stripe/YouTube 키를 넣어주세요 (.env) - 로컬에서는 결제 링크가 시뮬레이션 됩니다")

channel_id = st.text_input("분석할 YouTube 채널 ID를 입력하세요 (예: UC_x5XG1OV2P6uZZ5FSM9Ttw)")

if st.button("데이터 분석 시작") and channel_id:
    with st.spinner("YouTube 데이터 수집 중..."):
        try:
            stats = get_channel_stats(channel_id)
            df_videos = get_video_stats(channel_id, max_results=10)
        except Exception as e:
            st.error(f"데이터 수집 실패: {e}")
            raise

    st.subheader("📊 채널 요약 정보")
    st.json(stats)
    st.subheader("최근 영상 통계")
    st.dataframe(df_videos)

    st.subheader("💡 성장 분석 인사이트 (간단)")
    if not df_videos.empty:
        top_video = df_videos.loc[df_videos['Views'].idxmax()]
        st.success(f"가장 인기 있는 영상: {top_video['Title']} ({int(top_video['Views'])}회 조회수)")
    else:
        st.info("분석 가능한 영상 데이터가 없습니다.")

    st.markdown("---")
    st.write("**보고서 생성 / 결제**")
    price_usd = 50
    st.write(f"보고서 가격: ${price_usd}")
    if st.button("PDF 보고서 생성 (결제 후 다운로드)"):
        # start checkout - returns URL or simulated URL
        try:
            checkout_url = start_checkout(channel_id, unit_amount=int(price_usd*100))
            st.markdown(f"[결제 페이지로 이동하기]({checkout_url})")
            st.info("결제 성공 후 Stripe의 success_url로 돌아오면 체크아웃 세션을 확인하고 보고서 발행을 구현하세요.")
        except Exception as e:
            st.error(f"결제 처리 오류: {e}")

st.markdown("---")
st.write("배포/설정 가이드: README.md를 참고하세요.")
