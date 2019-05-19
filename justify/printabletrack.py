""" Justify types.

Contains the types used only internally in Justify,
and functions to create them properly.
"""

# std lib
from typing import Iterable
from collections import namedtuple
from itertools import chain

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


def get_only_tracks(mdata: Iterable) -> Iterable:
    """ Get list of Track tuples from any Mopidy type. """
    elementtype = type(mdata[0]).__name__
    if elementtype == 'Track':
        ts = mdata

    elif elementtype == 'SearchResult':
        # each searchresult contains a list of tracks
        ts = [sr.tracks for sr in mdata if 'tracks' in sr._fields]
        logger.debug(mdata[0].tracks)
        logger.debug(mdata[0].tracks)
        logger.debug(mdata[0].tracks)
        if len(ts) > 1:
            ts = chain(*ts)

    elif elementtype == 'TlTrack':
        # each track contains a track
        ts = [tl.track for tl in mdata]

    else:
        # unforeseend type
        err = f"Unexpected type: {elementtype}"
        logger.error(err)
        raise ValueError(err)

    # assert that it went well
    finaltype = type(ts[0]).__name__
    assert ts != [] and finaltype == 'Track', f"Got {finaltype} from {elementtype}"
    return ts


@logger.catch()
def printable_tracks(mdata: Iterable) -> Iterable[PrintableTrack]:
    """ Basically make every value a string,
    and the time be in MM:SS format.
    Also this is a generator.
    """
    # get list of votes (tuples, cast to dict)
    vdict = dict(get_votelist(withscores=True))

    # ensure that data is list of Tracks
    ts = get_only_tracks(mdata)

    for t in ts:
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
