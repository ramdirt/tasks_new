
from dataclasses import dataclass
import requests
from schema import YandexUserDataSchema

from settings import Settings


@dataclass
class YandexClient:
    settings: Settings

    def get_user_info(self, code: str):
        access_token = self._get_access_token(code=code)
        user_info = requests.get(
            url="https://login.yandex.ru/info?format=json",
            headers={"Authorization": f"OAuth {access_token}"}
        )
        
        return YandexUserDataSchema(**user_info.json(), access_token=access_token)



    def _get_access_token(self, code: str) -> str:


        response = requests.post(
            self.settings.YANDEX_TOKEN_URI,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': self.settings.YANDEX_CLIENT_ID,
                'client_secret': self.settings.YANDEX_CLIENT_SECRET,
            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )

        return response.json()['access_token']