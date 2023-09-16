from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.websockets import WebSocket
import asyncio
from pathlib import Path
import logging
from app import utils, env
from app.env import queues

logging.basicConfig(level=logging.INFO)

app = FastAPI(openapi_url="")

dir_path = Path(__file__).parent.resolve()

app.mount("/static", StaticFiles(directory=f"{dir_path}/static"), name="static")

templates = Jinja2Templates(directory=f"{dir_path}/templates")


@app.on_event("startup")
async def init():
    asyncio.get_event_loop().create_task(utils.run(utils.fetch_clients_mock if env.TS_DEBUG_MODE else utils.fetch_clients))


@app.websocket(f'{env.TS_API_PREFIX}/ws')
async def echo(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json(utils.get_users())
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


@app.get(f'{env.TS_API_PREFIX}/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
