
from bottle import get

### Controller
# class that handles all incoming requests,
# and calls the appropriate methods in other classes
class Controller():
    def __init__(self, parent):
        self.parent = parent
        self.model = parent.model
        self.viewer = parent.viewer


    # handle GET for the server root
    @get('/')
    def get_root(self):
        # get and check cookie
        cookie = request.get_cookie("id")
        if self.model.validate_cookie(cookie):
            # if the cookie is valid, show list
            page = self.viewer.playlist()

        else:
            # if no cookie found, make one
            newcookie = self.model.new_client()
            response.set_cookie("id", newcookie)
            # show welcome page
            page = self.viewer.welcome()

        #return template(tplpath+'front', delay=delay, header=header)
        return page
