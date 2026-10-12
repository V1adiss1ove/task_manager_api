from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.models.task import Task
from app.repositories.task import TaskRepoDep, TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def list(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        is_completed: bool | None = None,
    ) -> list[Task]:
        return await self.repo.list(
            user_id=user_id, skip=skip, limit=limit, is_completed=is_completed
        )

    async def get(self, task_id: int, user_id: int) -> Task:
        task = await self.repo.get(task_id=task_id, user_id=user_id)

        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        return task

    async def create(self, data: TaskCreate, user_id: int) -> Task:
        return await self.repo.create(data=data, user_id=user_id)

    async def update(self, data: TaskUpdate, task_id: int, user_id: int):
        task = self.repo.get(task_id=task_id, user_id=user_id)
        return await self.repo.update(task=task, data=data)

    async def delete(self, task_id: int, user_id: int) -> None:
        task = await self.repo.get(task_id=task_id, user_id=user_id)
        await self.repo.delete(task=task)


async def get_task_service(repo: TaskRepoDep) -> TaskService:
    return TaskService(repo)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
