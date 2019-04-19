
# deps
from loguru import logger
from flask import Flask

# app imports
# from . import config


def create_app() -> Flask:
    """ Factory function.
    Returns Flask app object. """
    logger.info("Starting Justify...")

    app = Flask(__name__,
                static_folder='',
                static_url_path='/static')

    from . import views
    app.register_blueprint(views.bp)

    return app


app = create_app()
