
# std lib

# deps
from loguru import logger
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    session
)

# app imports
from .users import add_user
from .votelist import vote
from .mopidy_connection import mp
from .printabletrack import printable_tracks


# flask blueprint (encapsulates web endpoints)
bp = Blueprint('web', __name__,
               url_prefix='/',
               template_folder='../templates')


@bp.route('/newuser', methods=['GET', 'POST'])
def new_user():
    # add user if user submitted form
    if request.method == 'POST' and request.get('username') is not None:
        # TODO: username sanitization
        userid = add_user(request.get('username'))
        session['userid'] = userid

    # input username welcome page
    return render_template('newuser.tpl')


@bp.route('/', methods=['GET'])
def playlist_view():
    """ Playlist view. """
    logger.info("Serving playlist view.")

    # get playlist from mopidy
    mlist = mp.tracklist.get_tracks()

    # make printable (also get votecount, vote status based on session)
    plist = printable_tracks(mlist)

    # render html
    return render_template('playlist.tpl', playlist=plist)


@bp.route('/vote/<string:songuri>', methods=['POST'])
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
        votedlist = []

    if songuri in votedlist:
        # if user already voted
        logger.warning(f"User already voted on song: {songuri}")

    else:
        # valid vote
        logger.info(f"Vote on {songuri} deemed valid.")
        session['voted'].append(songuri)
        vote(songuri)
        # TODO: sort playlist

    # redirect to playlist
    return redirect(url_for('web.playlist_view'))


@bp.route('/search', methods=['GET'])
def search_view():
    """ Return search result tracks.
    Takes GET parameters like ?query=Louis Armstrong
    """
    # 1. get ?query=<something> param
    squery = request.args.get('query')

    # 2. do mopidy search for it
    tracks = mp.library.search(any=squery)

    # 3. put tracks in printable format
    ptracks = printable_tracks(tracks)

    # 4. render html search results
    return render_template('searchresults.tpl', tracks=ptracks)
