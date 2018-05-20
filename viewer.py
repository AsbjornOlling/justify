
# library imports
from bottle import get, template

### Viewer
# Class responsible for handling template files,
# and sending html out to the clients
class Viewer():
    def __init__(self, parent):
        self.parent = parent
        self.model = parent.model
        self.config = parent.config

        # read config
        self.path = self.config.viewspath
        self.header = self.config.headertext



    def welcome(self):
        """ Introduction page """
        return template(self.path + '/front', header=self.header)





    # serve static files
    def get_static(filename):
        return static_file(filename, root=stapath)
