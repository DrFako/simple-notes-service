from datetime import datetime
from threading import Lock
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

from app.models import Note, NoteCreate, NoteUpdate

router = APIRouter(prefix="/api/notes", tags=["notes"])

# In-memory (thread-safe) notes store
db: dict[UUID, Note] = {}
db_lock = Lock()


@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
def create_note(note_in: NoteCreate):
    note = Note(
        id=uuid4(),
        title=note_in.title,
        content=note_in.content,
        created_at=datetime.utcnow(),
    )
    with db_lock:
        db[note.id] = note
    return note


@router.get("/", response_model=list[Note])
def list_notes():
    with db_lock:
        return list(db.values())


@router.get("/{note_id}", response_model=Note)
def get_note(note_id: UUID):
    with db_lock:
        note = db.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=Note)
def update_note(note_id: UUID, note_in: NoteUpdate):
    with db_lock:
        note = db.get(note_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        data = note.model_dump()
        if note_in.title is not None:
            if not note_in.title.strip():
                raise HTTPException(status_code=400, detail="Title must be a non-empty string")
            data["title"] = note_in.title
        if note_in.content is not None:
            data["content"] = note_in.content
        updated = Note(**data)
        db[note_id] = updated
    return updated


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: UUID):
    with db_lock:
        if note_id not in db:
            raise HTTPException(status_code=404, detail="Note not found")
        del db[note_id]
    return None
