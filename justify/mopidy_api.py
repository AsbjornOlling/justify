
# std lib
from collections import namedtuple
from typing import List, Dict, String

# deps
from requests import post
from loguru import logger
from werkzeug import abort
from pprint import pprint as print

# exceptions
from json.decoder import JSONDecodeError
from requests.exceptions import ConnectionError

MOPIDY_RPC_URL = 'http://localhost:6680/mopidy/rpc'
Track = namedtuple('Track', ['name', 'album', 'artists', 'length', 'uri'])


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

    # return empty dict if err
    # XXX: Betr
    return {}


def get_playback_state() -> dict:
    """ Return playback state. """
    return mopidy_post('core.playback.get_state')


def search(**kwargs) -> List[Track]:
    """ Call the mopidy search function.
    Kwargs could be one of:
        - artist="death grips"
        - song="get got"
        - any="Sound of Silver"
    """
    # get from mopidy api
    sresult = mopidy_post('core.library.search', **kwargs)

    # parse into Track tuples
    tracks = parse_search_tracks(sresult)

    return tracks


def parse_search_tracks(sresult: List) -> List[Track]:
    """ Take the entire raw json results of a search,
    and parse the "tracks" results into a list of Track tuples. """
    # get just track results
    tracks_raw: list = sresult[1]['tracks']

    # filter dicts keeping only fields in 'Track' tuple
    tracks_refined = [{k: t[k] for k in Track._fields} for t in tracks_raw]

    # build list of Track tuples
    tracks: List[Track] = []
    for trackdict in tracks_refined:
        tracks.append(Track(**trackdict))

    logger.debug(tracks[0])

    return tracks
