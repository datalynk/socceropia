from flask import jsonify
from flask.ext.restful import Resource, reqparse
from flask.ext.security import current_user
from decorators import user_required
from models import *


class ForecastAPI(Resource):
    @user_required
    def get(self, user):
        return {'objects': []}


class GameAPI(Resource):
    @user_required
    def get(self, user):
        objects = get_games_for_user(user.id)
        return jsonify(dict(objects=objects))


class PredictionAPI(Resource):
    def get(self):
        objects = get_games_for_user(current_user.id)
        return jsonify(dict(objects=objects))

    def post(self):
        user = current_user
        parser = reqparse.RequestParser()
        parser.add_argument('game_id', type=int, help='Game ID')
        parser.add_argument('forecast', type=int, help='Forecast: 0, 1, 2')
        parser.add_argument('team_host_goals', type=int, help='Team host goals')
        parser.add_argument('team_guest_goals', type=int, help='Team host goals')
        args = parser.parse_args()

        create_forecast(user.id, args.game_id, args.forecast, args.team_host_goals, args.team_guest_goals)