from typing import Annotated
from dependecy import get_user_service
from fastapi import APIRouter, status, Depends
from schema import UserCreateSchema, UserLoginSchema
from service import UserService


router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserLoginSchema, status_code=status.HTTP_201_CREATED)
async def create_user(body: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    return user_service.create_user(username=body.username, password=body.password)
    