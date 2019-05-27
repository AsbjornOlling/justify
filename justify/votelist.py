""" votelist.py

Functions to manage the votelist,
which is a Redis ZSET.
(which is a list of (songuri, votecount) pairs,
sorted by votes).
"""

# std lib
from typing import List, Tuple

# deps
from loguru import logger

# app imports
from .db import get_redis

# name of votelist in redis
REDIS_VOTELIST = 'justify:votelist'


def get_votelist(withscores=False) -> List:
    """ Get list of tracks, sorted by votes
    from Redis layer. Optionally return tuples, containing scores. """
    # get the votelist from redis
    red = get_redis()
    rlist: List = red.zrange(REDIS_VOTELIST, 0, -1,
                             withscores=withscores)
    # clean results
    if not withscores:
        # cast bytes to strings
        result: List[str]
        result = [b.decode('utf8') for b in rlist]
    elif withscores:
        # cast to (str, int) tuples
        result: List[Tuple[str, int]]
        result = [(s.decode('utf8'), int(b)) for s, b in rlist]
    return result


def vote(songuri: str):
    """ Vote on a song by its Mopidy uri.
        - if not in redis, add with one vote
        - if in redis, increment with one vote
    """
    # increment votecount in redis
    # (adds it to the list if not already on)
    red = get_redis()
    red.zincrby(REDIS_VOTELIST, 1, songuri)
    logger.info(f"Voted on: {songuri}")


def remove_from_votelist(songuri: str):
    """ Remove uri from redis votelist. """
    logger.info(f"Removing song with uri: {songuri}")
    get_redis().zrem(REDIS_VOTELIST, str(songuri))
