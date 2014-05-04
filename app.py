import json
import requests
from config import *
from datetime import datetime
from flask import Flask, redirect, request
import flask.ext.sqlalchemy
import flask.ext.restless
from sqlalchemy import event
from sqlalchemy.orm import relationship, scoped_session
from functools import partial

TEAM_HOST_WIN = 1
TEAM_GUEST_WIN = 2
TEAM_DRAW = 3

app = Flask(__name__, static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forecaster.db'
db = flask.ext.sqlalchemy.SQLAlchemy(app)
db_session = scoped_session(db.session)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(60))
    score = db.Column(db.Integer, nullable=False, default=0)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_1 = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team_2 = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    date = db.Column(db.DateTime)
    extra_time_allowed = db.Column(db.Boolean)
    team_host = relationship('Team', primaryjoin='Game.team_1==Team.id')
    team_guest = relationship('Team', primaryjoin='Game.team_2==Team.id')
    details = relationship('GameDetail')

class GameDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    city = db.Column(db.String(100))
    weather_c = db.Column(db.String(10))
    weather_t = db.Column(db.String(10))

class GameResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    team_host_goals = db.Column(db.Integer)
    team_guest_goals = db.Column(db.Integer)

    def final_score(self):
        return self.team_host_goals, self.team_guest_goals

    def get_game_result(self):
        if self.team_host_goals > self.team_guest_goals:
            return TEAM_HOST_WIN
        elif self.team_host_goals < self.team_guest_goals:
            return TEAM_GUEST_WIN
        return TEAM_DRAW

"""
@event.listens_for(scoped_session(db.session), 'before_flush')
def game_result_inserted_listener(session, flush_context, instances):
    import pprint
    pprint.pprint(instances)
    #update_score(game_result=target)

event.listen(GameResult, 'append', game_result_inserted_listener)
"""

class Forecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    forecast = db.Column(db.Integer)
    team_host_goals = db.Column(db.Integer)
    team_guest_goals = db.Column(db.Integer)
    game = relationship('Game')
    user = relationship('User')

    def final_score(self):
        return self.team_host_goals, self.team_guest_goals

def calculate_score(forecast, game_result):
    if forecast.forecast == game_result.get_game_result():
        forecast_score = forecast.final_score()
        actual_score = game_result.final_score()

        if forecast_score == actual_score:
            return 5
        elif game_result.get_game_result() == TEAM_DRAW:
            return 4
        elif abs(forecast_score[0] - forecast_score[1]) == abs(actual_score[0] - actual_score[1]):
            return 3
        else:
            return 2
    return 0


def update_score(game_result):
    forecasts = db.session.query(Forecast)\
        .filter(Forecast.game_id == game_result.game_id)

    for forecast in forecasts:
        score = calculate_score(forecast, game_result)
        forecast.user.score += score
        db.session.commit()

def get_weather_forecast(apikey, country_code, city):
    city_ = city.replace(' ', '_')
    result = requests.get('http://api.wunderground.com/api/%(apikey)s/conditions/q/%(country_code)s/%(city_)s.json'
                 % locals())

    result.raise_for_status()
    obj = json.loads(result.text)
    return obj

get_weather = partial(get_weather_forecast, WEATHER_API_KEY, 'BR')

db.create_all()
manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Forecast,  methods=['GET', 'POST', 'DELETE'])
manager.create_api(Game, methods=['GET'], results_per_page=100, max_results_per_page=100)
manager.create_api(Team, methods=['GET'])
manager.create_api(User, methods=['GET'], include_columns=['id', 'name', 'score'],
                   results_per_page=100, max_results_per_page=100)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/settings.js')
def settings_js():
    settings = dict(url_root=request.url_root, debug_mode=DEBUG_MODE)
    return 'window.settings = ' + json.dumps(settings)

@app.route('/user/autoregister', methods=['POST'])
def autoregistration():
    token = request.form['token']
    user_url = LOGINZA_URL % dict(token=token)
    response = requests.get(user_url)

    response.raise_for_status()

    user = json.loads(response.text)

    fullname = '%(first_name)s %(last_name)s' % user['name']
    email = user['email']
    score = 0

    if not User.query.filter(User.email == email).count():
        usr = User(name=fullname, email=email, score=score)
        db.session.add(usr)
        db.session.commit()

    return redirect('/#games')

@app.route('/weather')
def weater():
    weather = get_weather('Salvador')
    return json.dumps(weather)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)