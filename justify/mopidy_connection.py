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


def in_tracklist(songuri: str):
    """ True if song with uri is in current Mopidy tracklist. """
    return songuri in [t.uri for t in mp.tracklist.get_tracks()]


def queue_song(songuri: str):
    """ Add song to Mopidy tracklist based on Mopidy song uri.  """
    mp.tracklist.add(uri=songuri)
