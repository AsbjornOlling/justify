""" vote.py

WIP: this module handles voting on songs
"""

# std lib
from typing import List

# deps
from loguru import logger
from flask import session

# app imports
from .db import get_redis
from .mopidy_api.playlist import get_playlist


def vote(songuri: str):
    """ Vote on a song by its Mopidy uri.
        - check if already in redis playlist
        - if not in redis, add with one vote
        - if in redis, increment with one vote
    """
    red = get_redis()

    # add vote to track
    # adds it to the list if not already on.
    red.zincrby('playlist_votes', songuri, 1)
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
    red = get_redis()
    rplist = red.zrange('playlist_votes', 0, -1)

    # TODO: algorithm for sorting mopidy
    rplist, mplist


def vote_and_sort(songuri: str):
    """ Function name says it all. """
    vote(songuri)
    sort_mopidy()
