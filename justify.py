##
## A democratic front-end for mpd
##
## TODO:
# make pretty
# multiple passes in sorting function 
# Spoof prevention

from __future__ import unicode_literals
from bottle import route, run, post, request, template, redirect, static_file
from mpd import MPDClient

# initalize dictionary of mpd ID : vote counts
votes = {}

# serve static files, not used atm - might use for images
@route('/static/<filename>')
def server_static(filepath):
    return static_file(filepath, root='/static')

###################
# MOPIDY STUFF
client = MPDClient()
client.timeout = 100
client.idletimeout = None
client.connect("localhost", 6600)
client.consume(1)

@route('/')
def Root():
    redirect('/list')

def Debug():
    print(votes)

##################
# SORTING FUNCTION
# bubble sort, not efficient but whatevs
def Sort():
    plist = client.playlistid() # get nice list of dicts
    #DEBUGGING
    #print("plist",plist)
    #print("plist length", len(plist))
    print("votes",votes)
    # sorting loop
    for i in range(1,len(plist)-1): #iterate through playlist, skipping first and last tracks
        song = plist[i]
        song2 = plist[i+1]
        print("###SORTING###")
        print(song["title"],"VOTES",votes[song["id"]],"ID",song["id"]) 
        print(song)
        if votes[song["id"]] < votes[song2["id"]]:
            print("Swapping songs:", song["id"], song2["id"])
            client.moveid(song2["id"],int(song2["pos"])-1)

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
    redirect('/list')

# add some songs for quick debug
#client.clear()
#Add("spotify:track:781V2Y5LPtcpgONEOadadE") # get got
#Add("spotify:track:444S3nPLefAIyQ0HphvRzx") # TAKYOON
#Add("spotify:track:7iupjrZvckPcvC4aeqeqcC") # Autechre
#Add("spotify:track:1gYn6OTpw5W6n8QaJjyY5m") # Nobody speak

run(host='localhost', port=9999)
