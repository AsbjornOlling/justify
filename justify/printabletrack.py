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
from .votelist import get_votelist

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


def tracks(mdata: Iterable) -> Iterable:
    """ Get a list of Track tuples, from list of any one Mopidy type.
    E.g. a list of SearchResults, which each have a list of Tracks,
    or a list of TlTracks, each of which contain a single track.
    """
    # find the mopidy tuple type
    mtype = type(mdata[0]).__name__

    # mangle the data based on the type
    if mtype == 'Track':
        ts = mdata

    elif mtype == 'SearchResult':
        # each searchresult contains a list of tracks
        ts = list(chain(*[sr.tracks
                          for sr in mdata
                          if 'tracks' in sr._fields]))

    elif mtype == 'TlTrack':
        # each track contains a track
        ts = [tl.track for tl in mdata]

    else:
        err = f"Unexpected type: {mtype}"
        logger.error(err)
        raise ValueError(err)

    if ts:  # skip empty lists
        # assert that it went well
        testtype = type(ts[0]).__name__
        assert testtype == 'Track', f"Got {testtype} from {mtype}"
    return ts


def printable_tracks(mdata: Iterable) -> Iterable[PrintableTrack]:
    """ Basically make every value a string,
    and the time be in MM:SS format.
    Also this is a generator.
    """
    if mdata in [None, []]:
        return []

    # get list of votes (tuples, cast to dict)
    vdict = dict(get_votelist(withscores=True))

    # ensure that data is list of Tracks
    ts = tracks(mdata)
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
