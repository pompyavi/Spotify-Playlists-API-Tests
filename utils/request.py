from dataclasses import dataclass

import allure
import requests
from requests import JSONDecodeError


@dataclass
class Response:
    status_code: int
    text: str
    as_dict: object
    headers: dict


class APIRequest:

    def get(self, url, headers=None, params=None):
        response = requests.get(url=url, headers=headers, params=params)
        allure.attach(name="Request url", body=str(response.request.url), attachment_type=allure.attachment_type.TEXT)
        allure.attach(name="Request headers", body=str(response.request.headers),
                      attachment_type=allure.attachment_type.TEXT)
        return self.__get_response(response)

    def post(self, url, payload=None, headers=None):
        response = requests.post(url, json=payload, headers=headers)
        allure.attach(name="Request url", body=str(response.request.url), attachment_type=allure.attachment_type.TEXT)
        allure.attach(name="Request body", body=str(response.request.body), attachment_type=allure.attachment_type.TEXT)
        allure.attach(name="Request headers", body=str(response.request.headers), attachment_type=allure.attachment_type.TEXT)
        return self.__get_response(response)

    def get_access_token(self, url, data=None, headers=None):
        response = requests.post(url, data=data, headers=headers)
        return self.__get_response(response)

    def put(self, url, payload=None, headers=None):
        response = requests.put(url, data=payload, headers=headers)
        return self.__get_response(response)

    @staticmethod
    def __get_response(response):
        status_code = response.status_code
        text = response.text
        try:
            as_dict = response.json()
        except JSONDecodeError as err:
            as_dict = {}

        headers = response.headers

        return Response(
            status_code, text, as_dict, headers
        )
