from sqlalchemy import and_
from sqlalchemy.orm import relationship
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required


db = SQLAlchemy()

class GameWinnerEnum(object):
    TEAM_HOST_WIN = 1
    TEAM_GUEST_WIN = 2
    TEAM_DRAW = 3
    

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    fullname = db.Column(db.String(255))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    score = db.Column(db.Integer, nullable=False, default=0)

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))




class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_1 = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team_2 = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    date = db.Column(db.DateTime)
    extra_time_allowed = db.Column(db.Boolean)
    team_host = relationship('Team', primaryjoin='Game.team_1==Team.id')
    team_guest = relationship('Team', primaryjoin='Game.team_2==Team.id')
    details = relationship('GameDetail')
    result = relationship('GameResult', uselist=False)

    def to_dict(self):
        return {
            'id': self.id,
            'team_host': self.team_host.to_dict(),
            'team_guest': self.team_guest.to_dict(),
            'date': self.date,
            'extra_time_allowed': self.extra_time_allowed
        }


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
    game = relationship('Game')
    user = relationship('User')

    def final_score(self):
        return self.team_host_goals, self.team_guest_goals

    def to_dict(self):
        return {
            'forecast': self.forecast,
            'team_host_goals': self.team_host_goals,
            'team_guest_goals': self.team_guest_goals
        }


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


def get_games_for_user(user_id):
    """Returns list of games and forecast."""
    games = db.session.query(Game, Forecast).\
        outerjoin(Forecast, and_(Forecast.user_id == user_id, Forecast.game_id == Game.id)).\
        all()

    objects = []
    for game, forecast in games:
        item = {
            'game': game.to_dict(),
            'forecast': {
                'team_host_goals': forecast.team_host_goals if forecast else None,
                'team_guest_goals': forecast.team_guest_goals if forecast else None,
                'forecast': forecast.forecast if forecast else None
            }
        }
        objects.append(item)

    return objects

def create_forecast(user_id, game_id, forecast, team_host_goals, team_guest_goals):
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


def get_leaderboard():
    leaders = db.session.query(User.fullname, User.score).order_by(-User.score)\
        .all()
    return leaders