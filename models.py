from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# This file contains Pydantic models for the application.
class User(BaseModel):
    username: str
    hashed_password: str

class Note(BaseModel):
    id: str
    value: str
    owner: str
    tags: Optional[List[str]] = None
    created_at: datetime
    
class NoteCreate(BaseModel):
    value: str
    
class NoteUpdate(BaseModel): 
    value: Optional[str] = None
    tags: Optional[List[str]] = None 

class UserCreate(BaseModel):
    username: str
    password: str