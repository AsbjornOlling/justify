

# deps
from requests import post
from loguru import logger
from werkzeug import abort

# exceptions
from json.decoder import JSONDecodeError
from requests.exceptions import ConnectionError

MOPIDY_RPC_URL = 'http://localhost:6680/mopidy/rpc'


def mopidy_post(command: str, *args, **kwargs) -> dict:
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
        logger.info(f"Sending Mopidy RPC: {command}")
        logger.info(f"Sending Mopidy RPC: {rpccmd}")

        # do the HTTP POST to mopidy
        r = post(MOPIDY_RPC_URL,
                 json=rpccmd).json()

        # assert: no errors :^)
        assert 'error' not in r, r.get('error', None)
        return r['result']

    # a whole bunch of error handling
    except AssertionError as ex:
        err = f"Mopidy error: {ex} {helpstr}"
        logger.error(err)
        # abort(500, err)
    except ConnectionError as ex:
        err = f"Mopidy connection error: {ex} {helpstr}"
        logger.error(err)
        # abort(500, err)
    except JSONDecodeError:
        err = f"Got weird response from mopidy. {helpstr}"
        logger.error(err)
        # abort(500, err)

    # return empty dict if err
    # XXX: Betr
    return {}


def get_playback_state() -> dict:
    """ Return playback state. """
    return mopidy_post('core.playback.get_state')


def search(**kwargs) -> dict:
    """ Call the mopidy search function.
    Kwargs could be one of:
        - artist="death grips"
        - song="get got"
        - any="Sound of Silver"
    """
    return mopidy_post('core.library.search', **kwargs)


if __name__ == '__main__':
    print(get_playback_state())
    print(search(artist='death grips'))
