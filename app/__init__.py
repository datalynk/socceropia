import config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from models import db
from security import security
from admin import admin

app = Flask(__name__, static_url_path='')
app.config.from_object(config)

mail = Mail(app)

db.init_app(app)
security.init_app(app)

app.register_blueprint(admin, url_prefix='/admin')

db.app = app
db.create_all()


from app import views
from app import security
from app import filters
from app import api