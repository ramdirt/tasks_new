
from dataclasses import dataclass
from clients import GoogleClient
from exception import TokenExpireException, TokenNotCorrectException, UserNotCorrentPasswordException, UserNotFoundException
from models import User
from repository import UserRepository
from jose import jwt, JWTError
import datetime as dt
from datetime import timedelta 

from schema import UserLoginSchema, GoogleUserDataSchema
from schema.user import UserCreateSchema
from settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    

    def login(self, username: str, password: str) -> UserLoginSchema:

        user = self.user_repository.get_user_by_username(username)

        self._validate_auth_user(user, password)
        access_token = self.generate_access_token(user_id=user.id)
        
        return UserLoginSchema(user_id=user.id, access_token=access_token)
    
    @staticmethod
    def _validate_auth_user(user: User, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrentPasswordException
        

    def generate_access_token(self, user_id: int) -> str:
        expire_date_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode(
            {
                'user_id': user_id,
                'expire': expire_date_unix
            },
            self.settings.JWT_SECRET_KEY,
            algorithm=self.settings.JWT_ALGORITHM
        )
        
        return token


    def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(access_token, self.settings.JWT_SECRET_KEY, algorithms=[self.settings.JWT_ALGORITHM])
        except JWTError:
            raise TokenNotCorrectException
        
        if payload['expire'] < dt.datetime.utcnow().timestamp():
            raise TokenExpireException

        return payload['user_id']
    

    def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url()
    

    def google_auth(self, code: str):
        user_data = self.google_client.get_user_info(code=code)

        if user := self.user_repository.get_user_by_email(email=user_data.email):
            access_token = self.generate_access_token(user_id=user.id)
            print("user login")
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            google_access_token=user_data.access_token,
            email=user_data.email,
            name=user_data.name
        )
        create_user = self.user_repository.create_user(user=create_user_data)
        access_token = self.generate_access_token(user_id=create_user.id)
        print("new user")
        return UserLoginSchema(user_id=create_user.id, access_token=access_token)