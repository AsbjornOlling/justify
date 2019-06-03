
# std lib
from typing import List
from functools import wraps

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
from .votelist import vote
from .mopidy_connection import mp, sync_state
from .prettytracks import printable_tracks, coverart
from .users import (
    add_user,
    user_voted,
    add_uservote
)


# flask blueprint (encapsulates web endpoints)
bp = Blueprint('web', __name__,
               url_prefix='/',
               template_folder='templates',
               static_folder='static')


def check_user(f):
    """ Decorator: redirects user to new_user page
    if the user is unknown.
    """
    @wraps(f)
    def decorated_f(*args, **kwargs):
        if 'userid' not in session:
            logger.info('Unknown user. Redirecting to new user endpoint.')
            return redirect(url_for('web.new_user'))
        return f(*args, **kwargs)
    return decorated_f


@bp.route('/newuser', methods=['GET', 'POST'])
def new_user():
    """ The page a user hits, if he/she hasn't used the site yet. """
    if request.method == 'POST' and request.form.get('username') is not None:
        # get username from html form
        username = request.form.get('username')
        logger.info(f"User submitted: {username}")
        # TODO: username sanitization

        # add user to db, get unique id
        userid = add_user(username)

        # put unique id into session cookie and redirect
        session['userid'] = userid
        return redirect(url_for('web.playlist_view'))

    # username welcome page
    return render_template('newuser.tpl')


@check_user
@bp.route('/', methods=['GET'])
def playlist_view():
    """ Playlist view. """
    logger.info("Serving playlist view.")

    # get playlist from mopidy
    mlist = mp.tracklist.get_tracks()
    if len(mlist) == 0:
        return render_template('empty.tpl')

    # make pretty track tuples (also get votecount, TODO: fix 'canvote')
    plist = printable_tracks(mlist)

    # top of list is currently playing track
    current = next(plist)

    # render html
    return render_template('playlist.tpl',
                           playlist=plist,
                           current=current,
                           imageurl=coverart(current.uri))


@check_user
@bp.route('/vote/<string:songuri>', methods=['POST'])
def vote_view(songuri: str):
    """ Voting.
    TODO: redirect on HTTP GET
    """
    if user_voted(songuri, uid=session['userid']):
        logger.warning(f"User already voted on: {songuri}. Disallowing vote.")

    else:  # vote allowed
        logger.info(f"Vote on {songuri} deemed valid.")

        # record user vote (to prevent re-vote)
        add_uservote(songuri, uid=session['userid'])

        # add song to mopidy if not in tracklist already
        if str(songuri) not in [str(t.uri) for t in mp.tracklist.get_tracks()]:
            mp.tracklist.add(uri=songuri)

        # increment (or add) in votelist
        vote(songuri)

        # order in mopidy
        sync_state()

    # redirect to playlist
    return redirect(url_for('web.playlist_view'))


@check_user
@bp.route('/search', methods=['GET'])
def search_view():
    """ Return search result tracks.
    Takes GET parameters like ?query=Louis Armstrong
    """
    # get ?query=<something> param
    squery = request.args.get('query')
    if len(squery) == 0:
        logger.debug("Attempted empty search. Redirecting to list view.")
        return redirect(url_for('web.playlist_view'))

    # do mopidy search for it
    logger.info(f"Searching for: {squery}")
    tracks = mp.library.search(any=[squery])

    # put tracks in printable format
    ptracks = printable_tracks(tracks)

    # render html search results
    return render_template('searchresults.tpl', tracks=ptracks)
