# std lib
from datetime import timedelta
from time import sleep

# deps
from loguru import logger
from flask import Flask
from requests import get

# app imports
from . import config


def wait_for_mopidy(mopidyhost):
    """ Send HTTP to mopidy until it responds """
    # wait for mopidy to come up
    while True:
        try:
            r = get(f"http://{mopidyhost}")
            if r.status_code == 200:
                break
        except Exception:
            logger.warning(f"Mopidy seems down at address: {mopidyhost}"
                           " Trying to connect...")
            sleep(2)
    logger.debug("Mopidy seems to be up.")


def create_app() -> Flask:
    """ Factory function.
    Returns Flask app object. """
    logger.info("Starting Justify...")

    # make flask app
    app = Flask(__name__, static_url_path='/static')

    # read config into flask from env and file
    conf = config.load_config()
    app.config.update(**conf)

    sessconf = {  # flask session cookie config
        'SESSION_COOKIE_NAME':        'justify',
        'PERMANENT_SESSION_LIFETIME': timedelta(days=2)
    }
    app.config.update(**sessconf)

    # wait for mopidy to come up
    # (b/c the mopidy docker image is a liar)
    wait_for_mopidy(conf['MOPIDY_HOST'])
    with app.app_context():
        # set mopidy options right
        from .mopidy_connection import fix_mopidy_options
        fix_mopidy_options(None)

    # register web endpoints
    with app.app_context():
        from . import views
    app.register_blueprint(views.bp)

    return app


app = create_app()
