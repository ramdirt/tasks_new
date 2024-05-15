from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from models import Task, Category
from schema.task import TaskCreateSchema

class TaskRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_tasks(self):
        query = select(Task)

        async with self.db_session as session:
            tasks: list[Task] = (await session.execute(query)).scalars().all()

        return tasks


    async def get_task(self, task_id: int) -> Task | None:
        query = select(Task).where(Task.id == task_id)

        async with self.db_session as session:
            task: Task = (await session.execute(query)).scalar_one_or_none()

        return task
    
    async def get_user_task(self, user_id: int, task_id: int) -> Task | None:
        query = select(Task).where(Task.user_id == user_id, Task.id == task_id)

        async with self.db_session as session:
            task: Task = (await session.execute(query)).scalar_one_or_none()

        return task

    

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        query = insert(Task).values(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            user_id=user_id).returning(Task.id)
        
        async with self.db_session as session:
            task_id = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return task_id


    async def delete_task(self, task_id: int) -> None:
        query = delete(Task).where(Task.id == task_id)

        async with self.db_session as session:
            await session.execute(query)
            await session.commit()


    def get_task_by_category_id(self, category_name: int) -> list[Task] | None:
        query = select(Task).join(Category, Task.category_id == Category.id).where(Task.category_name == category_name)

        with self.db_session() as session:
            tasks: list[Task] = session.execute(query).scalars().all()

        return tasks
    

    async def update_name(self, task_id: int, name: str) -> Task:
        query = update(Task).where(Task.id == task_id).values(name=name).returning(Task.id)
        
        async with self.db_session as session:
            task_id: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()

            return await self.get_task(task_id)

