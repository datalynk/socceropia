from collections import defaultdict
from flask import render_template
from flask.ext.security import login_required

from app.models import db, Game, User, Forecast
from . import admin

@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/games')
@login_required
def games():
    games = db.session.query(Game).order_by(Game.date).all()
    total_users = db.session.query(User).count()
    predictions_games = db.session.query(Forecast.game_id, db.func.count('*')).group_by(Forecast.game_id).all()
    forecast_stat = defaultdict(int, {k: v for k, v in predictions_games})
    return render_template('admin/games.html', games=games, total_users=total_users, forecast_stat=forecast_stat)


@admin.route('/users')
@login_required
def users():
    users = db.session.query(User).all()
    return render_template('admin/users.html', users=users)


@admin.route('/users/<int:user_id>/forecasts')
def view_user_forecasts(user_id):
    user = User.query.get(user_id)

    items = db.session.query(Game, Forecast).\
        outerjoin(Forecast, db.and_(Game.id == Forecast.game_id, Forecast.user_id == user_id)).\
        all()

    has_prediction = lambda x: x[1] is not None

    games_predictions = []
    games = []

    for i in items:
        (games_predictions if has_prediction(i) else games).append(i)

    return render_template('admin/user_forecast.html',
                           games_predictions=games_predictions,
                           games=games,
                           user=user)
