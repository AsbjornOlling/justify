

# deps
from loguru import logger
from flask import Blueprint, request

# app imports
from .mopidy_api import search

bp = Blueprint('web', __name__, url_prefix='/')


# @bp.route('/playlist', methods=['GET'])
# def playlist_view():
#     # return render_template('playlist.tpl')
#     pass
#
# @bp.route('/vote/<str:songid>', methods=['POST'])
# def vote_view(songid: str):
#     # redirect(url_for(playlist_view))
#     pass


@bp.route('/search', methods=['GET'])
def search_view():
    """ x """

    # get ?query=<something> param
    squery = request.args.get('query')
    # TODO: sanitization

    # do mopidy search
    logger.info(f"Searching for: {squery}")
    results = search(artist=squery)

    # return render_template('search.tpl')
    return str(results)
