import json
from flask import request, current_app
from flask.ext.security import current_user
from app import app, config


@app.route('/')
@app.route('/index')
def index():
    return current_app.send_static_file('index.html')

