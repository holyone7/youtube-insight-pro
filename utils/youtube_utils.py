import os
from googleapiclient.discovery import build
import pandas as pd

API_KEY = os.environ.get('YOUTUBE_API_KEY', '') or os.environ.get('YOUTUBE_API_KEY', '')

def _build_client():
    if not API_KEY:
        return None
    return build('youtube', 'v3', developerKey=API_KEY)

def get_channel_stats(channel_id):
    youtube = _build_client()
    if youtube is None:
        raise ValueError('YouTube API client not initialized. Set YOUTUBE_API_KEY in env or Streamlit secrets.')
    res = youtube.channels().list(part='snippet,statistics', id=channel_id).execute()
    if 'items' not in res or len(res['items']) == 0:
        raise ValueError('Channel not found or API key/quotas issue.')
    data = res['items'][0]
    stats = {
        'Channel Name': data['snippet'].get('title'),
        'Subscribers': int(data['statistics'].get('subscriberCount', 0)),
        'Total Views': int(data['statistics'].get('viewCount', 0)),
        'Videos': int(data['statistics'].get('videoCount', 0))
    }
    return stats

def get_video_stats(channel_id, max_results=10):
    youtube = _build_client()
    if youtube is None:
        raise ValueError('YouTube API client not initialized. Set YOUTUBE_API_KEY in env or Streamlit secrets.')
    uploads_res = youtube.channels().list(part='contentDetails', id=channel_id).execute()
    if 'items' not in uploads_res or len(uploads_res['items']) == 0:
        return pd.DataFrame([])
    uploads_id = uploads_res['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    videos = []
    next_page_token = None
    while len(videos) < max_results:
        req = youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_id,
            maxResults=min(50, max_results - len(videos)),
            pageToken=next_page_token
        )
        res = req.execute()
        for item in res.get('items', []):
            vid = item['snippet']['resourceId']['videoId']
            title = item['snippet']['title']
            pub = item['snippet'].get('publishedAt')
            stats_res = youtube.videos().list(part='statistics', id=vid).execute()
            stats = stats_res['items'][0].get('statistics', {}) if stats_res.get('items') else {}
            videos.append({
                'Title': title,
                'Published': pub,
                'Views': int(stats.get('viewCount', 0)),
                'Likes': int(stats.get('likeCount', 0)),
                'Comments': int(stats.get('commentCount', 0))
            })
        next_page_token = res.get('nextPageToken')
        if not next_page_token:
            break
    return pd.DataFrame(videos[:max_results])
