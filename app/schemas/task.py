from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    """Что приходит при создании"""

    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)


class TaskUpdate(BaseModel):
    """Что приходит при обновлении. Все поля опциональны"""

    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    is_completed: bool | None = None


class TaskResponse(BaseModel):
    id: int
    name: str
    description: str | None
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
