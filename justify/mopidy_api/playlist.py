""" playlist.py
Functions to report back about the state of mopidy
"""
# std lib
from typing import List

# deps
from loguru import logger

# app imports
from .jsonrpc import mopidy_post
from .types import deserialize_mopidy


def get_playlist():
    logger.info("Getting playlist from mopidy...")
    mplist = mopidy_post('core.tracklist.get_tl_tracks')

    # parse into named tuples (from .types)
    plist = deserialize_mopidy(mplist)
    return plist
