import string
import requests
from src.model.BaseDto import BaseDto


class HttpClient:
    def __init__(self, url: string, auth: string):
        self.url = url
        self.auth = auth
        self.auth_header = {'Auth': f'{self.auth}'}

    def post_dto(self, dto: BaseDto) -> int:
        result = requests.post(url=self.url, headers=self.auth_header, json=dto.to_json())
        return result.status_code

    def post(self) -> int:
        result = requests.post(url=self.url, headers=self.auth_header)
        return result.status_code
