import asyncio
import logging
import random
import string
from typing import Callable

import requests

from app import env

users = []


def get_users():
    global users
    return users


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def fetch_clients():
    session = requests.Session()
    session.headers.update({'x-api-key': env.TS_API_KEY})
    r = session.get(f'{env.TS_API_URL}1/clientlist')
    data = r.json()
    logging.debug(f'API OUTPUT: {data}')
    new_users = []
    if 'body' in data:
        for user in data['body']:
            name = user['client_nickname']
            new_users.append(name) if name != "serveradmin" else ""
    return new_users


def fetch_clients_mock():
    random_users = [get_random_string(5) for x in range(10)]
    logging.debug(f'List of mock users: {random_users}')
    return random_users


async def run(func: Callable):
    logging.info("Start ts server listener...")
    global users
    while True:
        try:
            new_users = func()
            logging.info(f"Refresh user list: {new_users}")
            if users != new_users:
                users = new_users
                for q in env.queues.values():
                    try:
                        q.put_nowait(users)
                    except asyncio.QueueFull as e:
                        logging.info(e)
            await asyncio.sleep(int(env.TS_API_INTERVAL))
        except Exception as e:
            logging.error(f'{e}')
            await asyncio.sleep(int(env.TS_API_INTERVAL))
            continue
