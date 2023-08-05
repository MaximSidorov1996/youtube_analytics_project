import json
import os

from googleapiclient.discovery import build


class APIMixin:
    """Класс-миксин для предоставления доступа к API."""

    __API_KEY: str = os.getenv('YT_API_KEY')

    @classmethod
    def get_service(cls) -> build:
        """Возвращает объект для работы с API youtube."""
        service = build('youtube', 'v3', developerKey=cls.__API_KEY)
        return service


class Channel(APIMixin):
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id: str = channel_id
        self.__channel_info: dict = self._fetch_channel_info()
        self.__title: str = self.__channel_info['items'][0]['snippet']['title']
        self.__description: str = self.__channel_info['items'][0]['snippet']['description']
        self.__subscriptions: int = int(self.__channel_info['items'][0]['statistics']['subscriberCount'])
        self.__video_count: int = int(self.__channel_info['items'][0]['statistics']['videoCount'])
        self.__view_count: int = int(self.__channel_info['items'][0]['statistics']['viewCount'])

    def __str__(self):
        return f'{self.__title} ({self.url})'

    def __add__(self, other):
        if isinstance(other, Channel):
            return self.__subscriptions + other.__subscriptions
        else:
            raise TypeError("Unsupported operand type. Can only concatenate Channel objects.")

    def __sub__(self, other):
        if isinstance(other, Channel):
            return self.__subscriptions - other.__subscriptions
        else:
            raise TypeError("Unsupported operand type. Can only concatenate Channel objects.")

    def __gt__(self, other):
        if isinstance(other, Channel):
            return self.__subscriptions > other.__subscriptions
        else:
            raise TypeError("Unsupported operand type. Can only concatenate Channel objects.")

    def __lt__(self, other):
        if isinstance(other, Channel):
            return self.__subscriptions < other.__subscriptions
        else:
            raise TypeError("Unsupported operand type. Can only concatenate Channel objects.")

    def __ge__(self, other):
        if isinstance(other, Channel):
            return self.__subscriptions >= other.__subscriptions
        else:
            raise TypeError("Unsupported operand type. Can only concatenate Channel objects.")

    def __le__(self, other):
        if isinstance(other, Channel):
            return self.__subscriptions <= other.__subscriptions
        else:
            raise TypeError("Unsupported operand type. Can only concatenate Channel objects.")

    def __eq__(self, other):
        if isinstance(other, Channel):
            return self.__subscriptions == other.__subscriptions
        else:
            raise TypeError("Unsupported operand type. Can only concatenate Channel objects.")

    @property
    def url(self):
        return f'https://www.youtube.com/channel/{self.__channel_id}'

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        return self.__title

    @property
    def description(self):
        return self.__description

    @property
    def subscriptions(self):
        return self.__subscriptions

    @property
    def video_count(self):
        return self.__video_count

    @property
    def view_count(self):
        return self.__view_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.__channel_info, indent=2, ensure_ascii=False))

    def _fetch_channel_info(self) -> dict:
        return self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()

    def to_json(self, filename: str) -> None:
        """
        Метод сохраняющий в файл значения атрибутов экземпляра Channel
        """
        with open(filename, 'w') as file:
            data_dict = self.__dict__
            del data_dict['_Channel__channel_info']
            data_dict['_Channel__url'] = self.url

            json.dump(data_dict, file, ensure_ascii=False)
