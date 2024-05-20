from pydantic import BaseModel, Field

class GoogleUserDataSchema(BaseModel):
    id: int | None = None
    email: str | None = None
    varified_email: bool | None = None
    name: str | None = None
    access_token: str | None = None


class YandexUserDataSchema(BaseModel):
    id: int | None = None
    login: str | None = None
    name: str = Field(None, alias="real_name")
    default_email: str | None = None
    access_token: str | None = None
