from fastapi import APIRouter, HTTPException, status
from app.auth import create_access_token, verify_password
from app.database import users_db
from models import User, UserCreate
from app.auth import get_password_hash  
from fastapi import APIRouter

router = APIRouter()

# User authentication endpoints

# Register new users
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    users_db[user.username] = User(
        username=user.username,
        hashed_password=hashed_password
    )
    return {"message": "User created successfully"}

# Login users
@router.post("/login")
async def login(user: UserCreate):
    if user.username not in users_db or not verify_password(user.password, users_db[user.username].hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}