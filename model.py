# utility imports
import random

# library imports
from mpd import MPDClient

# other application imports
from client import Client


### Model
# This is the class that handles the logic of sorting songs,
# searching for songs, keeping track of identities, and communicating with mpd
class Model():
    clients = []
    cookies = []
    votes = {}


    def __init__(self, parent):
        self.parent = parent
        self.config = parent.config
        self.logger = parent.logger

        # connect to mpd
        self.mpd = MPDClient()
        self.connect_mpd()

        # read known cookies from file
        cookiefile = open(self.config.cookiepath, 'r')
        self.cookies = cookiefile.read().split("\n")


    def validate_cookie(self, cookie):
        """ Check if the clients cookie is a geniune user-id """
        if cookie in self.cookies:
            return True
        else:
            return False


    def new_client(self):
        """ Generate a new client object.
        Returns a cookie, to be sent to the client.
        """
        client = Client(self)
        cookie = client.cookie
        self.logger.log(2, "Made new client object.")
        return cookie


    def connect_mpd(self):
        """ Connect to the mpd server, 
        ensuring the right settings when connected.
        """
        # some settings
        self.mpd.timeout = 100
        self.mpd.idletimeout = None
        try:  # connecting
            self.mpd.connect(self.config.mpdhost, self.config.mpdport)
            self.logger.log(1, "Connected to MPD instance.")
            self.mpd.consume(1)  # clear each track after playing
        except:
            self.logger.log(0, "Failed connecting to MPD.")


    def get_playlist(self):
        """ Gets new playlist information from MPD.
        Should be run each time the user loads a playlist.
        """
        self.logger.log(2, "Getting new playlist")
        self.playlist = self.mpd.playlistid()  # ordered list of dicts

        for song in self.playlist:
            songid = song["file"]

            # fix songs with no votes entry
            votecount = self.votes.get(songid)
            if votecount is None:
                self.votes[songid] = 0

            # add votecount to dict
            song["votes"] = votecount

        return self.playlist


    def search(self, searchstring):
        """ MPD "Any"-search with just one string. """
        if searchstring is None:
            searchstring = ""
        self.logger.log(1, "Simple search for " + searchstring)
        results = self.mpd.search("any", searchstring)
        self.logger.log(3, "Received results: " + str(results))
        return results


    def better_search(self, searcharray):
        """ Search with separate track/album/artist fields """
        # replace None with empty string
        searcharray = ["" for x in searcharray if x is None]

        # search
        self.logger.log(1, "Better Search for " + str(searcharray))
        results = mpd.search("title", searcharray[0], "album", searcharray[1], "artist", searcharrray[2])
        self.logger.log(3, "Got reults: " + str(results))
        return results




















    ###############################
    ### CODE PULLED FROM LEGACY ###
    ### NOT YET PROCESSED ###

#    # SORTING FUNCTION
#    # Runs on every vote and add. sorts the song by bubble sort
#    def sort():
#        playlist = client.playlistid() # get nice list of dicts
#        swapped = True
#        while swapped:
#            swapped = False
#            for i in range(1,len(playlist)-1): #iterate thru playlist, skipping first and last tracks
#                print("sorting song nr. %i" % i)
#                song = playlist[i]
#                song2 = playlist[i+1]
#                if votes[song["id"]] < votes[song2["id"]]:
#                    client.move(int(song["pos"]),int(song["pos"])+1)
#                    playlist = client.playlistid() # reload playlist after swap
#                    swapped = True
#        print("Completed sorting.")
#
#
#    # REGISTER FUNCTION
#    # Triggered from list.tpl, adds a song to the dicts if not there. (for songs from other front-ends)
#    def register(songid):
#        votes[songid] = 0
#        timers[songid] = time.time()
#        print("Found and registered an unknown song.")
#
#
#    #PLAYLIST PAGE
#    #Shows the playlist in the current order, w/ vote buttons
#    @route('/list')
#    def list():
#        print("Serving playlist page.")
#        plist = client.playlistid() # get nice list of dicts
#        return template(tplpath+'list', header=header, plist=plist, votes=votes, timers=timers, delay=delay, time=time, register=register)
#
#
#    @post('/list')
#    def vote():
#        voteid = request.POST.get('voteID')
#        votes[voteid] += 1
#        timers[voteid] = time.time() # reset timer
#        print("Received vote.")
#        sort()
#        redirect('/list')
#
#    # SEARCH PAGE
#    # for specific search form
#    @route('/search')
#    def search_form():
#        print("Serving specific search page")
#        return template(tplpath+'search', header=header)
#
#
#    # SEARCH RESULTS PAGE
#    @route('/search/result')
#    def search_results():
#        print("Serving search results page")
#        return template(tplpath+'result', header=header, result=result)
#
#    @post('/search/result')
#    def add(uri=None):
#        if uri is None:
#            uri = request.POST.get('URI')
#        songid = client.addid(uri)
#        votes[songid] = 1
#        timers[songid] = time.time() - delay
#        # play song if paused
#        status = client.status()
#        if status["state"] != "play":
#            client.play()
#        print("added a song.")
#        sort()
#        redirect('/list')
#
#    # ADMIN PAGE totally incomplete
#    @route(admin_uri)
#    def admin_panel():
#        print("Serving admin panel.")
#        plist = client.playlistid() # get nice list of dicts
#        return template(tplpath+'admin', header=header, plist=plist, votes=votes, timers=timers, delay=delay, time=time, register=register, admin_uri=admin_uri)
#
#    @post(admin_uri)
#    def admin_actions():
#        if request.forms.get('actionType') == "delete":
#            deleteID = request.forms.get('deleteID')
#            client.deleteid(deleteID)
#            print("Deleting ID: %s" % deleteID)
#            redirect(admin_uri)
#        elif request.forms.get('actionType') == "vote":
#            voteID = request.forms.get('voteID')
#            if request.forms.get('votedirection') == "down":
#                votes[voteID] -= 1
#            elif request.forms.get('votedirection') == "up":
#                votes[voteID] += 1
#            elif request.forms.get('votedirection') == "420":
#                votes[voteID] = 420
#            sort()
#            redirect(admin_uri)
#        else:
#            print("Something went wrong.")
#
#
