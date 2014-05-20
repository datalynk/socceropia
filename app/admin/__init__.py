from flask import Blueprint

admin = Blueprint('admin app', __name__)


from .views import *
from .controllers import *