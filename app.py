import json
import requests
import config
import models
from admin import admin

from flask import Flask, redirect, request, current_app, abort, render_template
from flask.ext.restful import Api
from flask.ext.security import RegisterForm
from flask.ext.security import SQLAlchemyUserDatastore, Security, AnonymousUser, login_required, current_user
from flask.ext.mail import Mail

from api import ForecastAPI, GameAPI, PredictionAPI, LeaderboardAPI

from wtforms import TextField
from wtforms.validators import Required


class UserRegisterForm(RegisterForm):
    fullname = TextField('Full name', [Required()],
                         description="Enter your first and last name. Name will be displayed in Leaderboard.")


app = Flask(__name__, static_url_path='/static')
app.config.from_object(config)
mail = Mail(app)
app.register_blueprint(admin, url_prefix='/admin')
models.init_db(app)

api = Api(app, prefix='/api')
api.add_resource(ForecastAPI, '/forecast')
api.add_resource(GameAPI, '/games')
api.add_resource(PredictionAPI, '/prediction')
api.add_resource(LeaderboardAPI, '/leaderboard')

user_datastore = SQLAlchemyUserDatastore(models.db, models.User, models.Role)
security = Security(app, user_datastore, register_form=UserRegisterForm)


@app.route('/')
def index():
    return current_app.send_static_file('index.html')


@app.route('/settings.js')
def settings():
    settings = {
        'url_root': request.url_root,
        'debug_mode': config.DEBUG_MODE,
        'user': {
            'name': current_user.fullname if current_user.is_authenticated() else '',
            'anonymous': not current_user.is_authenticated()
        },
        'gameResultEnum': {k:v for k, v in models.GameWinnerEnum.__dict__.iteritems() if not k.startswith('_')}
    }
    return 'window.settings = ' + json.dumps(settings)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)