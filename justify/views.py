
# std lib
from typing import List

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
from .mopidy_connection import mp
from .users import check_user, add_user, get_user_votedlist, user_voted
from .printabletrack import printable_tracks


# flask blueprint (encapsulates web endpoints)
bp = Blueprint('web', __name__,
               url_prefix='/',
               template_folder='templates',
               static_folder='static')


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
        logger.debug(f"SESSION before: {session}")
        session['userid'] = userid
        logger.debug(f"SESSION after: {session}")
        return redirect(url_for('web.playlist_view'))

    # username welcome page
    return render_template('newuser.tpl')


@bp.route('/', methods=['GET'])
@check_user
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
@check_user
def vote_view(songuri: str):
    """ Voting. """
    # TODO: validate songuri

    # get songs already voted on by user
    votedlist: List[str] = get_user_votedlist(session['userid'])
    logger.debug(votedlist)

    if songuri in votedlist:
        # if user already voted
        logger.warning(f"User already voted on song: {songuri}")

    else:  # vote allowed
        logger.info(f"Vote on {songuri} deemed valid.")

        # record user vote (to prevent re-vote)
        user_voted(songuri, uri=session['uid'])

        # add song to mopidy if not in tracklist already
        if songuri not in [t.uri for t in mp.tracklist.get_tracks()]:
            mp.tracklist.add(uri=songuri)

        # increment (or add) to votelist
        # TODO: sort playlist
        vote(songuri)

    # redirect to playlist
    return redirect(url_for('web.playlist_view'))


@bp.route('/search', methods=['GET'])
@check_user
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
