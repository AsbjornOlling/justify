import random

## Client
# A class to represent client connection, identified by a random string.
# The client keeps track of votes from a user, to prevent voting multiple times.
class Client():
    # list of voted-on songIDs
    votes = []

    def __init__(self, model):
        self.model = model

        # generate identifying cookie
        self.cookie = self.gen_cookie()

        # add to model dictionary
        self.model.clients[self.cookie] = self


    def gen_cookie(self):
        """ Generate random cookie """
        return str(hex(random.getrandbits(128)))[2:]


    def register_vote(self, songid):
        """ Add songid to list of votes """
        self.votes.append(songid)
