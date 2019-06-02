""" Maintains a connection to mopidy
Encpasulates the mopidy object.
"""

# deps
from mopidyapi import MopidyAPI
from loguru import logger
from flask import current_app as app
from typing import List, Set

# app imports
from .users import clear_uservotes
from .votelist import (
    remove_from_votelist,
    get_votelist,
    vote
)

# MopidyAPI
# provides functions and event listeners
# defaults to connecting to localhost
try:
    # get address and port from config
    mphost, mpport = app.config['MOPIDY_HOST'].split(':')
    mp = MopidyAPI(host=mphost, port=int(mpport),
                   logger=logger, flask_object=app)
except ConnectionError:
    logger.error("Fatal error: could not establish connection to Mopidy."
                 " Are you sure Mopidy is running and accessible?")
    quit(1)


@mp.on_event('track_playback_ended')
def track_playback_ended(event):
    """ Removes track from votelist and records of user votes,
    when mopidy finishes playing it.
    """
    logger.debug(f"Track playback ended: {event}")
    remove_from_votelist(event.tl_track.track.uri)
    clear_uservotes(event.tl_track.track.uri)


@mp.on_event('options_changed')
def fix_mopidy_options():
    """ Sets the necessary playback options in Mopidy.
    Since setting an option triggers the 'options_changed'
    event, we have to check the option first, to avoid an
    infinite loop.
    """
    # obviously shuffle won't make sense
    if mp.tracklist.get_random() is not False:
        mp.tracklist.set_random(False)

    # remove track from playlist after playing
    if mp.tracklist.get_consume() is not True:
        mp.tracklist.set_consume(True)

    # dont loop tracks
    if mp.tracklist.get_repeat() is not False:
        mp.tracklist.set_repeat(False)

    # dont stop playing after each track
    if mp.tracklist.get_single() is not False:
        mp.tracklist.set_single(False)


def sync_state():
    """ 1. Ensure votelist and Mopidy tracklist contain only the same tracks.
        2. Sort tracklist based on votes.
    This function is called on every vote,
    (TODO should probably be called on some other mopidy event).
    """
    sync_votelist()
    sort_mopidy()


def sync_votelist():
    """ Checks for discrepencies between votelist,
    and the current Mopidy tracklist.
    Modifies votelist to match Mopidy if necessary.
    """
    vlist: Set[str] = set(get_votelist(withscores=False))
    tlist: Set[str] = {str(t.uri) for t in mp.tracklist.get_tracks()}

    vlistonly: Set[str] = vlist - tlist
    for songuri in vlistonly:
        logger.warning(f"Removing orphaned song: {songuri}")
        remove_from_votelist(songuri)
        clear_uservotes(songuri)

    tlistonly: Set[str] = tlist - vlist
    for songuri in tlistonly:
        logger.warning(f"Adding unknown song to votelist: {songuri}")
        vote(songuri)


def sort_mopidy():
    """ Ensure that the Mopidy playlist is ordered
    according to the Justify-controlled votelist.
    This could involve quite a lot of Mopidy calls.
    XXX: this is likely not the most clean / efficient
         implementation possible.
    """
    logger.debug("Sorting Mopidy...")

    vlist: List[str] = get_votelist()        # list of uris in vote order
    tllist = mp.tracklist.get_tl_tracks()    # TlTracks in playlist order
    tlsorted = sorted(tllist, reverse=True,  # TlTracks in vote order
                      key=lambda t: vlist.index(t.track.uri))

    if [str(t.track.uri) for t in tllist] == vlist:
        logger.debug("Songs already in order. Aborting sort.")
        return

    # move all tracks into place (except currently playing)
    for dst, tltrack in list(enumerate(tlsorted))[1:]:
        src = mp.tracklist.index(tl_track=tltrack)
        if src != dst:
            # move track to destination spot on tracklist
            logger.debug(f"Moving track {tltrack.track.uri} to {dst}.")
            mp.tracklist.move(src, src+1, dst)

    # check resulting mopidy order
    finalorder = [str(t.uri) for t in mp.tracklist.get_tracks()]
    if finalorder != vlist:
        # run again, if sort failed
        logger.error("Sort result unsuccessful. Running again...")
        sort_mopidy()
