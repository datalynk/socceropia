from flask import redirect, render_template, abort, flash, url_for
from flask.ext.security import login_required

from . import admin
from .forms import UserForm
from ..models import db, Game, User, Forecast
from ..security import user_datastore

@admin.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = user_datastore.create_user(email=form.email.data, fullname=form.fullname.data, password=form.password,
                                            active=True, score=0)
        db.session.commit()
        flash("User {} was created".format(form.email.data))
        return redirect("/admin/")
    return render_template('admin/user_form.html', form=form)


@admin.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
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