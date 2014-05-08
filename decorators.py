from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from flask import abort, request, current_app
from models import User, db


def user_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        if 'X-TOKEN' not in request.headers:
            abort(401)
        token = request.headers['X-TOKEN']
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except (SignatureExpired, BadSignature):
            return abort(401)

        email = data['email']
        user = db.session.query(User).filter_by(email=email).first()
        kwargs['user'] = user
        return fn(*args, **kwargs)
    return decorated