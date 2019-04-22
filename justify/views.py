
# std lib

# deps
from loguru import logger
from flask import Blueprint, request, render_template

# app imports
from .mopidy_api.search import search_tracks


# flask blueprint (encapsulates endpoints)
bp = Blueprint('web', __name__,
               url_prefix='/',
               template_folder='../templates')


# @bp.route('/playlist', methods=['GET'])
# def playlist_view():
#     # return render_template('playlist.tpl')
#     pass
#
#
# @bp.route('/vote/<str:songid>', methods=['POST'])
# def vote_view(songid: str):
#     # redirect(url_for(playlist_view))
#     pass


@bp.route('/search', methods=['GET'])
def search_view():
    """ Return search result tracks. """

    # get ?query=<something> param
    squery = request.args.get('query')

    # do mopidy api search
    tracks = search_tracks(any=squery)

    # render html search results
    return render_template('searchresults.tpl', tracks=tracks)
