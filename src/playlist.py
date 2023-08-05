import datetime

import isodate

from src.channel import APIMixin


class PlayList(APIMixin):
    def __init__(self, playlist_id: str):
        self.__playlist_id: str = playlist_id
        self.__playlist_info: dict = self._fetch_playlist_info()
        self.__playlist_videos = self._fetch_playlist_videos()
        self.__title: str = self.__playlist_info['items'][0]['snippet']['title']

    @property
    def playlist_id(self):
        return self.__playlist_id

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def video_ids(self) -> list[str]:
        return [video['contentDetails']['videoId'] for video in self.__playlist_videos['items']]

    def get_video_response(self):
        return self.get_service().videos().list(part='contentDetails,statistics',
                                                id=','.join(self.video_ids)
                                                ).execute()

    @property
    def total_duration(self) -> datetime.timedelta:
        video_response = self.get_video_response()
        total_duration = datetime.timedelta()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)

            total_duration += duration

        return total_duration

    def _fetch_playlist_info(self) -> dict:
        return self.get_service().playlists().list(id=self.playlist_id,
                                                   part='contentDetails,snippet',
                                                   maxResults=50,
                                                   ).execute()

    def _fetch_playlist_videos(self):
        return self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

    def show_best_video(self) -> str:
        video_response = self.get_video_response()

        videos_best_sorted = sorted(video_response['items'], key=lambda el: el['statistics']['likeCount'], reverse=True)
        url = f'https://youtu.be/{videos_best_sorted[0]["id"]}'

        return url
