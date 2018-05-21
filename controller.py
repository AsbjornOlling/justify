
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


    # handle GET for anything but the admin panel
    def get_root(self):
        # get and check cookie
        cookie = request.get_cookie("id")
        if self.model.validate_cookie(cookie):
            playlist = self.model.get_playlist()   # get playlist from model
            page = self.viewer.playlist(playlist)  # generate playlist html
        else:
            # if no cookie found, make one
            newcookie = self.model.new_client()
            response.set_cookie("id", newcookie)
            # show welcome page
            page = self.viewer.welcome()

        # send whichever html out to browser
        return page
