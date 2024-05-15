
from dataclasses import dataclass
import httpx
from schema import GoogleUserDataSchema

from settings import Settings


@dataclass
class GoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> dict:
        access_token = await self._get_access_token(code=code)
        
        async with self.async_client as client:
            user_info = await client.get(
                url="https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )

        return GoogleUserDataSchema(**user_info.json(), access_token=access_token)


    async def _get_access_token(self, code: str) -> str:
        data = {
            'code': code,
            'client_id': self.settings.GOOGLE_CLIENT_ID,
            'client_secret': self.settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': self.settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }

        async with self.async_client as client:
            response = await client.post(
                self.settings.GOOGLE_TOKEN_URI,
                data=data
            )

            print(response)

        return response

