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

    sessconf = {  # flask session config
        'SESSION_COOKIE_NAME':        'justify',
        'SESSION_COOKIE_SECURE':      True,
        'PERMANENT_SESSION_LIFETIME': timedelta(days=10),
    }
    app.config.update(**sessconf)

    # let users module bind '@before_request' on app obj
    with app.app_context():
        from . import users

    # register web endpoints
    from . import views
    app.register_blueprint(views.bp)

    return app


app = create_app()
