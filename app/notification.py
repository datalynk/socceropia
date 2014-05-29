from app import app, models, mail
from flask import render_template
from flask.ext.mail import Message

def message(recipient):
    return Message(sender="noreply@socceropia.com", recipients=[recipient])


def no_forecast(games):
    games = models.db.session.query(models.Game).all()
    content = render("notification/no_forecast.html", games=games, user={})

    msg = message("")
    msg.subject = "No forecast"
    msg.html = content
    send_mail(msg)


def send_mail(msg):
    with app.app_context():
        mail.send(msg)

def render(template_name_or_list, **context):
    with app.app_context():
        return render_template(template_name_or_list, **context)