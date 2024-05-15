from dataclasses import dataclass
from exception import TaskNotFoundException
from repository import TaskRepository, TaskCache
from schema import TaskSchema, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    async def get_tasks(self) -> list[TaskSchema]:
        if tasks := await self.task_cache.get_tasks():
            return tasks
    
        tasks = await self.task_repository.get_tasks()
        tasks_schema = [TaskSchema.model_validate(task) for task in tasks]
        await self.task_cache.set_tasks(tasks_schema)

        return tasks
    

    async def get_task(self, task_id: int, user_id: int) -> TaskSchema:
        task = await self.task_repository.get_user_task(
            task_id=task_id,
            user_id=user_id
        )

        if not task:
            raise TaskNotFoundException

        task = await self.task_repository.get_task(task_id)

        return task
    

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        task_id = await self.task_repository.create_task(task=task, user_id=user_id)

        return await self.get_task(task_id=task_id, user_id=user_id)

    
    async def delete_task(self, task_id: int, user_id: int):
        task = await self.task_repository.get_user_task(
            task_id=task_id,
            user_id=user_id
        )

        if not task:
            raise TaskNotFoundException

        await self.task_repository.delete_task(task_id)


    async def update_task(self, task_id: int, task_new_name: str, user_id: int) -> TaskSchema:
        task = await self.task_repository.get_user_task(
            task_id=task_id,
            user_id=user_id
        )

        if not task:
            raise TaskNotFoundException
        
        task = await self.task_repository.update_name(task_id, name=task_new_name)
        
        return task
    
