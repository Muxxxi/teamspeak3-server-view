from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocket
import asyncio
from pathlib import Path
import logging
from app import utils
from app.env import queues
from app.utils import users

logging.basicConfig(level=logging.INFO)

app = FastAPI(openapi_url="")

dir_path = Path(__file__).parent.resolve()


app.mount("/static", StaticFiles(directory=f"{dir_path}/static"), name="static")

templates = Jinja2Templates(directory=f"{dir_path}/templates")
favicon_path = f'/{dir_path}/static/favicon.ico'



@app.on_event("startup")
async def init():
    asyncio.get_event_loop().create_task(utils.run(utils.fetch_clients))


@app.middleware("http")
async def set_root_path_for_api_gateway(request: Request, call_next):
    """Sets the FastAPI root_path dynamically from the ASGI request data."""
    root_path = request.headers.get('X-Forwarded-Prefix')
    request.scope.update()
    if root_path:
        request.scope["root_path"] = root_path
        app.root_path = root_path
    response = await call_next(request)
    return response


@app.websocket('/ws')
async def echo(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json(users)
    queue = asyncio.Queue()
    queues[id(websocket)] = queue
    try:
        while True:
            value = await queue.get()
            await websocket.send_json(value)
            queue.task_done()
    except Exception as e:
        logging.error(f'Error: {e}')
    finally:
        del queues[id(websocket)]


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)
