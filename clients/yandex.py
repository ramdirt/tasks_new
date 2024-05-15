
from dataclasses import dataclass
from schema import YandexUserDataSchema
import httpx


from settings import Settings


@dataclass
class YandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str):
        access_token = await self._get_access_token(code=code)
        user_info = await self.async_client.get(
            url="https://login.yandex.ru/info?format=json",
            headers={"Authorization": f"OAuth {access_token}"}
        )
        
        return YandexUserDataSchema(**user_info.json(), access_token=access_token)



    async def _get_access_token(self, code: str) -> str:


        response = await self.async_client.post(
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