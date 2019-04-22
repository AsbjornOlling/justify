""" Mopidy API Types

This module contains the types and methods needed
to deserialize the results from e.g. a mopidy search.
"""

# std lib
from collections import namedtuple
from typing import Dict, List, Iterable, Generator
import time

# deps
from loguru import logger

# types
Track = namedtuple('Track', ['uri', 'name', 'album', 'artists', 'length'])
Album = namedtuple('Album', ['uri', 'name', ])
Artist = namedtuple('Artist', ['uri', 'name'])
SearchResult = namedtuple('SearchResult', ['uri', 'artists', 'tracks', 'albums']) # noqa

PrintableTrack  = namedtuple('PrintableTrack', ['uri', 'name', 'album', 'artist', 'time'])  # noqa

# registry over types
MopidyTypes = {
    'SearchResult': SearchResult,
    'Track':        Track,
    'Album':        Album,
    'Artist':       Artist
}


def deserialize_mopidy(data) -> List:
    """ Recursively turn the structure of mopidy dicts
    into an identical structure with namedtuples.
    """
    # first detect type of data
    if isinstance(data, Dict) and '__model__' in data:
        model = data['__model__']

        # get namedtuple constructor from MopidyTypes dict
        assert model in MopidyTypes, f"Unknown mopidy type: {data}"
        nt = MopidyTypes[model]

        # recurse on dict
        recd = {k: deserialize_mopidy(data.get(k, None)) for k in nt._fields}

        # make tuple
        return nt(**recd)

    elif isinstance(data, List):
        # recurse on list
        return list(map(deserialize_mopidy, data))

    elif isinstance(data, str) or isinstance(data, int):
        # strings and ints should be the only primitives here
        return data

    else:
        logger.error(f"Uncaught type: {type(data)}")


def printable_tracks(tracks: Iterable[Track]) -> Iterable[PrintableTrack]:
    """ Make the first level of children all be strings,
    and the time be in MM:SS format.
    """
    t: Track
    for t in tracks:
        pt = PrintableTrack(
            uri=t.uri,
            name=t.name,
            album=t.album.name,
            artist=", ".join([a.name for a in t.artists]),
            time="{mins}:{secs}".format(
                mins=t.length // 60_000,
                secs=str((t.length // 1000) % 60).zfill(2)
            )
        )
        yield pt
