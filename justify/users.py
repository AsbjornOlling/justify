"""
Manages registered users in Redis.
"""

# std lib
import json
from functools import wraps
from uuid import uuid4
from typing import List

# deps
from loguru import logger
from flask import redirect, url_for, session

# app imports
from .db import get_redis

REDIS_USER_PREFIX = 'justify:user:'


def check_user(f):
    """ Decorator: redirects user to new_user page
    if the user is unknown.
    """
    @wraps(f)
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


def user_voted(songuri: str, uid=None):
    """ Add URI to list of songs voted on, for given userid. """
    if uid is None:
        userid = session['userid']

    # get current user data from redis
    r = get_redis()
    rkey = f'{REDIS_USER_PREFIX}{userid}'
    udata = r.hmget(rkey, 'votes_current', 'votes_history')

    # append song uri to json lists of voted songs
    def appenduri(arraystr: str) -> str:
        """ Safely append song uri to a json array of strings. """
        array = json.loads(arraystr)
        return json.dumps(array.append(songuri))

    udata['votes_current'] = appenduri(udata['votes_current'])
    udata['votes_history'] = appenduri(udata['votes_history'])

    # put the new data into redis
    r.hmset(rkey, udata)
    logger.debug(f"Updated votelist of {udata['userdata']}")


def clear_uservotes(songuri: str):
    """ Remove uri from all users' 'votes_current' lists. """
    # get all redis keys
    r = get_redis()
    userids = r.scan_iter(f"{REDIS_USER_PREFIX}*")

    for uid in userids:
        # get 'votes_current' field from user entry
        vcurr = r.hmget(uid, 'votes_current')[0]
        assert isinstance(vcurr, bytes)

        if str(songuri) in str(vcurr):
            # if user voted on song, remove the vote
            logger.info(f"Clearing vote {songuri} for user {uid}")
            currlist = json.loads(vcurr[0])
            newvcurr = json.dumps(currlist.remove(songuri))
            assert len(newvcurr) < len(vcurr)
            r.hmset(uid, {'votes_current': newvcurr})
