from clients import GoogleClient, YandexClient
from exception import TokenExpireException, TokenNotCorrectException
from fastapi import Depends, Request, security, Security, HTTPException, status
from database import get_db_session
from cache import get_redis_connection
from repository import TaskRepository, TaskCache, UserRepository
from service import TaskService, UserService, AuthService
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from settings import Settings


# Tasks
async def get_tasks_repository(
        db_session: AsyncSession = Depends(get_db_session)
) -> TaskRepository:
    return TaskRepository(
        db_session=db_session
)


async def get_tasks_cache_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)

async def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        task_cache: TaskCache = Depends(get_tasks_cache_repository)
) -> TaskService:
    return TaskService(task_repository=task_repository, task_cache=task_cache)


async def get_users_repository(db_session: AsyncSession = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_google_client(
        async_client: httpx.AsyncClient = Depends(get_async_client)
) -> GoogleClient:
    return GoogleClient(
        settings=Settings(),
        async_client=async_client
    )


async def get_yandex_client(
    async_client: httpx.AsyncClient = Depends(get_async_client)
) -> YandexClient:
    return YandexClient(
        settings=Settings(),
        async_client=async_client
    )


async def get_auth_service(
        user_repository: UserRepository = Depends(get_users_repository),
        google_client: GoogleClient = Depends(get_google_client),
        yandex_client: YandexClient = Depends(get_yandex_client)
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        google_client=google_client,
        yandex_client=yandex_client,
        settings=Settings()
    )


async def get_user_service(
        user_repository: UserRepository = Depends(get_users_repository),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service
    )

reusable_oauth2 = security.HTTPBearer()

async def get_request_user_id(
        auth_service: AuthService = Depends(get_auth_service),
        token: security.HTTPAuthorizationCredentials = Security(reusable_oauth2)
) -> int:
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)

    except TokenExpireException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )
    
    except TokenNotCorrectException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )

    return user_id



