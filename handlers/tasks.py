from typing import Annotated
from exception import TaskNotFoundException
from fastapi import APIRouter, status, Depends, HTTPException

from dependecy import get_task_service, get_request_user_id
from schema import TaskSchema, TaskCreateSchema

router = APIRouter(prefix="/tasks", tags=["tasks"])

task_service = Annotated[TaskSchema, Depends(get_task_service)]

@router.get("/", response_model=list[TaskSchema])
async def get_tasks(task_service: task_service):

    return await task_service.get_tasks()


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
    task_id: int,
    task_service: task_service,
    # user_id: int = Depends(get_request_user_id)
):

    try:
        return await task_service.get_task(task_id, user_id=7)
    
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.post("/", response_model=TaskSchema)
async def create_task(
    body: TaskCreateSchema,
    task_service: task_service,
    # user_id: int = Depends(get_request_user_id)
):
    return await task_service.create_task(body, user_id=7)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    task_service: task_service,
    # user_id: int = Depends(get_request_user_id)
):
    try:
        await task_service.delete_task(task_id=task_id, user_id=7)
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )


@router.patch("/{task_id}",response_model=TaskSchema)
async def update_task(
    task_id: int,
    task_new_name: str,
    task_service: task_service,
    # user_id: int = Depends(get_request_user_id)
):
    try:
        return await task_service.update_task(
            task_id=task_id,
            task_new_name=task_new_name,
            user_id=7
        )
    except TaskNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.detail
        )