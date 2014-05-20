from models import db, User, Role
from flask.ext.security import SQLAlchemyUserDatastore, Security

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)
