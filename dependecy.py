from clients import GoogleClient
from exception import TokenExpireException, TokenNotCorrectException
from fastapi import Depends, Request, security, Security, HTTPException, status
from database import get_db_session
from cache import get_redis_connection
from repository import TaskRepository, TaskCache, UserRepository
from service import TaskService, UserService, AuthService
from sqlalchemy.orm import Session

from settings import Settings


# Tasks
def get_tasks_repository(db_session: Session = Depends(get_db_session)) -> TaskRepository:
    return TaskRepository(db_session=db_session)


def get_tasks_cache_repository() -> TaskCache:
    redis_connection = get_redis_connection()
    return TaskCache(redis_connection)

def get_task_service(
        task_repository: TaskRepository = Depends(get_tasks_repository),
        task_cache: TaskCache = Depends(get_tasks_cache_repository)
) -> TaskService:
    return TaskService(task_repository=task_repository, task_cache=task_cache)


def get_users_repository(db_session: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)


def get_google_client() -> GoogleClient:
    return GoogleClient(settings=Settings())


def get_auth_service(
        user_repository: UserRepository = Depends(get_users_repository),
        google_client: GoogleClient = Depends(get_google_client)
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        google_client=google_client,
        settings=Settings()
    )


def get_user_service(
        user_repository: UserRepository = Depends(get_users_repository),
        auth_service: AuthService = Depends(get_auth_service)
) -> UserService:
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service
    )

reusable_oauth2 = security.HTTPBearer()

def get_request_user_id(
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



