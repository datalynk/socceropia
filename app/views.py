import json
from flask import request, current_app
from flask.ext.security import current_user
from app import app, config


@app.route('/')
@app.route('/index')
def index():
    return current_app.send_static_file('index.html')

@app.route('/settings.js')
@app.route('/settings')
def settings():
    settings = {
        'url_root': request.url_root,
        'debug_mode': config.DEBUG_MODE,
        'user': {
            'name': current_user.fullname if current_user.is_authenticated() else '',
            'anonymous': not current_user.is_authenticated()
        },
        #'gameResultEnum': {k:v for k, v in models.GameWinnerEnum.__dict__.iteritems() if not k.startswith('_')}
    }
    return 'window.settings = ' + json.dumps(settings)