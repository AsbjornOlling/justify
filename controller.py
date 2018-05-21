
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


    def get_root(self):
        """ Handle GET for the root dir """
        if self.check_cookie(request):
            playlist = self.model.get_playlist()   # get playlist from model
            page = self.viewer.playlist(playlist)  # generate playlist html
        else:
            page = self.bad_cookie(response)

        # send whichever html out to browser
        return page


    def post_search(self):
        """ Handle POST requests for /search """
        if self.check_cookie(request):  # check cookie
            searchtype = request.forms.get("searchtype")
            results = []

            # Simple Seearch
            if searchtype == "simple":
                query = request.forms.get("query")
                results = self.model.search(query)

            # Better Search
            elif searchtype == "better":
                searcharray = [ request.forms.get("track"),
                                request.forms.get("album"),
                                request.forms.get("artist") ]
                results = self.model.better_search(searcharray)

            # Invalid POST
            else:
                self.logger.log(0, "Received bad search type.")

            # generate results page
            page = self.viewer.search(results)
        else:
            # if bad cookie
            page = self.bad_cookie(response)

        # send html out
        return page


    def check_cookie(self, request):
        """ Passes cookie from request object to the model for validation """
        cookie = request.get_cookie("id")
        return self.model.validate_cookie(cookie)

    
    def bad_cookie(self, response):
        """ If an unknown cookie is found
        Must be passed the response object of the request.
        """
        # if no cookie found, make one
        newcookie = self.model.new_client()
        response.set_cookie("id", newcookie)
        # show welcome page
        return self.viewer.welcome()
