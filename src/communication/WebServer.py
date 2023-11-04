import string

import requests

from src.model.BaseDto import BaseDto


class WebServer:
    def __init__(self, url: string):
        # TODO: URL Validieren
        self.url = url

    def post_dto(self, dto: BaseDto) -> string:
        result = requests.post(url=self.url, json=dto.to_json())
        return result.status_code
