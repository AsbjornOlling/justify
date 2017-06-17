##
## A democratic front-end for mopidy.
##

#import youtube_dl
from __future__ import unicode_literals
from bottle import route, run, post, request, template, redirect
from mopidy import config, ext, core
from mpd import MPDClient

# initalize dictionary of mpd ID : vote counts
votes = {}

###################
# MOPIDY STUFF
client = MPDClient()
client.timeout = 100
client.idletimeout = None
client.connect("localhost", 6600)
client.consume(1)

##################
# SORTING FUNCTION
# bubble sort, not efficient
def Sort():
    plist = client.playlistid() # get nice list of dicts
    #DEBUGGING
    #print("plist",plist)
    #print("plist length", len(plist))
    print("votes",votes)

    # sorting loop (only kicks in with multiple tracks)
    for i in range(1,len(plist)-1): #iterate through playlist, skipping first and last tracks
        song = plist[i]
        song2 = plist[i+1]
        print("###SORTING###")
        print(song["title"],"VOTES",votes[song["id"]],"ID",song["id"]) 
        print(song)
        if votes[song["id"]] < votes[song2["id"]]:
            client.swapid(song["id"],song2["id"])

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
# SEARCH PAGE
@route('/search')
def SearchForm():
    # clear the vars, not sure if necessary
    inputsong=""
    inputartist=""
    inputalbum=""
    return template('search')

@post('/search')
def Search():
    searchsong = request.forms.get('inputsong')
    searchartist = request.forms.get('inputartist')
    searchalbum = request.forms.get('inputalbum')
    global result
    result = client.search("title", searchsong, "artist", searchartist, "album", searchalbum)
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
    votes[songid] = 0
    # play song if paused
    status = client.status()
    if status["state"] != "play":
        client.play()
    print("ADDED:", songid)
    #redirect('/list') disabled to make temp playlist work

# add some songs for quick debug
#client.clear()
#Add("spotify:track:781V2Y5LPtcpgONEOadadE") # get got
#Add("spotify:track:444S3nPLefAIyQ0HphvRzx") # TAKYOON
#Add("spotify:track:7iupjrZvckPcvC4aeqeqcC") # Autechre
#Add("spotify:track:1gYn6OTpw5W6n8QaJjyY5m") # Nobody speak

run(host='localhost', port=9999)
