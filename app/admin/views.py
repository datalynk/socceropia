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
