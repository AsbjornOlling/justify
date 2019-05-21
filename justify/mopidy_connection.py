""" Maintains a connection to mopidy
Encpasulates the mopidy object.
"""

# deps
from mopidyapi import MopidyAPI
from loguru import logger

# app imports
from .votelist import remove_from_votelist

# MopidyAPI
# provides functions and event listeners
# defaults to connecting to localhost
try:
    # TODO: make mopidy url configurable
    mp = MopidyAPI(logger=logger)
except ConnectionError:
    logger.error("Fatal error: could not establish connection to Mopidy."
                 " Are you sure Mopidy is running and accessible?")


@mp.on_event('track_playback_ended')
def track_playback_ended(event):
    """ Removes track from votelist
    when mopidy finishes playing it.
    """
    logger.debug(f"Track playback ended: {event}")
    remove_from_votelist(event.track.uri)


@mp.on_event('tracklist_changed')
def tracklist_changed(event):
    logger.debug(f"Trackist changed: {event}")
    pass
