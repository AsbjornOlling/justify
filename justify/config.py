"""
Reads an validates configuration variables,
either from environment variables, a (WIP) config file,
or from a default, defined in this module's CONFVARS dict.
"""

# std lib
from os import getenv

# deps
from loguru import logger
from requests import head
from requests.exceptions import ConnectionError, MissingSchema


def _validate_REDIS_ADDR(REDIS_ADDR: str):
    """ Validator for REDIS_ADDR """
    noneerr = f"REDIS_ADDR not set."
    assert REDIS_ADDR is not None, noneerr

    formerr = f"REDIS_ADDR must be in format <host>:<port> Got: {REDIS_ADDR}"
    assert ':' in REDIS_ADDR, formerr

    try:  # check portnum
        portno = int(REDIS_ADDR.split(':')[-1])
        assert portno <= 2**16, "REDIS_ADDR: {porno} is an invalid port number"
    except ValueError:
        raise AssertionError(formerr)
    # TODO: check redis connection


def _validate_SECRET_KEY(SECRET_KEY):
    """ Warn if user hasn't set a key (used for cookie signing). """
    errmsg = (
        "SECRET_KEY not set. Will use default key for cookie signing."
        " You should fix this by setting the SECRET_KEY config option,"
        " if you care about users tampering with your session cookies."
    )
    assert SECRET_KEY is not None, errmsg


def _validate_MOPIDY_RPC_URL(MOPIDY_RPC_URL: str):
    """ Check connection to Mopidy instance. """
    mopurl = MOPIDY_RPC_URL
    # use default if not set
    if mopurl is None:
        mopurl = CONFVARS['MOPIDY_RPC_URL'][0]

    # err in case connect fails
    errmsg = ("Mopidy doesn't seem to be responding right."
              " Justify will likely not work."
              f" Is there a running Mopidy instance at {MOPIDY_RPC_URL}?"
              " You can change this address by setting MOPIDY_RPC_URL.")
    try:  # test connection to mopidy
        r = head(mopurl)
        assert r.status_code == 200, errmsg
    except ConnectionError:
        logger.error(errmsg)
    except AssertionError as e:
        logger.error(errmsg)
        raise e

    # throw assertion error, in order to use default
    raise AssertionError("MOPIDY_RPC_URL not set.")


def _validate_MOPIDY_WS_URL(MOPIDY_WS_URL: str):
    """ Check format of Mopidy Websocket URL """
    # check if set
    assert MOPIDY_WS_URL is not None, "MOPIDY_WS_URL not set."

    # check for schema
    schemerr = "Websocket schema ('ws://') missing from MOPIDY_WS_URL."
    wsscheck = 'wss://' == MOPIDY_WS_URL[:6]
    wscheck = 'ws://' == MOPIDY_WS_URL[:5]
    assert wsscheck or wscheck, schemerr


CONFVARS = {
    'REDIS_ADDR':     ('localhost:6379',
                       _validate_REDIS_ADDR),
    'SECRET_KEY':     ('changeme-you-fool',
                       _validate_SECRET_KEY),
    'MOPIDY_RPC_URL': ('http://localhost:6680/mopidy/rpc',
                       _validate_MOPIDY_RPC_URL),
    'MOPIDY_WS_URL':  ('http://localhost:6680/mopidy/rpc/ws',
                       _validate_MOPIDY_WS_URL)
}


def read_env() -> dict:
    """ Read tracked environment variables into dict """
    logger.info("Reading environment variables...")
    return {k: getenv(k) for k in CONFVARS.keys()}


def read_configfile() -> dict:
    """ TODO: Read config file into dict."""
    logger.info("(Not) Reading config file...")
    return {}


@logger.catch()
def load_config() -> dict:
    """ Read configurations from
    environment varibles and from config file.
    Then validate it all, defaulting if necessary.
    """
    # read confs
    logger.info("Reading configuration...")
    envconf: dict = read_env()
    # fileconf: dict = read_configfile()

    # let file overwrite env
    # readconf = {**envconf, **fileconf}
    readconf = {**envconf}
    assert isinstance(readconf, dict)

    # validate
    finalconf = {}
    for k in CONFVARS.keys():
        # read default value and validator function
        default, validator = CONFVARS[k]

        try:  # validate
            logger.debug(f"Validating {k}...")
            validator(readconf[k])
            finalconf[k] = readconf[k]
        except AssertionError as e:
            errmsg = f"When configuring {k}: {e}"
            defmsg = f"Defaulting to {k}={default}"
            logger.warning(errmsg)
            logger.info(defmsg)
            # use default value from CONFVARS
            finalconf[k] = default
        except Exception as e:
            logger.error(f"Something happened: {e}")

    logger.info("Finished reading configuration.")
    return finalconf
