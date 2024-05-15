from dataclasses import dataclass
from models import User
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from schema import UserCreateSchema

@dataclass
class UserRepository:
    db_session: AsyncSession


    async def get_user_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)

        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()


    async def create_user(self, user: UserCreateSchema) -> User:
        query = insert(User).values(**user.model_dump()).returning(User.id)

        async with self.db_session as session:
            user_id: int = (await session.execute(query)).scalar()
            await session.flush()
            await session.commit()

            return await self.get_user(user_id)
        

    async def get_user(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)

        async with self.db_session as session:
            user: User = (await session.execute(query)).scalar_one_or_none()

        return user
    
    
    async def get_user_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)

        async with self.db_session as session:
            user: User = (await session.execute(query)).scalar_one_or_none()

        return user