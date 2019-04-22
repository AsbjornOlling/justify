""" Mopidy API Types

This module contains the named tuples needed
to deserialize the results from e.g. a search.
"""

from collections import namedtuple


Track = namedtuple('Track', ['uri', 'name', 'album', 'artists', 'length'])
Album = namedtuple('Album', ['uri', 'name', ])
Artist = namedtuple('Artist', ['uri', 'name'])

SearchResult = namedtuple('SearchResult', ['uri', 'artists', 'tracks', 'albums']) # noqa

MopidyTypes = {
    'SearchResult': SearchResult,
    'Track':        Track,
    'Album':        Album,
    'Artist':       Artist
}
