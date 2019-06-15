"""
Manages user data in redis.
This includes:
    - uuid of user
    - chosen username
    - current songs a user has voted on
    - history of all votes
"""

# std lib
import json
from uuid import uuid4
from typing import List

# deps
from loguru import logger
from flask import redirect, url_for, session, g
from werkzeug import abort

# app imports
from .db import get_redis

REDIS_USER_PREFIX = 'justify:user:'


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
    # if cached
    if 'votedlist' in g:
        logger.debug(f"Getting votedlist for {userid} from g cache.")
        return g.votedlist

    try:  # else, get from redis
        logger.debug(f"Getting votedlist for {userid} from redis.")
        rkey = f"{REDIS_USER_PREFIX}{userid}"
        vdata: bytes = get_redis().hmget(rkey, 'votes_current')
        assert len(vdata) == 1
        assert vdata[0] != b'null'
    except Exception as e:
        logger.error(f"Error reading user votes: '{e}' - Resetting user.")
        del session['userid']
        abort(redirect(url_for('web.new_user')))

    # load as python list, cache and return
    vlist: List = json.loads(vdata[0])
    g.votedlist = vlist
    return vlist


def user_voted(songuri: str, uid=None) -> bool:
    """ True if user already voted on song with URI. """
    assert uid is not None
    return songuri in get_user_votedlist(uid)


def user_canvote(songuri: str, uid=None) -> bool:
    """ True if user has not voted on song,
        OR if user is None """
    if uid is None:
        return True
    else:
        return not user_voted(songuri, uid=uid)


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

    # delete old cached list
    if 'votedlist' in g:
        del g.votedlist


def clear_uservotes(songuri: str):
    """ Remove uri from all users' 'votes_current' lists. """
    # get all redis keys
    r = get_redis()
    rkeys = r.scan_iter(f'{REDIS_USER_PREFIX}*')

    for rkey in rkeys:
        # get 'votes_current' field from user entry
        vlist = get_user_votedlist()
        assert isinstance(vlist, list), f"Got votedlist of type {vlist}"

        if songuri in vlist:
            # if user voted on song, remove the vote
            logger.debug(f"Clearing vote {songuri} for user {rkey}")

            # load into list and remove songuri
            newlist = filter(lambda x: x != songuri, vlist)
            assert len(newlist) < len(vlist)

            # dump back into json and update redis
            newliststr: str = json.dumps(list(newlist))
            r.hmset(rkey, {'votes_current': newliststr})

            # remove old list from g cache
            if 'votedlist' in g:
                del g.votedlist
