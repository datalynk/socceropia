import csv
import datetime
from collections import namedtuple
from app import Game, GameDetail, Team, db

csvrow = namedtuple('Row', 'date,time,team_a,team_b,city')

teams = {t.name: t.id for t in Team.query.all()}

Game.query.delete()

with open('data/group-games.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for line in reader:
        row = csvrow._make(line)
        date = [int(t) for t in row.date.split("/")]
        time = [int (t) for t in row.time.split(":")]

        datetime_ = datetime.datetime(year=2000+date[2], month=date[0], day=date[1], hour=time[0], minute=time[1])
        g = Game(team_1=teams[row.team_a], team_2=teams[row.team_b], date=datetime_, extra_time_allowed=False)
        db.session.add(g)
        db.session.commit()
        db.session.refresh(g)

        detail = GameDetail(city=row.city, game_id=g.id)
        db.session.add(detail)
        db.session.commit()