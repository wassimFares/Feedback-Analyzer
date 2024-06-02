import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("YT_API")


max_pages=1

def collect_data(video_id):
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = api_key

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    comments = []
    page_token = None

    for _ in range(max_pages):
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=10,
            pageToken=page_token
        )
        response = request.execute()

        comments.extend(response['items'])

        page_token = response.get('nextPageToken')
        if not page_token:
            break

    return comments
