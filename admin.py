from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, validators
from wtforms.validators import Email, DataRequired
from models import db, User

class UserForm(Form):
    email = TextField('Email', validators=[validators.Required()])
    fullname = TextField('Fullname', validators=[validators.Required()])
    password = PasswordField('Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')


admin = Blueprint('admin_app', __name__)

@admin.route('/')
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
    return "Games list"


@admin.route('/games/add')
def add_game():
    return "Add game"


@admin.route('/games/edit/<int:game_id>')
def edit_game(game_id):
    return "Edit game: " + str(game_id)


@admin.route('/games/edit/<int:game_id>/result')
def edit_game_result(game_id):
    return "Edit game result: " + str(game_id)

