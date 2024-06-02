from googleapiclient.discovery import build
import scrapper
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("YT_API")

def search_videos(query, max_results=3, lang='english'):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    query += ' review'
    if lang == 'arabic':
        query += ' بالعربية'
    elif lang == 'french':
        query += ' en français'
    

    search_response = youtube.search().list(
        q=query + ' review',
        part='id,snippet',
        maxResults=max_results
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
            video_title = search_result['snippet']['title']
            video_link = 'https://www.youtube.com/watch?v=' + video_id
            thumbnail_url = search_result['snippet']['thumbnails']['high']['url']
            videos.append({'title': video_title, 'link': video_link, 'thumbnail': thumbnail_url})


    return videos


def get_data(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    video_data = video_response.get('items', [])
    if not video_data:
        return None

    video = video_data[0]
    video_title = video['snippet']['title']
    video_link = 'https://www.youtube.com/watch?v=' + video_id
    thumbnail_url = video['snippet']['thumbnails']['high']['url']

    return [video_title, video_link, thumbnail_url]
    