
from dataclasses import dataclass
from app.settings import Settings
import pytest
import httpx

@dataclass
class FakeGoogleClient():
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> dict:
        access_token = self._get_access_token(code=code)
        return {
            "access_token": access_token
        }

    async def _get_access_token(self, code: str) -> str:
        return f"fake_access_token {code}"

@dataclass
class FakeYandexClient():
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> dict:
        access_token = self._get_access_token(code=code)
        return {
            "access_token": access_token
        }
    
    async def _get_access_token(self, code: str) -> str:
            return f"fake_access_token {code}"


@pytest.fixture
def google_client():
    return FakeGoogleClient(settings=Settings(), async_client=httpx.AsyncClient())

@pytest.fixture
def yandex_client():
    return FakeYandexClient(settings=Settings(), async_client=httpx.AsyncClient())