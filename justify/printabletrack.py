""" Justify types.

Contains the types used only internally in Justify,
and functions to create them properly.
"""

# std lib
from typing import Iterable
from collections import namedtuple

# deps
from flask import session
from loguru import logger

# app imports
from .vote import get_votelist

# justify objects (not to be deserialed from api)
PrintableTrack = namedtuple(
    'PrintableTrack',
    ['uri',
     'name',
     'album',
     'artist',
     'time',
     'votes',
     'canvote'])


def printable_tracks(ts: Iterable) -> Iterable[PrintableTrack]:
    """ Basically make every value a string,
    and the time be in MM:SS format.
    Also this is a generator.
    """
    # get list of votes (tuples, cast to dict)
    vdict = dict(get_votelist(withscores=True))
    for t in ts:
        # ensure that t is Track
        t = t.track if type(t).__name__ == 'TlTrack' else t
        assert type(t).__name__ == 'Track'

        # format into PrintableTrack
        yield PrintableTrack(
            uri=t.uri,
            album=t.album.name,

            # truncate to 40 chars
            name=t.name if len(t.name) < 40 else f"{t.name[:40]}...",

            # join with comma if multiple artists
            artist=", ".join([a.name for a in t.artists]),

            # convert millis -> mm:ss str
            time="{mins}:{secs}".format(
                mins=t.length // 60_000,
                secs=str((t.length // 1000) % 60).zfill(2)
            ),

            # no of votes
            votes=vdict.get(t.uri, 0),

            # whether requesting user has already voted
            canvote=t.uri not in session.get('voted', [])
        )
