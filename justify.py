##
## A democratic http front-end for mpd
##
# TODO:
# make pretty
# move search form to main page
# Spoof prevention - timing?

from __future__ import unicode_literals
from bottle import route, run, post, request, template, redirect, static_file
from mpd import MPDClient
import subprocess

# dictionary of mpd ID : vote counts
votes = {}

# serve static files, not in use atm - might use for images
@route('/static/<filename>')
def server_static(filepath):
    return static_file(filepath, root='/static')

@route('/')
def Root():
    redirect('/list')

###########
# MPD STUFF
client = MPDClient()
client.timeout = 100
client.idletimeout = None
client.connect("localhost", 6600)
client.consume(1)
client.clear() # clear playlist, to avoid key errors with votes dict

##################
# SORTING FUNCTION
# bubble sort, totally broken - not efficient but whatevs
def Sort():
    playlist = client.playlistid() # get nice list of dicts
    swapped = True
    while swapped:
        swapped = False
        for i in range(1,len(playlist)-1): #iterate through playlist, skipping first and last tracks
            song = playlist[i]
            song2 = playlist[i+1]
            print("###SORTING", song["pos"])
            print(song["title"],"VOTES",votes[song["id"]],"ID",song["id"]) 
            if votes[song["id"]] < votes[song2["id"]]:
                print("###MOVING DOWN")
                client.move(int(song["pos"]),int(song["pos"])+1)
                #swapped = True

##############
#PLAYLIST PAGE
#Shows the playlist in the current order, w/ vote buttons
@route('/list')
def List():
    plist = client.playlistid() # get nice list of dicts
    return template('list', plist=plist, votes=votes)

@post('/list')
def Vote():
    voteid = request.POST.get('voteID')
    votes[voteid] += 1
    print("votes",votes)
    Sort()
    redirect('/list')

#############
# SEARCH PAGE, deprecated, delet soon
#@route('/search')
#def SearchForm():
#    # clear the vars, not sure if necessary
#    inputsong=""
#    inputartist=""
#    inputalbum=""
#    return template('search')

@post('/search')
def Search():
    searchany = request.forms.get('inputany')
    global result
    result = client.search("title",searchany)
    result += client.search("artist",searchany)
    redirect('/search/result')

#####################
# SEARCH RESULTS PAGE
@route('/search/result')
def SearchResults():
    return template('result', result=result)

@post('/search/result')
def Add(uri=None):
    if uri is None:
        uri = request.POST.get('URI')
    songid = client.addid(uri)
    votes[songid] = 1
    # play song if paused
    status = client.status()
    if status["state"] != "play":
        client.play()
    print("ADDED:", songid)
    redirect('/list')

# add some songs for quick debug
#Add("spotify:track:781V2Y5LPtcpgONEOadadE") # get got
#Add("spotify:track:444S3nPLefAIyQ0HphvRzx") # TAKYOON
#Add("spotify:track:7iupjrZvckPcvC4aeqeqcC") # Autechre
#Add("spotify:track:1gYn6OTpw5W6n8QaJjyY5m") # Nobody speak

run(host='localhost', port=9999)
