import hashlib
import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import security

db = SQLAlchemy()


class Role(db.Model, security.RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class User(db.Model, security.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    fullname = db.Column(db.String(255))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    score = db.Column(db.Integer, nullable=False, default=0)
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(40))
    current_login_ip = db.Column(db.String(40))
    login_count = db.Column(db.Integer)

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


    def get_avatar_url(self):
        hash = hashlib.md5(self.email).hexdigest()
        return "http://www.gravatar.com/avatar/" + hash




class GameWinnerEnum(object):
    TEAM_HOST_WIN = 1
    TEAM_GUEST_WIN = 2
    TEAM_DRAW = 3



class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_1 = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team_2 = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    date = db.Column(db.DateTime)
    extra_time_allowed = db.Column(db.Boolean)
    team_host = db.relationship('Team', primaryjoin='Game.team_1==Team.id')
    team_guest = db.relationship('Team', primaryjoin='Game.team_2==Team.id')
    details = db.relationship('GameDetail')
    result = db.relationship('GameResult', uselist=False)

    def is_forecast_allowed(self):
        five_min_before = self.date - datetime.timedelta(seconds=300)
        return five_min_before > datetime.datetime.now()

    @property
    def game_title(self):
        return self.team_host.name + " - " + self.team_guest.name

    @property
    def game_result(self):
        if self.result:
            return "{} - {}".format(self.result.team_host_goals, self.result.team_guest_goals)
        return 'N/A'


class GameDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    city = db.Column(db.String(100))
    weather_c = db.Column(db.String(10))
    weather_t = db.Column(db.String(10))


class GameResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    team_host_goals = db.Column(db.Integer)
    team_guest_goals = db.Column(db.Integer)
    __excluded__ = ('id', 'game_id')

    def final_score(self):
        return self.team_host_goals, self.team_guest_goals

    def get_game_result(self):
        if self.team_host_goals > self.team_guest_goals:
            return GameWinnerEnum.TEAM_HOST_WIN
        elif self.team_host_goals < self.team_guest_goals:
            return GameWinnerEnum.TEAM_GUEST_WIN
        return GameWinnerEnum.TEAM_DRAW


class Forecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    forecast = db.Column(db.Integer)
    team_host_goals = db.Column(db.Integer)
    team_guest_goals = db.Column(db.Integer)
    points = db.Column(db.Integer, default=0)
    game = db.relationship('Game')
    user = db.relationship('User')

    def final_score(self):
        return self.team_host_goals, self.team_guest_goals

    @property
    def prediction(self):
        return "{} - {}".format(self.team_host_goals, self.team_guest_goals)
