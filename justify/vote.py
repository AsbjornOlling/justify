""" vote.py

WIP: this module handles voting on songs
"""

# std lib
from typing import List, Tuple

# deps
from loguru import logger

# app imports
from .db import get_redis
from .mopidy_api.playlist import get_playlist, add_uri


def get_votelist(withscores=False):
    """ Get list of tracks, sorted by votes
    from Redis layer. Optionally return tuples, containing scores. """
    # get all of 'playlist_votes' from redis
    red = get_redis()
    rlist: List = red.zrange('playlist_votes', 0, -1,
                             withscores=withscores)
    # clean results
    if not withscores:
        # cast to strings
        result: List[str] = [str(b) for b in rlist]
    elif withscores:
        # cast to (str, int) tuples
        result: List[Tuple[str, int]] = [(str(s), int(b)) for s, b in rlist]
    return result


# TODO: validate songuri
def vote(songuri: str):
    """ Vote on a song by its Mopidy uri.
        - check if already in redis playlist
        - if not in redis, add with one vote
        - if in redis, increment with one vote
    """
    red = get_redis()

    # if it's a new song, add it to mopidy
    if songuri.encode('utf8') not in get_votelist():
        # queue song in mopidy
        add_uri(songuri)

    # increment votecount in redis
    # (adds it to the list if not already on)
    red.zincrby('playlist_votes', 1, songuri)
    logger.info(f"Voted on: {songuri}")


def sort_mopidy():
    """ TODO: Sorting.
    Sort by mopidy_api calls.
        - get playlist from mopidy_api
        - plan efficient actions to sort playlist
        - send actions to mopidy
        - get playlist again, check state
    """
    # get playlist from mopidy
    mplist = get_playlist()

    # get sorted list of song uris from redis
    vlist = get_votelist()

    # TODO: algorithm for sorting mopidy
    # if in redis, but not mopdiy
    vlist, mplist


def vote_and_sort(songuri: str):
    """ Function name says it all. """
    vote(songuri)
    sort_mopidy()
