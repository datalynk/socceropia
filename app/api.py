from app import app
from flask import jsonify
from flask.ext.restful import Api, Resource, reqparse, marshal, fields
from flask.ext.security import current_user
from models import db, User, Game, Forecast


def success(response):
    return dict(status="success", data=response)


def fail(response):
    return dict(status="fail", data=response)


def error(message):
    return dict(status="error", message=message)


def user_required(fn):
    def wrapped(*args, **kwargs):
        if current_user.is_anonymous():
            return error("User required.")
        return fn(*args, **kwargs)
    return wrapped


class UserAPI(Resource):
    def get(self):
        if current_user.is_anonymous():
            return success(dict(is_anonymous=True))

        return success({
            "avatar_url": current_user.get_avatar_url(),
            "name": current_user.fullname,
            "is_anonymous": False
        })


class PredictionAPI(Resource):
    @user_required
    def get(self):
        def get_games(user_id):
            games = db.session.query(Game, Forecast).\
                outerjoin(Forecast, db.and_(Forecast.user_id == user_id, Forecast.game_id == Game.id)).\
                all()
            return games

        def game_to_response(game, forecast):
            game_ = {
                "id": game.id,
                "date": game.date.isoformat(),
                "team_host": {
                    "id": game.team_host.id,
                    "name": game.team_host.name
                },
                "team_guest": {
                    "id": game.team_guest.id,
                    "name": game.team_guest.name
                },
                "locked": not game.is_forecast_allowed()
            }

            forecast_ = None

            if forecast:
                forecast_ = {
                    "forecast": forecast.forecast,
                    "team_host_goals": forecast.team_host_goals,
                    "team_guest_goals": forecast.team_guest_goals,
                    "points": 0
                }

            result_ = None
            if game.result:
                result_ = {
                    "team_host_goals": game.result.team_host_goals,
                    "team_guest_goals": game.result.team_guest_goals
                }

            return dict(game=game_, forecast=forecast_, result=result_)

        games = [game_to_response(*g) for g in get_games(current_user.id)]
        return success(dict(objects=games))

    @user_required
    def post(self):
        def save_forecast(user_id, game_id, forecast, team_host_goals, team_guest_goals):
            forecast_ = db.session.query(Forecast).\
                filter(Forecast.user_id == user_id).\
                filter(Forecast.game_id == game_id).\
                first()

            if not forecast_:
                forecast_ = Forecast(user_id=user_id, game_id=game_id)

            forecast_.forecast = forecast
            forecast_.team_host_goals = team_host_goals
            forecast_.team_guest_goals = team_guest_goals

            db.session.add(forecast_)
            db.session.commit()

        parser = reqparse.RequestParser()
        parser.add_argument('game_id', type=int, help='Game ID')
        parser.add_argument('forecast', type=int, help='Forecast: 0, 1, 2')
        parser.add_argument('team_host_goals', type=int, help='Team host goals')
        parser.add_argument('team_guest_goals', type=int, help='Team host goals')
        args = parser.parse_args()

        save_forecast(current_user.id, args.game_id, args.forecast, args.team_host_goals, args.team_guest_goals)


class LeaderBoardAPI(Resource):
    def get(self):
        def user_to_response(user):
            return {
                "name": user.fullname,
                "score": user.score,
                "avatar_url": user.get_avatar_url()
            }

        leaders = [user_to_response(u) for u in db.session.query(User).order_by(-User.score).all()]
        return success(dict(objects=leaders))


api = Api(app, prefix='/api')
api.add_resource(UserAPI, '/user')
api.add_resource(PredictionAPI, '/prediction')
api.add_resource(LeaderBoardAPI, '/leaderboard')