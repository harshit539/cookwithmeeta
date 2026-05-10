import requests
from .models import Video
from datetime import datetime

API_KEY = "AIzaSyABbX5j4JdzdwlOHZ2onJzmbIfniR_htg8"
CHANNEL_ID = "UCsxsqnTx5nRsiWa4rSSbiFQ"

def fetch_videos():
    next_page_token = None

    while True:
        url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=50"

        if next_page_token:
            url += f"&pageToken={next_page_token}"

        response = requests.get(url).json()

        for item in response.get('items', []):
            if item['id']['kind'] == 'youtube#video':

                video_id = item['id']['videoId']
                title = item['snippet']['title']
                published_at = item['snippet']['publishedAt']
                thumbnail = item['snippet']['thumbnails']['high']['url']

                # category detect
                title_lower = title.lower()
                if "breakfast" in title_lower:
                    category = "Breakfast"
                elif "lunch" in title_lower:
                    category = "Lunch"
                elif "dessert" in title_lower:
                    category = "Dessert"
                else:
                    category = "Dinner"

                # fetch views
                stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={API_KEY}"
                stats_res = requests.get(stats_url).json()

                views = 0
                if stats_res.get('items'):
                    views = int(stats_res['items'][0]['statistics'].get('viewCount', 0))

                # save/update in DB
                Video.objects.update_or_create(
                    video_id=video_id,
                    defaults={
                        'title': title,
                        'category': category,
                        'views': views,
                        'thumbnail': thumbnail,
                        'published_at': datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    }
                )

        # next page
        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    print("✅ All videos fetched successfully!")