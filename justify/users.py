"""
Manages known users in Redis.
"""

# std lib
import json
from functools import wraps
from uuid import uuid4
from typing import List

# deps
from loguru import logger
from flask import redirect, url_for, session
from werkzeug import abort

# app imports
from .db import get_redis

REDIS_USER_PREFIX = 'justify:user:'


def check_user(f):
    """ Decorator: redirects user to new_user page
    if the user is unknown.
    """
    @wraps(f)
    def decorated_f(*args, **kwargs):
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


def get_user_votedlist(userid: str) -> List[str]:
    """ Get list of song uris voted on by user. """
    logger.debug(f"Getting votedlist for {userid}")

    try:
        # get json from redis
        rkey = f"{REDIS_USER_PREFIX}{userid}"
        vdata: bytes = get_redis().hmget(rkey, 'votes_current')
        assert len(vdata) == 1
        assert vdata[0] != b'null'
    except Exception as e:
        logger.error(f"Error reading user votes: '{e}' - Resetting user.")
        del session['userid']
        abort(redirect(url_for('web.new_user')))

    # load as python list, check and return
    logger.debug(f"VDATA: {vdata}")
    vlist: List = json.loads(vdata[0])
    logger.debug(f"VLIST: {vlist}")
    return vlist


def user_voted(songuri: str, uid=None) -> bool:
    """ Return True if user already voted on song with URI. """
    assert uid is not None
    return songuri in get_user_votedlist(uid)


def add_uservote(songuri: str, uid=None):
    """ Add URI to list of songs voted on, for given userid. """
    # fall back to session info if not explicity passed
    userid = uid if uid is not None else session['userid']

    # get current user data from redis
    r = get_redis()
    rkey = f'{REDIS_USER_PREFIX}{userid}'
    current, history = r.hmget(rkey, 'votes_current', 'votes_history')

    # append song uri to json lists of voted songs
    def appenduri(arraystr: str) -> str:
        """ Safely append song uri to a json array of strings. """
        array = json.loads(arraystr)
        array.append(songuri)
        return json.dumps(array)

    udata = {
        'votes_current': appenduri(current),
        'votes_history': appenduri(history)
    }

    # put the new data into redis
    r.hmset(rkey, udata)
    logger.debug(f"Recorded vote from user {userid}")


def clear_uservotes(songuri: str):
    """ Remove uri from all users' 'votes_current' lists. """
    # get all redis keys
    r = get_redis()
    rkeys = r.scan_iter(f"{REDIS_USER_PREFIX}*")

    for rkey in rkeys:
        # get 'votes_current' field from user entry
        vcurr = r.hmget(rkey, 'votes_current')[0]
        assert isinstance(vcurr, bytes)

        if str(songuri) in str(vcurr):
            # if user voted on song, remove the vote
            logger.debug(f"Clearing vote {songuri} for user {rkey}")
            currlist = json.loads(vcurr[0])
            newvcurr = json.dumps(currlist.remove(songuri))
            assert len(newvcurr) < len(vcurr)
            r.hmset(rkey, {'votes_current': newvcurr})
