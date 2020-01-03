
# std lib
from functools import wraps

# deps
from loguru import logger
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    session,
    g
)

# app imports
from .votelist import vote
from .mopidy_connection import mp, sync_state
from .prettytracks import printable_tracks, coverart
from .users import (
    add_user,
    load_username,
    user_voted,
    add_uservote,
    get_user_votedlist,
)


# flask blueprint (encapsulates web endpoints)
bp = Blueprint('web', __name__,
               url_prefix='/',
               template_folder='templates',
               static_folder='static')


def check_user(force_signup=True):
    """ Decorator: Check that the user is valid.
    If userid is unset or invalid, redirect to new_user page.
    If force_signup is False, let just it slip.
    Load username into flask.g
    """
    def f_decorator(f):

        @wraps(f)
        def decorated_f(*args, **kwargs):
            logger.debug("Checking user...")

            if 'userid' not in session.keys():
                # if no 'userid' in session cookie
                logger.info('No userid found. Redirecting...')
                if force_signup:
                    return redirect(url_for('web.new_user'))

            else:   # we know 'userid' is in session
                try:
                    # load username into flask.g
                    load_username(session['userid'])
                except Exception as e:
                    logger.error(f"User has bad userid: {e}")
                    del session['userid']  # redis doesn't know the id anyway
                    if force_signup:
                        logger.info("Redirecting to new user endpoint")
                        return redirect(url_for('web.new_user'))

            # call original endpoint func, if we made it through
            return f(*args, **kwargs)

        return decorated_f
    return f_decorator


@bp.route('/newuser', methods=('GET', 'POST'))
def new_user():
    """ The page a user hits, if he/she hasn't used the site yet. """
    if request.method == 'POST' and request.form.get('username') is not None:
        # get username from html form
        username = request.form.get('username')
        logger.info(f"User submitted: {username}")
        # TODO: username sanitization

        # add user to redis, get unique id back
        userid = add_user(username)

        # put unique id into session cookie and redirect
        session['userid'] = userid
        return redirect(url_for('web.playlist_view'))

    # username welcome page
    return render_template('newuser.tpl')


@bp.route('/', methods=['GET'])
@check_user(force_signup=False)
def playlist_view():
    """ Playlist view. """
    logger.info("Serving playlist view.")

    # get playlist from mopidy
    mlist = mp.tracklist.get_tracks()
    if len(mlist) == 0:
        return render_template('empty.tpl')

    # get user votes (if signed up)
    if 'username' in g:
        vlist = get_user_votedlist(session['userid'])
    else:
        logger.warning("Making playlist for un-initiated user.")
        vlist = []

    # make pretty track tuples, votecount and all
    plist = printable_tracks(mlist, vlist)

    # render html
    current = next(plist)  # current track is top of list
    return render_template('playlist.tpl',
                           playlist=plist,
                           current=current,
                           imageurl=coverart(current.uri))


@bp.route('/vote/<string:songuri>', methods=['POST', 'GET'])
@check_user()
def vote_view(songuri: str):
    """ Voting. """
    if request.method == 'GET':
        # if user somehow ends up issuing a GET here, just redirect
        return redirect(url_for('web.playlist_view'))

    if user_voted(songuri, uid=session['userid']):
        logger.warning(f"User already voted on: {songuri}. Disallowing vote.")

    else:  # vote allowed
        # TODO: disallow really long songs
        logger.info(f"Vote on {songuri} deemed valid.")

        # add song to mopidy if not in tracklist already
        if str(songuri) not in [str(t.uri) for t in mp.tracklist.get_tracks()]:
            mp.tracklist.add(uri=songuri)

        vote(songuri)          # increment (or add) to votelist
        sync_state()           # put mopidy in order
        add_uservote(songuri,  # record to user data (prevent re-vote)
                     uid=session['userid'])

    # redirect back to playlist
    return redirect(url_for('web.playlist_view'))


@bp.route('/search', methods=['GET'])
@check_user()
def search_view():
    """ Return search result tracks.
    Takes GET parameters like ?query=Louis Armstrong
    """
    # get ?query=<something> param
    squery = request.args.get('query')
    if len(squery.strip(' ')) == 0:
        logger.debug("Attempted empty search. Redirecting to list view.")
        return redirect(url_for('web.playlist_view'))

    # do mopidy search for it
    logger.info(f"Searching for: {squery}")
    tracks = mp.library.search({'any': squery.split(' ')})

    # put tracks in printable format
    votedlist = get_user_votedlist(session['userid'])
    ptracks = printable_tracks(tracks, votedlist)

    # render html search results
    return render_template('searchresults.tpl', tracks=ptracks)
