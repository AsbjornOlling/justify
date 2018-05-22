#!/usr/bin/env python

## Justify.py
# A democratic http front-end for Mopidy

# DO I NEED THIS WHAT IS THIS
from __future__ import unicode_literals

# web stuff
from bottle import Bottle
from paste import httpserver # not in use atm

# other app objects
from config import Configuration
from logger import Logger
from model import Model
from controller import Controller
from viewer import Viewer


### App
# just encapsulation for the important objects
class App(Bottle):
    def __init__(self):
        # call bottle contructor
        super(App, self).__init__()

        # utility objects
        self.config = Configuration()
        self.logger = Logger(self, 1)

        # main mvc objects
        self.model = Model(self)
        self.viewer = Viewer(self)
        self.controller = Controller(self)

        # assign directories to functions
        self.set_routes()

        # RUN SHIT!
        self.logger.log(1, "Starting Justify.")
        self.run(server='paste', host=self.config.host, port=self.config.port)


    def set_routes(self):
        """ Assigns web directories to functions """
        self.route('/', method="GET", callback=self.controller.route_request)
        self.route('/<path>', ["GET","POST"], callback=self.controller.route_request)


if __name__ == "__main__":
    app = App()
