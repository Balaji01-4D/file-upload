from fastapi import FastAPI
from .api import register_routes
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="file upload")

@app.get("/")
def root():
    return {"message": "hello world"}

register_routes(app)
