from fastapi import FastAPI
from src.auth.controller import authRouter

def register_routes(app: FastAPI):
    app.include_router(authRouter)