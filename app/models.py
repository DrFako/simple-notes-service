from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Note(BaseModel):
    id: UUID
    title: str
    content: str | None = None
    created_at: datetime


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1)
    content: str | None = None


class NoteUpdate(BaseModel):
    title: str | None = Field(None, min_length=1)
    content: str | None = None
