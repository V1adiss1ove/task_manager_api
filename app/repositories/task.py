from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import SessionDep
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, task_id: int, user_id: int) -> Task | None:
        """Возвращает задачу, только если она принадлежит user_id."""

        result = await self.session.execute(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        is_completed: bool | None = None,
    ) -> list[Task]:

        stmt = select(Task).where(Task.user_id == user_id)
        if is_completed is not None:
            stmt = stmt.where(Task.is_completed == is_completed)

        stmt = stmt.order_by(Task.created_at.desc()).offset(skip).limit(limit)
        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def create(self, data: TaskCreate, user_id: int) -> Task:
        task = Task(name=data.name, description=data.description, user_id=user_id)

        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def update(self, task: Task, data: TaskUpdate) -> Task:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def delete(self, task: Task) -> None:
        await self.session.delete(task)
        await self.session.commit()


async def get_task_repository(session: SessionDep) -> TaskRepository:
    return TaskRepository(session)


TaskRepoDep = Annotated[TaskRepository, Depends(get_task_repository)]
