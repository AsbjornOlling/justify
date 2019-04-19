import sys
import os.path
from configparser import RawConfigParser

### Configuration object
# Just a dumb holder for a bunch of fields
class Configuration(RawConfigParser):
    def __init__(self):
        # run parent class constructor
        super(Configuration, self).__init__()
        self.read_configfile()    # read file
        self.get_configuration()  # load values from file


    def read_configfile(self):
        """ Find and load the configuration file """
        # find path to code dir
        self.relpath = os.path.dirname(sys.argv[0])  # path relative to shell dir
        self.path = os.path.abspath(self.relpath)         # absolute path of script
        self.configpath = self.path+"/config.txt"

        # open config
        self.read(self.configpath)


    def get_configuration(self):
        """ Read the config values """
        # HTTP
        self.host = self.get("http",
                             "host",
                             fallback="0.0.0.0")
        self.port = self.getint("http",
                                "port",
                                fallback="80")
        # MPD
        self.mpdhost = self.get("mpd",
                                "host",
                                fallback="localhost")
        self.mpdport = self.getint("mpd",
                                   "port",
                                   fallback="6600")
        self.neverpause = self.getboolean("mpd",
                                          "neverpause",
                                          fallback="yes")
        self.staticpath = self.path + self.get("paths",
                                               "static_content",
                                               fallback="/static")
        self.viewspath = self.path + self.get("paths",
                                              "templates",
                                              fallback="/views")
        self.csspath = self.path + self.get("paths",
                                            "stylesheets",
                                            fallback="/static/css")
        self.cookiepath = self.path + self.get("paths",
                                               "cookiefile",
                                               fallback="/cookies")
        self.logpath = self.path + self.get("paths",
                                            "logfile",
                                            fallback="/log")
        self.defaultcoverart = self.get("paths",
                                        "default_coverart",
                                        fallback = "static/default_coverart.png")

        # LAST.FM
        self.lastfm_key = self.get("last.fm",
                                   "api_key",
                                   fallback="")
        self.lastfm_secret = self.get("last.fm",
                                      "secret",
                                      fallback="")
        self.lastfm_secret

        # OTHER
        self.theme = self.get("other",
                              "theme",
                              fallback="darkly")
        self.headertext = self.get("other",
                                   "header",
                                   fallback="Justify")
        self.admin_uri = self.get("other",
                                  "admin_uri",
                                  fallback="secretadminpanel")

