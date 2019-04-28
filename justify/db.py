
""" Handles connections to Redis """

# deps
from loguru import logger
from flask import current_app as app
from flask import g
from werkzeug import abort
from redis import Redis
from redis.exceptions import ConnectionError


def get_redis():
    """ Connect to Redis instance,
    if there's no connection already in the
    flask 'g' object.
    """
    if 'redis' not in g:
        # connect to redis
        raddr = app.config['REDIS_ADDR']
        rhost = raddr.split(':')[0]
        rport = int(raddr.split(':')[-1])
        try:
            g['redis'] = Redis(host=rhost, port=rport)
            logger.info("Connected to Redis.")
        except ConnectionError as e:
            err = f"Could not connect to Redis: {e}"
            logger.error(err)
            abort(503, err)
    return g.redis
