from fastapi import FastAPI
from app.users import router as users_router  
from app.notes import router as notes_router 

app = FastAPI()

# Include routers for user and note management
app.include_router(users_router)
app.include_router(notes_router)



def root():
    return {"message": "Notes API"}
