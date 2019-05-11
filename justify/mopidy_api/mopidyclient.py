
# std lib
import logging
import asyncio
import json
from threading import Thread

# deps
import websockets

# app imports
# from .mopidy_types import deserialize_mopidy
from loguru import logger


class MopidyWSClient:
    """ Mopidy Websocket API Client """
    def __init__(self, ws_url='ws://localhost:6680/mopidy/ws',
                 logger=None):
        # typical, boring constructor stuff
        self.logger = logger if logger else logging.getLogger(__name__)
        self.ws_url = ws_url
        self._event_callbacks = {}

        # check schema
        err = f"{ws_url} doesn't look like a websocket address."
        assert 'wss://' or 'ws://' in ws_url, err

        # start websocket listener thread
        self.logger.info("Creating Mopidy Websocket connection...")
        self.wsthread = Thread(target=self._websocket_runner,
                               args=(asyncio.new_event_loop(),),
                               name="WSListener", daemon=False)
        self.wsthread.start()

    @logger.catch()
    def _websocket_runner(self, loop):
        """ Method to run in websocket handler thread.
        Receives websocket messages using the library 'websockets'.
        Since 'websockets' uses asyncio, it needs an event loop.
        """
        async def packethandler():
            async with websockets.connect(self.ws_url) as ws:
                while True:
                    msg = await ws.recv()
                    self.on_message(msg)

        # run listener forever, reconnect on exceptions
        while True:
            try:
                loop.run_until_complete(packethandler())
            except Exception as e:
                raise e
                self.logger.warning(
                    f"Websocket connection error (reconnecting): {e}")

    def on_message(self, msgstr: str):
        """ Method to be called on every arriving websocket message. """
        logger.debug(f"Websocket received: {msgstr}")
        msg = json.loads(msgstr)
        if 'event' in msg.keys():
            self.route_event(msg)
        else:
            logger.debug(f"Received unknown type packet: {msg}")

    def route_event(self, event: dict):
        """ Pass event data to the functions registered
        in the _event_callbacks dict.
        """
        eventname = event['event']
        logger.debug(f"Routing event: {eventname}")
        callbacks = self._event_callbacks.get(eventname, [])
        for cb in callbacks:
            # TODO: deserialize data
            cb(event)

    def on_event(self, eventname):
        """ Function decorator.
        Decorated function is added to callbacks dict,
        to be called when event arrives.
        TODO: check for invalid/unsupported event names
        """
        def decorator(func):
            """ Appends function to the event callbacks dict. """
            cbs = self._event_callbacks
            existingcallbacks = cbs.get(eventname, [])
            cbs[eventname] = existingcallbacks.append(func)
            return func
        return decorator


if __name__ == '__main__':
    # testing code
    mp = MopidyWSClient(logger=logger)

    @mp.on_event('volume_changed')
    def shoopwoop():
        print("SHOOP DA WOOP")
        print("SHOOP DA WOOP")
        print("SHOOP DA WOOP")
