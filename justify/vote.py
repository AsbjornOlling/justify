""" vote.py

WIP: this module handles voting on songs
"""

# std lib
from typing import List, Tuple

# deps
from loguru import logger

# app imports
from .db import get_redis
from .mopidy_connection import mp


def get_votelist(withscores=False) -> List:
    """ Get list of tracks, sorted by votes
    from Redis layer. Optionally return tuples, containing scores. """
    # get all of 'playlist_votes' from redis
    red = get_redis()
    rlist: List = red.zrange('playlist_votes', 0, -1,
                             withscores=withscores)
    # clean results
    if not withscores:
        # cast to strings
        result: List[str]
        result = [b.decode('utf8') for b in rlist]
    elif withscores:
        # cast to (str, int) tuples
        result: List[Tuple[str, int]]
        result = [(s.decode('utf8'), int(b)) for s, b in rlist]
    return result


# TODO: validate songuri
def vote(songuri: str):
    """ Vote on a song by its Mopidy uri.
        - check if already in redis playlist
        - if not in redis, add to mopidy  # XXX: change?
        - if not in redis, add with one vote
        - if in redis, increment with one vote
    """
    red = get_redis()

    if songuri not in [t.uri for t in mp.tracklist.get_tracks()]:
        # if song is unknown to mopidy, add it to playlist
        mp.tracklist.add(uri=songuri)

    # increment votecount in redis
    # (adds it to the list if not already on)
    red.zincrby('playlist_votes', 1, songuri)
    logger.info(f"Voted on: {songuri}")


def vote_and_sort(songuri: str):
    """ Function name says it all. """
    vote(songuri)
