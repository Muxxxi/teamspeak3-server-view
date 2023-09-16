import uvicorn
from app import app, env
import logging
import sys


def main():
    level = logging.getLevelName(env.LOG_LEVEL)
    logging.basicConfig(level=level)

    logging.info(f' Startup TS Server Viewer. Log level: {env.LOG_LEVEL}')

    if (env.TS_API_KEY == "" or env.TS_API_URL == "") and not env.TS_DEBUG_MODE:
        logging.error(f' Please provide TS server api credentials')
        sys.exit(1)

    uvicorn.run(app.app, host="0.0.0.0", port=8080, proxy_headers=True, forwarded_allow_ips="*")


if __name__ == "__main__":
    main()