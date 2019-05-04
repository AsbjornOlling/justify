""" playlist.py
Functions to report back about the state of mopidy
"""
# std lib
from typing import List

# deps
from loguru import logger

# app imports
from .jsonrpc import mopidy_post
from .types import deserialize_mopidy, TlTrack


def get_playlist() -> List[TlTrack]:
    logger.info("Getting playlist from mopidy...")
    mplist = mopidy_post('core.tracklist.get_tl_tracks')

    # parse into namedtuple types (tuples defined in .types)
    plist: List[TlTrack] = deserialize_mopidy(mplist)
    return plist


def add_uri(uri: str):
    """ Add track to Mopidy's currently
    playing tracklist by URI.
    """
    logger.info(f"Adding {uri} to Mopidy playlist.")
    result = mopidy_post('core.tracklist.add', uri=uri)
    logger.debug(f"Got: {result}")
