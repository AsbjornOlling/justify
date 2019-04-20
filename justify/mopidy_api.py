
# std lib
from itertools import chain
from collections import namedtuple
from typing import List, Dict, NamedTuple

# deps
from requests import post
from loguru import logger
from werkzeug import abort

# exceptions
from json.decoder import JSONDecodeError
from requests.exceptions import ConnectionError

MOPIDY_RPC_URL = 'http://localhost:6680/mopidy/rpc'

SearchResult = namedtuple('SearchResult', ['uri', 'artists', 'tracks', 'albums'])
Track = namedtuple('Track', ['uri', 'name', 'album', 'artists', 'length'])
Album = namedtuple('Album', ['uri', 'name', ])
Artist = namedtuple('Artist', ['uri', 'name'])
MopidyTypes = {
    'SearchResult': SearchResult,
    'Track':        Track,
    'Album':        Album,
    'Artist':       Artist
}


def mopidy_post(command: str, *args, **kwargs):
    """ Call the Mopidy HTTP JSON RPC API """
    helpstr = """Check that MOPIDY_RPC_URL is set right
                 and that Mopidy is running and accessible."""

    # assemble rpc command
    rpccmd = {'jsonrpc': '2.0',
              'id': 1,
              'method': command}
    if kwargs:
        rpccmd['params'] = kwargs
    elif args:
        rpccmd['params'] = list(args)

    try:
        logger.debug(f"Sending Mopidy RPC: {rpccmd}")

        # do the HTTP POST to mopidy
        r = post(MOPIDY_RPC_URL,
                 json=rpccmd).json()

        # assert: no errors :^)
        assert 'error' not in r, r.get('error', None)
        logger.debug("Got Mopidy response.")
        return r['result']

    # a whole bunch of error handling
    except AssertionError as ex:
        err = f"Mopidy error: {ex}"
        logger.error(err)
        # abort(500, err)
    except ConnectionError as ex:
        err = f"Mopidy connection error: {ex} {helpstr}"
        logger.error(err)
        # abort(500, err)
    except JSONDecodeError:
        err = f"Got weird response from mopidy url. {helpstr}"
        logger.error(err)
        # abort(500, err)


def deserialize_mopidy(data):
    """ Recursively turn the structure of mopidy dicts
    into an identical structure with namedtuples.
    """
    # first detect type of data
    if isinstance(data, Dict) and '__model__' in data:
        model = data['__model__']
        logger.debug(f"Deserialzing {model}.")

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

    elif isinstance(data, str):
        # strings should be the only primitives here
        return data

    else:
        logger.error(f"Uncaught type: {type(data)}")


def get_playback_state() -> dict:
    """ Return playback state. """
    return mopidy_post('core.playback.get_state')


@logger.catch
def search(**kwargs) -> List[Track]:
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
    tracks = chain(*[r.tracks for r in results if r.tracks is not None])

    return list(tracks)


def parse_search_tracks(sresult: List) -> List[Track]:
    """ XXX: Bugged legacy function. Replaced by deserialization.
    Take the entire raw json results of a search,
    and parse the "tracks" results into a list of Track tuples. """
    # get just track results
    tracks_raw: list = sresult[1]['tracks']

    # filter dicts keeping only fields in 'Track' tuple
    tracks_refined = [{k: t[k] for k in Track._fields} for t in tracks_raw]

    # build list of Track tuples
    tracks: List[Track] = []
    for trackdict in tracks_refined:
        logger.debug(trackdict)
        tracks.append(Track(**trackdict))

    return tracks
