
from dataclasses import dataclass
import requests
from schema import GoogleUserDataSchema

from settings import Settings


@dataclass
class GoogleClient:
    settings: Settings

    def get_user_info(self, code: str) -> dict:
        access_token = self._get_access_token(code=code)
        user_info = requests.get(
            url="https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        return GoogleUserDataSchema(**user_info.json(), access_token=access_token)


    def _get_access_token(self, code: str) -> str:
        data = {
            'code': code,
            'client_id': self.settings.GOOGLE_CLIENT_ID,
            'client_secret': self.settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': self.settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }

        response = requests.post(
            self.settings.GOOGLE_TOKEN_URI,
            data=data
        )

        return response.json()['access_token']