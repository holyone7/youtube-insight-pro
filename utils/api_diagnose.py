from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import streamlit as st

def test_youtube_api_key():
    """YouTube API Key 유효성 테스트"""
    api_key = st.secrets.get("YOUTUBE_API_KEY", None)

    st.header("🔍 YouTube API Key 자동 진단")

    if not api_key:
        st.error("❌ YOUTUBE_API_KEY가 secrets.toml에 없습니다.")
        st.info("예시: YOUTUBE_API_KEY = 'AIzaSyAxxxxx'")
        return

    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.search().list(part="snippet", q="streamlit tutorial", maxResults=1)
        response = request.execute()

        st.success("✅ API Key 정상 작동 중입니다!")
        st.write("예시 검색 결과:", response["items"][0]["snippet"]["title"])

    except HttpError as e:
        st.error(f"❌ API 호출 오류: {e._get_reason()}")
    except Exception as e:
        st.error(f"⚠️ 예기치 못한 오류: {e}")
