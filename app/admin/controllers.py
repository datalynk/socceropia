import forms

from flask import redirect, render_template, abort, flash, url_for
from flask.ext.security import login_required, registerable

from . import admin
from ..models import db, Game, User, Forecast, Team, GameResult, GameWinnerEnum


@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    form = forms.UserRegistrationForm()
    if form.validate_on_submit():
        user = registerable.register_user(email=form.email.data, fullname=form.fullname.data,
                                          password=form.password.data)
        flash("User {} was created".format(form.email.data))
        return redirect(url_for('.users'))

    return render_template('admin/user_add.html', form=form)


@admin.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    form = forms.UserEditForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash("User was updated")
        return redirect(url_for('.users'))

    return render_template('admin/user_form.html', form=form)


@admin.route('/games/add', methods=['GET', 'POST'])
def add_game():
    teams = [(t.id, t.name) for t in db.session.query(Team).order_by(Team.name)]
    form = forms.GameForm()
    form.team_1.choices = teams
    form.team_2.choices = teams

    if form.validate_on_submit():
        game = Game()
        form.populate_obj(game)
        db.session.add(game)
        db.session.commit()
        flash("Game was added.")
        return redirect(url_for('.games'))

    return render_template('admin/game_form.html', form=form)


@admin.route('/games/edit/<int:game_id>')
def edit_game(game_id):
    return "Edit game: " + str(game_id)


@admin.route('/games/edit/<int:game_id>/result', methods=['GET', 'POST'])
def edit_game_result(game_id):
    form = forms.GameResultForm()
    game = db.session.query(Game).get(game_id)

    form.team_host_goals.label.text = game.team_host.name
    form.team_guest_goals.label.text = game.team_guest.name

    if game.result:
        abort("Game result already exists")

    if form.validate_on_submit():
        result = GameResult(game_id=game_id)
        form.populate_obj(result)
        db.session.add(result)

        forecasts = db.session.query(Forecast).filter(Forecast.game_id == game_id).all()
        for forecast in forecasts:
            score = calculate_score(forecast, result)
            forecast.points = score
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