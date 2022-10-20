
from flask import Flask, render_template
import requests
import os
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

TS_API_KEY = os.getenv('TS_API_KEY')
TS_API_URL = os.getenv('TS_API_URL')

def get_clients():
    session = requests.Session()
    session.headers.update({'x-api-key': TS_API_KEY})
    r = session.get(f'{TS_API_URL}1/clientlist')
    data = r.json()
    logging.info(f'API OUTPUT: {data}')
    users = []
    if 'body' in data:
        for user in data['body']:
            name = user['client_nickname']
            users.append(name) if name != "serveradmin" else ""
    return users


@app.route('/')
def index():
    return render_template("index.html", users=get_clients())
