import random

## Client
# A class to represent client connection, identified by a random string.
# The client keeps track of votes from a user, to prevent voting multiple times.
class Client():
    def __init__(self, model):
        self.model = model

        # generate identifying cookie
        self.cookie = self.gen_id()

        # add to model list
        self.model.clients.append(self)
        self.model.cookies.append(self.cookie)


    def gen_cookie():
        """ Generate random cookie """
        return str(hex(random.getrandbits(128)))[2:]
