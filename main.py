import uvicorn
from app import app
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    uvicorn.run(app.app, host="0.0.0.0", port=8080)