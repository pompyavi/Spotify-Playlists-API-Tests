import json
from config import BASE_URI, PLAYLIST_ENDPOINTS
from tests.utils.token_manager import TokenManager
from utils.request import APIRequest


class Playlist:
    def __init__(self, name=None, description=None, is_public=None):
        self.request = APIRequest()
        self.base_uri = BASE_URI
        self.playlist_endpoints = PLAYLIST_ENDPOINTS
        self.__name = name
        self.__description = description
        self.__is_public = is_public
        self.headers = {
            'Authorization': f'Bearer {TokenManager.get_token()}'
        }

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name
        return self

    def get_description(self):
        return self.__description

    def set_description(self, description):
        self.__description = description
        return self

    def get_is_public(self):
        return self.__is_public

    def set_is_public(self, is_public):
        self.__is_public = is_public
        return self

    def create_playlist(self, access_token='valid'):
        if access_token != 'valid':
            self.headers.update({'Authorization': f'Bearer invalid'})

        return self.__create_new_playlist()

    def get_playlist(self, playlist_id):
        return self.request.get(url=self.base_uri + self.playlist_endpoints['get_playlist'].format(playlist_id),
                                headers=self.headers)

    def update_playlist(self, playlist_id):
        payload = {
            'name': 'Test Name',
            'description': 'New description setting through test script',
            'public': False
        }

        return self.request.put(url=self.base_uri + self.playlist_endpoints['update_playlist'].format(playlist_id),
                                headers=self.headers, payload=json.dumps(payload))

    def __create_new_playlist(self):
        payload = {
            'name': self.__name,
            'description': self.__description,
            'public': self.__is_public
        }
        response = self.request.post(url=self.base_uri + self.playlist_endpoints['create_playlist'],
                                     headers=self.headers, payload=payload)
        return response
