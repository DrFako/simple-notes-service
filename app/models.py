from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Note(BaseModel):
    id: UUID
    title: str
    content: str | None = None
    created_at: datetime
