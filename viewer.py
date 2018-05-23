# library imports
from bottle import get, template, static_file

### Viewer
# Class responsible for handling template files,
# and sending html out to the clients
class Viewer():
    def __init__(self, parent):
        self.parent = parent
        self.model = parent.model
        self.config = parent.config
        self.logger = parent.logger

        # read config
        self.path = self.config.viewspath
        self.headertext = self.config.headertext
        self.theme = self.config.theme


    def welcome(self):
        """ Introduction page.
        Only shown to users with no valid cookie.
        """
        return template(self.path + '/welcome.tpl', viewer=self)


    def playlist(self, playlist):
        """ Main playlist page.
        Generates playlist with song info, and vote buttons.
        """
        return template(self.path + '/playlist.tpl', playlist=playlist, viewer=self)


    def search(self, searchresults):
        """ Search results page.
        Generates list of search reults in table,
        with an add button.
        """
        return template(self.path + '/searchresults.tpl', searchresults=searchresults, viewer=self)


    def better_search(self):
        """ Better Search page.
        Search with specific track, artist and album fields
        """
        return template(self.path + '/bettersearch.tpl', viewer=self)


    def not_found(self):
        """ 404 Page """
        return "<h1>404 - Page not found</h1>"


    def get_static(self, filename):
        """ Serve any static files """
        return static_file(filename, root=stapath)


    def stylesheet(self, stylesheet):
        """ Fetch stylesheet """
        self.logger.log(3, "Serving stylesheet" + stylesheet)
        return static_file(stylesheet, root=self.config.csspath)

