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
import functools
from uuid import uuid4

# deps
from loguru import logger
from flask import redirect, url_for, session

# app imports
from .db import get_redis

REDIS_USER_PREFIX = 'justify:user:'


def check_user(f):
    """ Decorator: redirects user to new_user page
    if the user is unknown.
    XXX: This is buggy
    TODO: fix this shit
    """
    @functools.wraps(f)
    def decorated_f(*args, **kwargs):
        logger.debug(f"SESSION IN DEC: {session}")
        if 'userid' not in session:
            logger.info('Unknown user. Redirecting to new user endpoint.')
            return redirect(url_for('web.new_user'))
        return f(*args, **kwargs)
    return decorated_f


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
