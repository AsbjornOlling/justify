
# deps
from loguru import logger
from flask import Flask

# app imports
from . import config
from . import sync


def create_app() -> Flask:
    """ Factory function.
    Returns Flask app object. """
    logger.info("Starting Justify...")

    # duh.. of course?
    app = Flask(__name__,
                static_folder='',
                static_url_path='/static')

    # read configuration
    conf = config.load_config()
    app.config.update(**conf)

    # register web endpoints
    from . import views
    app.register_blueprint(views.bp)

    return app


app = create_app()
