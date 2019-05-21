"""
Manages registered users in Redis.

Redis schema:

justify:user:uniqueid
{
    'username':     str,
    'votes_current': list[str],
    'votes_history': list[str]
}

"""

# std lib
from uuid import uuid4

# deps
from loguru import logger
from flask import redirect, url_for, request, session
from flask import current_app as app

# app imports
from .db import get_redis

REDIS_USER_PREFIX = 'justify:user:'


@app.before_request
def check_user():
    if ('userid' not in session and request.endpoint != 'newuser'):
        redirect(url_for('new_user'))


def add_user(username: str):
    """ Add a new user to db,
    with user-chosen username.
    Return value is the unique id of the user.
    """
    logger.info(f"New user with name: {username}")
    # gen random unique user id
    userid = uuid4().hex

    # assemble user entry
    udata = {
        'username': username,
        'votes_current': '[]',
        'votes_history': '[]'
    }

    # put in redis
    r = get_redis()
    r.hmset(f'{REDIS_USER_PREFIX}{userid}', udata)

    return userid
