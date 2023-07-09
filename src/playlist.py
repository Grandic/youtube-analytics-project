import datetime
import os
import isodate
from src.channel import Channel

api_key: str = os.getenv('YT_API_KEY')


class PlayList:
    def __init__(self, playlist_id: str):
        self.youtube = Channel.get_service()
        self.playlist_id = playlist_id
        playlist_videos = self.youtube.playlists().list(id=self.playlist_id,
                                                        part='snippet',
                                                        maxResults=50,
                                                        ).execute()
        self.title = playlist_videos["items"][0]["snippet"]["title"]
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        total_dur = datetime.timedelta()
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_dur += duration

        return total_dur

    def show_best_video(self):
        like_count = "0"
        video_id = ""
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()
        for i in range(len(video_response['items'])):
            if video_response['items'][i]['statistics']['likeCount'] > like_count:
                like_count = video_response['items'][i]['statistics']['likeCount']
                video_id = f"https://youtu.be/{video_response['items'][i]['id']}"
        return video_id
