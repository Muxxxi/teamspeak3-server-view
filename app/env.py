from typing import Dict
import asyncio
import os

queues : Dict[int, asyncio.Queue] = {}

LOG_LEVEL = os.getenv("TS_LOG_LEVEL", "INFO")
TS_API_KEY = os.getenv('TS_API_KEY', '')
TS_API_URL = os.getenv('TS_API_URL', '')