import sys
import os.path
import configparser

### Configuration object
# Just a dumb holder for a bunch of fields
class Configuration():
    def __init__(self):
        self.set_paths()
        self.read_config()


    # set paths
    def set_paths(self):
        relpath = os.path.dirname(sys.argv[0])     # path relative to shell dir
        abspath = os.path.abspath(relpath)         # absolute path of script
        self.configpath = abspath + "/config.txt"  # config file path
        self.staticpath = abspath + "/static"      # static server path
        self.viewspath = abspath + "/views"        # html templates path
        self.logpath = abspath + "/log"            # logfile
        self.cookiepath = abspath + "/cookies"     # previously dealt cookies


    def read_config(self):
        """ Read the config file """
        parser = configparser.RawConfigParser()
        parser.read(self.configpath)
        # http section
        self.host = parser.get("http", "host")
        self.port = parser.getint("http","port")
        # mpd section
        self.mpdhost = parser.get("mpd", "host")
        self.mpdport = parser.getint("mpd","port")
        # other section
        self.admin_uri = parser.get("other","admin_uri")
        self.headertext = parser.get("other","header")
