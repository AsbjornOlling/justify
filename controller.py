
from bottle import get, request, response

### Controller
# class that handles all incoming requests,
# and calls the appropriate methods in other classes
class Controller():
    def __init__(self, parent):
        # other app ojbects
        self.parent = parent
        self.model = parent.model
        self.viewer = parent.viewer

        # utility objects
        self.logger = parent.logger

        # done
        self.logger.log(3, "Instantiated Controller object")


    def get_any(self, path=None):
        """ Any GET request routes through here.
        This function checks the cookie for validity,
        then passes the request on.
        """
        if self.check_cookie():  # check cookie
            # GET /
            if path == None:
                page = self.get_root()
            else:
                page = self.viewer.not_found()
        else:  # bad cookie
            page = self.bad_cookie()

        return page


    def post_any(self, path=None):
        """ Any POST request routes through here.
        This function checks the cookie, then passes it on.
        """
        if self.check_cookie():  # check cookie
            if path == "search":
                page = self.post_search()
            elif path == "add":
                page = self.post_add()
            elif path == "vote":
                page = self.post_vote()
            else:
                page = self.viewer.not_found()
        else:  # bad cookie
            page = self.bad_cookie()
        return page


    def get_root(self):
        """ Handle GET for the root dir """
        playlist = self.model.get_playlist()   # get playlist from model
        page = self.viewer.playlist(playlist)  # generate playlist html
        return page


    def post_search(self):
        """ Handle POST requests for /search """
        searchtype = request.forms.get("searchtype")
        results = []

        # Simple Search
        if searchtype == "simple":
            query = request.forms.get("query")
            results = self.model.search(query)

        # Better Search
        elif searchtype == "better":
            results = self.model.better_search([request.forms.get("track"),
                                                request.forms.get("album"),
                                                request.forms.get("artist")])
        # Invalid type
        else:
            self.logger.log(0, "Received bad search type.")
        # generate results page
        page = self.viewer.search(results)
        # send html out
        return page


    def post_add(self):
        """ Handle POST requests for /add """
        songid = request.forms.get("songid")
        cookie = self.get_cookie()
        self.model.add_song(cookie, songid)
        # redirect to main view
        return self.get_root()


    def post_vote(self):
        """ Handle POST requests for /vote """
        songid = request.forms.get("songid")
        cookie = self.get_cookie()
        self.model.vote(cookie, songid)
        return self.get_root()


    def get_cookie(self):
        """ Just return the cookie """
        return request.get_cookie("id")


    def set_cookie(self, cookie):
        """ Set the cookie on the response object """
        response.set_cookie("id", cookie)


    def check_cookie(self):
        """ Passes cookie from request object to the model for validation """
        cookie = self.get_cookie()
        return self.model.validate_cookie(cookie)

    
    def bad_cookie(self):
        """ If an unknown cookie is found
        Must be passed the response object of the request.
        """
        self.logger.log(2, "Reacting to bad cookie state.")
        # make a new client object / cookie
        newcookie = self.model.new_client()
        self.set_cookie(newcookie)
        # show welcome page
        return self.viewer.welcome()
