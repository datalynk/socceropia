from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from sqlalchemy.orm import relationship

TEAM_HOST_WIN = 1
TEAM_GUEST_WIN = 2
TEAM_DRAW = 3

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(60))
    score = db.Column(db.Integer, nullable=False, default=0)


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
            return TEAM_HOST_WIN
        elif self.team_host_goals < self.team_guest_goals:
            return TEAM_GUEST_WIN
        return TEAM_DRAW

"""
@event.listens_for(scoped_session(db.session), 'before_flush')
def game_result_inserted_listener(session, flush_context, instances):
    import pprint
    pprint.pprint(instances)
    #update_score(game_result=target)

event.listen(GameResult, 'append', game_result_inserted_listener)
"""

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


class BaseRepository(object):

    __model_class__ = None

    def all(self):
        return self.session().query(self.__model_class__).all()

    def get_by_id(self, id):
        return self.session().query(self.__model_class__).filter_by(id == id).one()

    def save(self, entry):
        return self.session().add(entry)

    @staticmethod
    def session():
        return db.session


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