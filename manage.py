#!/usr/bin/python
# -*- coding: UTF-8 -*-

from app import app
from getpass import getpass
from datetime import datetime
from flask import current_app
import argparse


def create_user(args):
    with app.app_context():
        from app.models import db, User, Role
        from flask.ext.security.utils import encrypt_password

        email = raw_input('Enter email: ')
        fullname = raw_input('Name: ')
        password = getpass()
        assert password == getpass('Password (again):')

        user = User(email=email, password=encrypt_password(password),
                    fullname=fullname, active=True, confirmed_at=datetime.now())
        db.session.add(user)
        db.session.commit()
        print("User created.")


def import_teams(args):
    from app.models import Team, db

    Team.query.delete()

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


def import_games(args):
    import csv
    from collections import namedtuple
    from app.models import Game, GameDetail, Team, db

    csvrow = namedtuple('Row', 'date,time,team_a,team_b,city')

    teams = {t.name: t.id for t in Team.query.all()}

    Game.query.delete()

    with open('data/group-games.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for line in reader:
            row = csvrow._make(line)
            date = [int(t) for t in row.date.split("/")]
            time = [int (t) for t in row.time.split(":")]

            datetime_ = datetime(year=2000+date[2], month=date[0], day=date[1], hour=time[0], minute=time[1])
            g = Game(team_1=teams[row.team_a], team_2=teams[row.team_b], date=datetime_, extra_time_allowed=False)
            db.session.add(g)
            db.session.commit()
            db.session.refresh(g)

            detail = GameDetail(city=row.city, game_id=g.id)
            db.session.add(detail)
            db.session.commit()


def _main(args):
    fn = globals().get(args.command, None)
    if fn:
        fn(args)
    else:
        print("Command %s not found" % args.command)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', metavar='COMMAND')
    args = parser.parse_args()
    _main(args)


if __name__ == '__main__':
    main()