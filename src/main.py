from fastapi import FastAPI
from app.models.enums import Message
from app.api.auth import userRouter

app = FastAPI(title="file upload")

@app.get("/")
def root():
    return {"message": Message.HELLO}

app.include_router(userRouter, prefix="/users")