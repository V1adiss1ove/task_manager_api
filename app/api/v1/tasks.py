from typing import Annotated

from fastapi import APIRouter, Query, status

from app.api.deps import CurrUserDep
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task import TaskServiceDep

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("/", response_model=list[TaskResponse])
async def list_tasks(
    service: TaskServiceDep,
    current: CurrUserDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    is_completed: bool | None = None,
):
    return await service.list(
        user_id=current.id,
        skip=skip,
        limit=limit,
        is_completed=is_completed,
    )


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    service: TaskServiceDep,
    current: CurrUserDep,
    payload: TaskCreate,
):
    return await service.create(data=payload, user_id=current.id)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(service: TaskServiceDep, current: CurrUserDep, task_id: int):
    return await service.get(task_id=task_id, user_id=current.id)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    service: TaskServiceDep,
    current: CurrUserDep,
    payload: TaskUpdate,
    task_id: int,
):
    return await service.update(data=payload, task_id=task_id, user_id=current.id)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    service: TaskServiceDep,
    current: CurrUserDep,
    task_id: int,
):
    return await service.delete(task_id=task_id, user_id=current.id)
