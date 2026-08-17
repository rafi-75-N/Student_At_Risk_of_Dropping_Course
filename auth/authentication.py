from utils.api_client import register_user as _register_user
from utils.api_client import login_user as _login_user


def register_user(name, email, password, confirm):

    try:
        return _register_user(name, email, password, confirm)

    except Exception:
        return False, "Couldn't reach the server. Is the API running (uvicorn api.main:app)?"


def login_user(email, password):

    try:
        return _login_user(email, password)

    except Exception:
        return False, "Couldn't reach the server. Is the API running (uvicorn api.main:app)?"
