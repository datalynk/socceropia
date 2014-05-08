import json
from flask.ext.restful import Api
from api import ForecastAPI, GameAPI, PredictionAPI
import requests
import config
import models
from config import *
from flask import Flask, redirect, request, current_app, abort
from functools import partial, wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

app = Flask(__name__, static_url_path='/static')
app.config.from_object(config)
models.init_db(app)

api = Api(app, prefix='/api')
api.add_resource(ForecastAPI, '/forecast')
api.add_resource(GameAPI, '/games')
api.add_resource(PredictionAPI, '/prediction')

def calculate_score(forecast, game_result):
    TEAM_HOST_WIN = 1
    TEAM_GUEST_WIN = 2
    TEAM_DRAW = 3

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


"""
def update_score(game_result):
    forecasts = db.session.query(Forecast)\
        .filter(Forecast.game_id == game_result.game_id)

    for forecast in forecasts:
        score = calculate_score(forecast, game_result)
        forecast.user.score += score
        db.session.commit()
"""

@app.route('/')
def index():
    return current_app.send_static_file('index.html')


def user_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        if 'X-TOKEN' not in request.headers:
            abort(401)
        token = request.headers['X-TOKEN']
        serializer = Serializer(app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except (SignatureExpired, BadSignature):
            return abort(401)

        email = data['email']
        user = models.db.session.query(models.User).filter_by(email=email).first()
        return fn(user, *args, **kwargs)
    return decorated


@app.route('/test')
@user_required
def test(user):
    return user.name

@app.route('/test2')
def test2():
    serializer = Serializer(app.config['SECRET_KEY'])
    token = serializer.dumps({'email': 'vasilcovsky@gmail.com'})
    #response = current_app.make_response('test')
    #response.set_cookie('token', token)
    #return response
    return token

@app.route('/settings.js')
def settings_js():
    settings = dict(url_root=request.url_root, debug_mode=DEBUG_MODE)
    return 'window.settings = ' + json.dumps(settings)

@app.route('/user/autoregister', methods=['GET', 'POST'])
def autoregistration():
    if request.method == 'GET':
        return redirect('/')

    token = request.form['token']
    user_url = LOGINZA_URL % dict(token=token)
    response = requests.get(user_url)

    response.raise_for_status()

    user = json.loads(response.text)

    fullname = '%(first_name)s %(last_name)s' % user['name']
    email = user['email']
    score = 0

    if not models.User.query.filter(models.User.email == email).count():
        usr = models.User(name=fullname, email=email, score=score)
        models.db.session.add(usr)
        models.db.session.commit()

    return redirect('/#games')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)