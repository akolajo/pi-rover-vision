from fastapi import APIRouter
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from app.camera.stream import generate_frames
from app.state import tracking_state

router = APIRouter()
templates = Jinja2Templates(directory="app/camera/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/video_feed")
async def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


@router.get("/tracking/status")
async def tracking_status():
    return tracking_state.get()