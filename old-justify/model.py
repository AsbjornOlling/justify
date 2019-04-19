# DEBUGGING SHIT
import pdb

# utility imports
import random

# library imports
from mpd import MPDClient
import pylast

# other application imports
from client import Client


### Model
# This is the class that handles the logic of sorting songs,
# searching for songs, keeping track of identities, and communicating with mpd
class Model():
    # cookie-string : client-object pairs
    clients = {}
    # song-id : votecount pairs
    votes = {}
    # holds the last fetched coverart
    artinfo = ("album title", "coverart url")


    def __init__(self, parent):
        self.parent = parent
        self.config = parent.config
        self.logger = parent.logger
        self.logger.log(3, "Making Model object.")

        # connect to mpd
        self.mpd = MPDClient()
        self.connect_mpd()

        # connect to lastfm
        self.lastfm = self.connect_lastfm()

        # initial playlist (fix votes dict, etc)
        self.playlist = self.get_playlist()

        # read known cookies from file
        self.read_cookies()


    def read_cookies(self):
        """ Read cookies file, and make client object for each. """
        self.logger.log(3, "Reading cookie file.")
        cookiefile = open(self.config.cookiepath, 'r')
        cookies = cookiefile.read().split("\n")
        for cookie in cookies:
            Client(self,cookie)
        cookiefile.close()


    def write_cookie(self, cookie):
        """ Write a string to a file. """
        cookiefile = open(self.config.cookiepath, 'a')
        cookiefile.write(cookie + "\n")
        cookiefile.close()


    def validate_cookie(self, cookie):
        """ Check if the clients cookie is a geniune client-id """
        self.logger.log(3, "Validating cookie")
        if cookie in self.clients:
            return True
        else:
            return False


    def new_client(self):
        """ Generate a new client object.
        Returns a cookie, to be sent to the client.
        """
        client = Client(self)
        cookie = client.cookie
        self.write_cookie(cookie)
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
            self.mpd.consume(1)  # clear each track after playing
            self.logger.log(1, "Connected to MPD instance.")
        except:
            self.logger.log(0, "Failed connecting to MPD.")


    def connect_lastfm(self):
        """ Connect to last.fm.
        Uses api_keys provided by the user, in ther config file.
        """
        if self.config.lastfm_key and self.config.lastfm_secret:
            lastfm = pylast.LastFMNetwork(self.config.lastfm_key, api_secret = 
                                          self.config.lastfm_secret)
        else:
            lastfm = None

        if lastfm:
            self.logger.log(1, "Connected to Last.fm")
        else:
            self.logger.log(0, "Could not connect to Last.fm,")

        return lastfm


    def unpause_mpd(self):
        """ Sends play command to mpd if paused """
        if self.mpd.status().get("state") != "play" and self.playlist:
            self.mpd.play(0)  # play first song on list


    def get_playlist(self, cookie=None):
        """ Gets new playlist information from MPD.
        Should be run each time client loads a playlist.
        """
        self.logger.log(2, "Getting new playlist.")
        self.playlist = self.bubblesort_playlist()  # sort and get playlist

        if self.playlist:
            # process playlist
            self.add_coverart()   # get coverart from last.fm
            self.clear_votes()    # clear old votes
            self.sync_playlist()  # add missing songs to votes,
                                  # & add votecounts to playlist

            # add button states to the playlist
            if cookie: self.get_client_playlist(cookie)

            if self.config.neverpause:
                self.unpause_mpd()  # WHYD THE MUSIC STOP

        return self.playlist


    def get_client_playlist(self, cookie):
        """ Makes a playlist to display for a specific user.
        The user-specifc playlist has a field that controls
        disabling the button, in the html template.
        """
        client = self.clients.get(cookie)
        self.logger.log(2, "Generating buttonstates for client " + client.cookie)
        for song in self.playlist:
            if song["file"] in client.votes:
                # disable button if client voted
                song["buttonstate"] = False
            else:
                # let button stay if untouched
                song["buttonstate"] = True


    def sync_playlist(self):
        """ Sync playlist from MPD with votes dict.
        Add votecounts to playlist, as a new field in each song dict.
        If playlist contains song not in votes dict, add it to votes dict.
        Is called from get_playlist()
        """
        # add votes to playlist
        # add missing songs to votes
        for song in self.playlist:
            songid = song["file"]

            # add songs missing in votes dict
            # (relevant if songs added from another frontend)
            votecount = self.votes.get(songid)
            if votecount is None:
                self.votes[songid] = 1

            # add votecount to dict
            song["votes"] = votecount


    def clear_votes(self):
        """ Clean up the vote dict.
        Reset any voteentries which are no longer in the playlist.
        Is called from get_playlist().
        """
        for votesentry in self.votes:
            if not self.song_in_playlist(votesentry):  # if song missing
                # remove from votes dict
                self.logger.log(2, "Resmoving votes for song: " + votesentry)
                del(self.votes[votesentry])
                # remove clients' records of voting on that song
                for cookie, client in self.clients.items():
                    if votesentry in client.votes:
                        self.logger.log(3, "Removing record of song " + votesentry
                                            + " from client " + client.cookie)
                        client.votes.remove(votesentry)

    
    def add_coverart(self):
        """ Add coverart to current song on the playlist.
        Coverart is gotten from last.fm, if it isn't already set.
        """
        self.logger.log(2, "Checking for cover art update.")

        # get current song
        song = self.playlist[0]
        album = song["album"]
        artist = song["artist"]

        # fetch new album if changed
        if self.artinfo[0] != album and self.lastfm:
            self.logger.log(1, "Album has changed, getting new coverart.")
            coverart = pylast.Album(artist, album, self.lastfm).get_cover_image()
            self.artinfo = (album, coverart)
        elif self.artinfo[0] == album and self.lastfm:
            self.logger.log(1, "Didn't need to update cover art.")

        # put cover art url into playlist
        self.playlist[0]["coverart"] = self.artinfo[1]


    def song_in_playlist(self, songid):
        """ Returns boolean, whether songid is in the current playlist.
        This func does not call get_playlist() and update the playlist,
        because it is being called from get_playlist() (and it would make a
        recursive mess). Remember to call get_playlist() before calling me.
        """
        found = False
        for song in self.playlist:
            if song["file"] == songid:
                found = True
                break
        return found


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
        # search
        self.logger.log(1, "Better Search for " + str(searcharray))
        results = self.mpd.search("title", searcharray[0], "album", searcharray[1], "artist", searcharray[2])
        self.logger.log(3, "Got reults: " + str(results))
        return results


    def add_song(self, cookie, songid):
        """ Add a song to the playlist.
        Takes the cookie of the user who added it,
        and the MPD filename of the song.
        """
        if not self.song_in_playlist(songid):
            # add song to mpd
            self.logger.log(1, "Client " + cookie + " added song " + songid + ".")
            self.mpd.add(songid)
            # make new votes entry
            self.votes[songid] = 0
        else:  # song already added
            self.logger.log(1, "Couldn't add song, " + songid + " is already on playlist. Interpreting as vote.")


    def vote(self, cookie, songid):
        """ Vote on a song from the playlist.
        Takes the cookie of the user who voted,
        and the MPD filename of the song.
        """
        # check if client is allowed to vote
        client = self.clients[cookie]
        if songid not in client.votes:
            # if client has not cast vote yet
            client.register_vote(songid)
            self.votes[songid] = self.votes.get(songid) + 1
            self.logger.log(1, "Client " + client.cookie 
                            + " voted on song " + songid)
        else:  # client has already voted on that song
            self.logger.log(0, "Client " + cookie + " tried voting on a song twice.")


    def bubblesort_playlist(self, level=0):
        """ Bubble-sorts the playlist according to votes.
        It  sorts using bubble sort,
        where every single swap is a "move" call to MPV
        This code is legacy from Justify v1.0:
        """
        swapped = False
        playlist = self.mpd.playlistid()

        # iterate through playlist, skipping first and last tracks
        for i in range(1, len(playlist) - 1):
            # get songs
            s1 = playlist[i]
            s2 = playlist[i+1]

            for s in [s1, s2]:
                if self.votes.get(s["file"]) is None:
                    self.votes[s["file"]] = 0

            # count votes
            votecount = [ self.votes[s["file"]] for s in [s1, s2] ]

            if votecount[0] < votecount[1]:
                # move song1 down
                self.mpd.move(int(s1["pos"]),int(s1["pos"])+1)
                playlist = self.mpd.playlistid() # re-load playlist only after swap
                swapped = True

        # recurse until done
        if swapped:
            self.bubblesort_playlist(level=level + 1)

        # log and fix playlist before exiting
        if level is 0:
            self.logger.log(2, "Sorted playlist.")

        return playlist































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
