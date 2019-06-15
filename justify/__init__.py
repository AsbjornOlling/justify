# std lib
from datetime import timedelta
from time import sleep

# deps
from loguru import logger
from flask import Flask

# app imports
from . import config


def create_app() -> Flask:
    """ Factory function.
    Returns Flask app object. """
    logger.info("Starting Justify...")

    # make flask app
    app = Flask(__name__, static_url_path='/static')

    # read configuration into flask config obj
    conf = config.load_config()
    app.config.update(**conf)

    sessconf = {  # flask session cookie config
        'SESSION_COOKIE_NAME':        'justify',
        'PERMANENT_SESSION_LIFETIME': timedelta(days=2)
    }
    app.config.update(**sessconf)

    # register web endpoints
    with app.app_context():
        from . import views
    app.register_blueprint(views.bp)

    # check (and fix) mopidy settings
    with app.app_context():
        sleep(5)  # this sleep is shit, but necessary because the mopidy container is a liar
        from .mopidy_connection import fix_mopidy_options
        fix_mopidy_options(None)

    return app


app = create_app()
