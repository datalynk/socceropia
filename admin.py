from collections import defaultdict
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask.ext.wtf import Form
from flask.ext.security import login_required
from sqlalchemy import func
from wtforms import TextField, PasswordField, validators, IntegerField, SelectField, DateTimeField, BooleanField
from models import db, User, Game, GameResult, Forecast, GameWinnerEnum, Team


class UserForm(Form):
    email = TextField('Email', validators=[validators.Required()])
    fullname = TextField('Fullname', validators=[validators.Required()])
    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


class GameResultForm(Form):
    team_host_goals = IntegerField('Team Host goals', validators=[validators.Required()])
    team_guest_goals = IntegerField('Team Guest goals', validators=[validators.Required()])


class GameForm(Form):
    team_1 = SelectField(u'Host team', description='Host team', coerce=int)
    team_2 = SelectField(u'Guest team', description='Guest team', coerce=int)
    date = DateTimeField(u'Date', description='Date time in UTC')
    extra_time_allowed = BooleanField('Extra time allowed?')

admin = Blueprint('admin_app', __name__)

@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@admin.route('/users')
def users():
    users = db.session.query(User).all()
    return render_template('admin/users.html', users=users)


@admin.route('/users/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, fullname=form.fullname.data, password=form.fullname.data,
                    active=True, score=0)
        db.session.add(user)
        db.session.commit()
        return redirect("/admin/")
    return render_template('admin/user_form.html', form=form)


@admin.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get(user_id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash("Changed saved.")
        return redirect(url_for(".users"))
    return render_template('admin/user_form.html', form=form)


@admin.route('/games')
def games():
    games = db.session.query(Game).order_by(Game.date).all()
    total_users = db.session.query(User).count()
    predictions_games = db.session.query(Forecast.game_id, func.count('*')).group_by(Forecast.game_id).all()
    forecast_stat = defaultdict(int, {k: v for k, v in predictions_games})
    return render_template('admin/games.html', games=games, total_users=total_users, forecast_stat=forecast_stat)


@admin.route('/games/add', methods=['GET', 'POST'])
def add_game():
    teams = [(t.id, t.name) for t in db.session.query(Team).order_by(Team.name)]
    form = GameForm()
    form.team_1.choices = teams
    form.team_2.choices = teams
    return render_template('admin/game_form.html', form=form)


@admin.route('/games/edit/<int:game_id>')
def edit_game(game_id):
    return "Edit game: " + str(game_id)


@admin.route('/games/edit/<int:game_id>/result', methods=['GET', 'POST'])
def edit_game_result(game_id):
    form = GameResultForm()
    game = db.session.query(Game).get(game_id)

    if game.result:
        abort("Game result already exists")

    if form.validate_on_submit():
        result = GameResult(game_id=game_id)
        form.populate_obj(result)
        db.session.add(result)

        forecasts = db.session.query(Forecast).filter(Forecast.game_id == game_id).all()
        for forecast in forecasts:
            score = calculate_score(forecast, result)
            forecast.user.score += score

        db.session.commit()

        flash("Results were saved.")
        return redirect(url_for('.games'))

    return render_template('admin/game_result_form.html', form=form, game=game)


def calculate_score(forecast, game_result):
    if forecast.forecast == game_result.get_game_result():
        forecast_score = forecast.final_score()
        actual_score = game_result.final_score()

        if forecast_score == actual_score:
            return 5
        elif game_result.get_game_result() == GameWinnerEnum.TEAM_DRAW:
            return 4
        elif abs(forecast_score[0] - forecast_score[1]) == abs(actual_score[0] - actual_score[1]):
            return 3
        else:
            return 2
    return 0
