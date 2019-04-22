
# std lib
from itertools import chain
from typing import List

# deps
from loguru import logger

# app imports
from .jsonrpc import mopidy_post, deserialize_mopidy
from .types import (
    Track,
    SearchResult
)


def get_playback_state() -> dict:
    """ Return playback state. """
    return mopidy_post('core.playback.get_state')


def search_tracks(**kwargs) -> List[Track]:
    """ Call the mopidy search function.
    Kwargs could be one of:
        - artist="death grips"
        - song="get got"
        - any="Sound of Silver"
    """
    logger.info(f"Searching for {str(kwargs)}")

    # get results from mopidy api
    sresult: List[dict] = mopidy_post('core.library.search', **kwargs)

    # deserialize into tree of named tuples
    results: List[SearchResult] = deserialize_mopidy(sresult)

    # concatenate lists of tracks
    tracks = list(chain(*[r.tracks for r in results if r.tracks is not None]))

    return tracks
