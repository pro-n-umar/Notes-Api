from fastapi import APIRouter, Depends, HTTPException, Query
from app.auth import get_current_user
from app.database import notes_db, redis_client
from models import Note, NoteCreate, NoteUpdate
import uuid
import json
from typing import List, Optional
from datetime import datetime

router = APIRouter()

# Caching notes in Redis
async def get_cached_notes(username: str):
    cached = await redis_client.get(f"user_notes:{username}")
    return json.loads(cached) if cached else None

# Cache notes after fetching from the database
def cache_notes(username: str, notes: list):
    redis_client.setex(
        f"user_notes:{username}",
        300,  # 5 minute expiration
        json.dumps([note.dict() for note in notes])
    )

# Create a new note
@router.post("/Create_notes/", response_model=Note)
async def create_note(
    note: NoteCreate,
    username: str = Depends(get_current_user)
):
    note_id = str(uuid.uuid4())
    new_note = Note(
        id=note_id,
        value=note.value,
        owner=username,
        created_at=datetime.now(),
        tags=getattr(note, 'tags', [])  # Handle tags if they exist
    )
    notes_db[note_id] = new_note
    return new_note

# To read all notes for the current user with optional search
@router.get("/Read_notes/", response_model=List[Note])
async def read_notes(
    username: str = Depends(get_current_user),
    search: Optional[str] = Query(None, description="Search term to filter notes")
):
    # Get all notes for the user
    user_notes = [note for note in notes_db.values() if note.owner == username]
    
    # Apply search filter
    if search:
        search_lower = search.lower()
        user_notes = [
            note for note in user_notes
            if search_lower in note.value.lower() or
            (hasattr(note, 'tags') and 
             any(search_lower in tag.lower() for tag in (note.tags or [])))
        ]
    
    return user_notes

# To update a specific note by ID
@router.put("/Update_notes/{note_id}", response_model=Note)
async def update_note(
    note_id: str,
    note_update: NoteUpdate,
    username: str = Depends(get_current_user)
):
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="Note not found")
    if notes_db[note_id].owner != username:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if note_update.value is not None:
        notes_db[note_id].value = note_update.value
    if hasattr(note_update, 'tags'):
        notes_db[note_id].tags = note_update.tags
    
    return notes_db[note_id]

# To delete a specific note by ID
@router.delete("/Delete_notes/{note_id}")
async def delete_note(
    note_id: str,
    username: str = Depends(get_current_user)
):
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="Note not found")
    if notes_db[note_id].owner != username:
        raise HTTPException(status_code=403, detail="Not authorized")
    del notes_db[note_id]
    return {"message": "Note deleted successfully"}