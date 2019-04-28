
# std lib

# deps
from loguru import logger
from flask import Blueprint, request, render_template, redirect, url_for, session

# app imports
from .mopidy_api.search import search_tracks
from .vote import vote_and_sort


# flask blueprint (encapsulates web endpoints)
bp = Blueprint('web',
               __name__,
               url_prefix='/',
               template_folder='../templates')


@bp.route('/playlist', methods=['GET'])
def playlist_view():
    """ TODO: Playlist view. """
    return render_template('playlist.tpl')


@bp.route('/vote/<str:songuri>', methods=['POST'])
def vote_view(songuri: str):
    """ Voting.
    - one vote per cookie per song
    - vote triggers re-sort
    """
    # get songs already voted on by user
    votedlist = session.get('voted', None)

    if votedlist is None:
        # new list for new users
        logger.info("Init empty voted list for user.")
        session['voted'] = []

    if songuri in votedlist:
        # if user already voted
        logger.warning(f"User already voted on song: {songuri}")

    else:
        # valid vote
        logger.info(f"Vote on {songuri} deemed valid.")
        session['voted'].append(songuri)
        vote_and_sort(songuri)

    # redirect to playlist
    redirect(url_for(playlist_view))


@bp.route('/search', methods=['GET'])
def search_view():
    """ Return search result tracks.
    Takes GET parameters like ?query=Louis Armstrong
    """
    # 1. get ?query=<something> param
    squery = request.args.get('query')

    # 2. do mopidy api search with it
    tracks = search_tracks(any=squery)

    # 3. render html search results
    return render_template('searchresults.tpl', tracks=tracks)
