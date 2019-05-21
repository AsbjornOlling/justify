# std lib
from datetime import timedelta

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
    app = Flask(__name__,
                static_folder='',
                static_url_path='/static')

    # read configuration into flask config obj
    conf = config.load_config()
    app.config.update(**conf)

    sessconf = {  # flask session cookie config
        'SESSION_COOKIE_NAME':        'justify',
        'PERMANENT_SESSION_LIFETIME': timedelta(days=10),
        'SECRET_KEY':                 'wow_thats_very_safe',
        # XXX: this breaks cookies
        # 'SESSION_COOKIE_SECURE':     True,
    }
    app.config.update(**sessconf)

    # register web endpoints
    from . import views
    app.register_blueprint(views.bp)

    return app


app = create_app()
