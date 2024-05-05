from dataclasses import dataclass
from models import User
from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from schema import UserCreateSchema

@dataclass
class UserRepository:
    db_session: Session


    def get_user_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)

        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()


    def create_user(self, user: UserCreateSchema) -> User:
        query = insert(User).values(**user.model_dump()).returning(User.id)

        with self.db_session() as session:
            user_id: int = session.execute(query).scalar()
            session.flush()
            session.commit()

            return self.get_user(user_id)
        

    def get_user(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)

        with self.db_session() as session:
            user: User = session.execute(query).scalar_one_or_none()

        return user
    
    
    def get_user_by_username(self, username: str) -> User | None:
        query = select(User).where(User.username == username)

        with self.db_session() as session:
            user: User = session.execute(query).scalar_one_or_none()

        return user