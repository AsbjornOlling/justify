
from bottle import get

### Viewer
# Class responsible for handling template files,
# and sending html out to the clients
class Viewer():
    def __init__(self, parent):
        self.parent = parent
        self.model = parent.model
        self.config = parent.config

        # read config
        self.path = config.viewspath
        self.header = config.header

        # read template files
        self.welcome = template(self.path+'front', header=self.header)


    def welcome(self):
        """ Introduction page """
        return self.welcome





    # serve static files
    def get_static(filename):
        return static_file(filename, root=stapath)
