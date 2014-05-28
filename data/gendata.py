#!/usr/bin/python
# -*- coding: UTF-8 -*-

import datetime
from app_old import Game, Team, User, Forecast, GameResult, db
from app_old import TEAM_HOST_WIN

User.query.delete()
Team.query.delete()
Game.query.delete()
GameResult.query.delete()

users = []
users.append(User(email='vasilcovsky@gmail.com', name='Igor V', score=10))
users.append(User(email='shinjik@gmail.com', name='Shinji K', score=15))

db.session.add_all(users)
db.session.commit()

for user in users:
    db.session.refresh(user)

teams = []
teams.append(Team(name='Algeria'))
teams.append(Team(name='Cameroon'))
teams.append(Team(name='Ivory Coast'))
teams.append(Team(name='Ghana'))
teams.append(Team(name='Nigeria'))
teams.append(Team(name='Australia'))
teams.append(Team(name='Iran'))
teams.append(Team(name='Japan'))
teams.append(Team(name='South Korea'))
teams.append(Team(name='Belgium'))
teams.append(Team(name='Bosnia and Herzegovina'))
teams.append(Team(name='Croatia'))
teams.append(Team(name='England'))
teams.append(Team(name='France'))
teams.append(Team(name='Germany'))
teams.append(Team(name='Greece'))
teams.append(Team(name='Italy'))
teams.append(Team(name='Netherlands'))
teams.append(Team(name='Portugal'))
teams.append(Team(name='Russia'))
teams.append(Team(name='Spain'))
teams.append(Team(name='Switzerland'))
teams.append(Team(name='Costa Rica'))
teams.append(Team(name='Honduras'))
teams.append(Team(name='Mexico'))
teams.append(Team(name='USA'))
teams.append(Team(name='Argentina'))
teams.append(Team(name='Brazil'))
teams.append(Team(name='Chile'))
teams.append(Team(name='Colombia'))
teams.append(Team(name='Ecuador'))
teams.append(Team(name='Uruguay'))

db.session.add_all(teams)
db.session.commit()

for team in teams:
    db.session.refresh(team)


games = []
games.append(Game(team_1=teams[0].id, team_2=teams[1].id, date=datetime.datetime.now(), extra_time_allowed=False))
db.session.add_all(games)
db.session.commit()

for game in games:
    db.session.refresh(game)

forecasts = []
forecasts.append(Forecast(game_id = games[0].id, user_id = users[0].id, forecast=TEAM_HOST_WIN, team_host_goals=4, team_guest_goals=2))
db.session.add_all(forecasts)
db.session.commit()

results = []
results.append(GameResult(game_id=games[0].id, team_host_goals=4, team_guest_goals=2))
db.session.add_all(results)
db.session.commit()