from fastapi import FastAPI
from src.auth.controller import authRouter
from src.files.controller import file_router

def register_routes(app: FastAPI):
    app.include_router(authRouter)
    app.include_router(file_router)