##
## A democratic http front-end for mpd
##
# TODO:
# put currently playing track in header
# add no results message to templates
# generate results pages dynamically - test w/ multiple people first
# write admin panel
# write readme.md

from __future__ import unicode_literals
from bottle import route, run, post, request, template, redirect, static_file
from mpd import MPDClient
import time

# dictionary of mpd ID : vote counts
votes = {}
# dictionary of mpd ID : vote times, for spoof prevention
timers = {}
# minimum delay between votes, in seconds
delay = 10

# serve static files, not in use atm - might use for images
@route('/static/<filename>')
def server_static(filepath):
    return static_file(filepath, root='/static')

#redirect to main page
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
client.clear() # clear playlist, to avoid key errors from songs not in votes{}

##################
# SORTING FUNCTION
# bubble sort, totally broken but whatevs
def Sort():
    playlist = client.playlistid() # get nice list of dicts
    swapped = True
    while swapped == True:
        swapped = False
        for i in range(1,len(playlist)-1): #iterate thru playlist, skipping first and last tracks
            song = playlist[i]
            song2 = playlist[i+1]
            if votes[song["id"]] < votes[song2["id"]]:
                client.move(int(song["pos"]),int(song["pos"])+1)
                playlist = client.playlistid() # reload playlist after swap
                swapped = True
                #client.swapid(song["id"],song2["id"])
                #client.swap(song["pos"],song2["pos"])

##############
#PLAYLIST PAGE
#Shows the playlist in the current order, w/ vote buttons
@route('/list')
def List():
    plist = client.playlistid() # get nice list of dicts
    return template('list', plist=plist, votes=votes, timers=timers, delay=delay, time=time)

@post('/list')
def Vote():
    voteid = request.POST.get('voteID')
    votes[voteid] += 1
    timers[voteid] = time.time() # reset timer
    print("votes",votes)
    Sort()
    redirect('/list')

#############
# SEARCH PAGE
# for specific search form
@route('/search')
def SearchForm():
    return template('search')

@post('/search')
def Search():
    global result
    if request.forms.get('searchtype') == "simple":
        print("Doing simple search!")
        searchany = request.forms.get('inputany')
        result = client.search("any",searchany)
    elif request.forms.get('searchtype') == "specific":
        print("Doing specific search!")
        # reset vars to avoid searching for "None"
        searchsong = ""
        searchartist = ""
        searchalbum = ""
        searchsong = request.forms.get('inputsong')
        searchartist = request.forms.get('inputartist')
        searchalbum = request.forms.get('inputalbum')
        result = client.search("title",searchsong,"artist",searchartist,"album",searchalbum)
    else:
        "Something went wrong!"
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
    timers[songid] = time.time() - delay
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
