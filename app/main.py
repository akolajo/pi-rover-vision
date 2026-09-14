from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router

app = FastAPI(title="Pi Rover Vision")

app.mount("/static", StaticFiles(directory="app/camera/static"), name="static")
app.include_router(router)