""" Maintains a connection to mopidy
Encpasulates the mopidy object.
"""

# deps
from mopidyapi import MopidyAPI
from loguru import logger

# mopidy connection object
# provides functions and event listeners
# defaults to connecting to localhost
# TODO: make mopidy url configurable
try:
    mp = MopidyAPI(logger=logger)
except ConnectionError:
    logger.error("Fatal error: could not establish connection to Mopidy."
                 " Are you sure Mopidy is running and accessible?")


