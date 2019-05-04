""" Justify types.

Contains the types used only internally in Justify,
and functions to create them properly.
"""

# std lib
from typing import Iterable
from collections import namedtuple

# deps
from flask import session

# app imports
from .mopidy_api.types import Track, TlTrack
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


def printable_tracks(ts: Iterable[Track]) -> Iterable[PrintableTrack]:
    """ Basically make every value a string,
    and the time be in MM:SS format.
    Also this is a generator.
    """
    # get list of votes (tuples, cast to dict)
    vdict = dict(get_votelist(withscores=True))
    for t in ts:
        # ensure that t is Track
        t = t.track if isinstance(t, TlTrack) else t
        assert isinstance(t, Track)

        # construct Track
        yield PrintableTrack(
            uri=t.uri,
            name=t.name if len(t.name) < 40 else t.name[:40] + '...',
            album=t.album.name,
            artist=", ".join([a.name for a in t.artists]),
            time="{mins}:{secs}".format(
                mins=t.length // 60_000,
                secs=str((t.length // 1000) % 60).zfill(2)
            ),
            votes=vdict.get(t.uri, 0),
            canvote=t.uri not in session.get('voted', [])
        )
