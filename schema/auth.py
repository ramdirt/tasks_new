from pydantic import BaseModel

class GoogleUserDataSchema(BaseModel):
    id: int | None = None
    email: str | None = None
    varified_email: bool | None = None
    name: str | None = None
    access_token: str | None = None
