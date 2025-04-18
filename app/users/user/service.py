
from dataclasses import dataclass

from app.users.user.repository import UserRepository

from app.users.user.schema import UserLoginSchema
from app.users.auth.service import AuthService


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, username: str, password: str) -> UserLoginSchema:
        user = await self.user_repository.create_user(username=username, password=password)
        access_token = await self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
    
