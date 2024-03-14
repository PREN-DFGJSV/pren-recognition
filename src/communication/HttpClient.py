import string
import requests
from src.model.BaseDto import BaseDto


class HttpClient:
    def __init__(self, url: string, auth: string):
        self.url = url
        self.auth = auth

    def post_dto(self, dto: BaseDto) -> string:
        result = requests.post(url=self.url, auth=self.auth, json=dto.to_json())
        return result.status_code
