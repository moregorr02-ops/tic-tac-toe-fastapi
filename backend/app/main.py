from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from .database import engine, Base
from . import models   # <-- обязательно
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tic-Tac-Toe API")
app.include_router(router)

static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")

@app.get("/")
async def get_index():
    return FileResponse(os.path.join(static_dir, "index.html"))

app.mount("/static", StaticFiles(directory=static_dir), name="static")