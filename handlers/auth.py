from typing import Annotated
from dependecy import get_auth_service
from exception import UserNotCorrentPasswordException, UserNotFoundException
from fastapi import APIRouter, status, Depends, HTTPException
from schema import UserCreateSchema, UserLoginSchema
from service import AuthService
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserLoginSchema)
async def login(body: UserCreateSchema, auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    
    try:
        return auth_service.login(body.username, body.password)
    
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )
    
    except UserNotCorrentPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )
    

@router.get(
    "/login/google",
    response_class=RedirectResponse,
)
async def google_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(url=redirect_url)


@router.get(
    "/google"
)
async def google_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str
):
    return auth_service.google_auth(code=code)


@router.get(
    "/login/yandex",
    response_class=RedirectResponse,
)
async def yandex_login(
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
):
    redirect_url = auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(url=redirect_url)


@router.get(
    "/yandex"
)
async def yandex_auth(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    code: str
):
    return auth_service.yandex_auth(code=code)