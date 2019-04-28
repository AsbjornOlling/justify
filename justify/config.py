
# std lib
from os import getenv

# deps
from loguru import logger
from flask import Flask
# debug
import pysnooper


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


CONFVARS = {
    'REDIS_ADDR': ('localhost:6379', _validate_REDIS_ADDR),
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
            errmsg = f"Error configuring {k}: {e}"
            defmsg = f"Defaulting to {k}={default}"
            logger.error(errmsg)
            logger.info(defmsg)
            # use default value from CONFVARS
            finalconf[k] = default
        # except Exception as e:
        #     logger.error(f"Something happened: {e}")

    logger.info("Finished reading configuration.")
    return finalconf
