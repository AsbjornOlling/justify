"""
This module contains the functions (and a type)
used for processing data before piping it into
Jinja for html rendering.
"""

# std lib
from itertools import chain
from typing import Iterable
from collections import namedtuple

# deps
from loguru import logger
from flask import session, url_for

# app imports
from .users import user_canvote
from .votelist import get_votelist
from .mopidy_connection import mp

# justify objects
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
            canvote=user_canvote(str(t.uri), uid=session.get('userid'))
        )


def coverart(songuri: str) -> str:
    """ Get the cover art for a specific track.
    If there's no coverart, use a default.
    """
    mresult: dict = mp.library.get_images([songuri])
    ims: list = mresult.get(songuri)

    if ims == [] or ims is None:
        # if mopidy has no images, use default
        logger.debug(f"No image got for {songuri}. Using default.")
        return url_for('static', filename='default_coverart.png')

    # otherwise, return uri of the biggest image
    biggest = max(ims, key=lambda i: i.height)
    return biggest.uri
