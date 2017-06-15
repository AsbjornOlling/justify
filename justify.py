## 
## A festify / partify clone, for youtube instead of spotify.
##

#import youtube_dl
from __future__ import unicode_literals
from bottle import route, run, post, request, template, redirect
from mopidy import config, ext, core
from mpd import MPDClient

#################
# DEBUGGING STUFF
# print variables and list, not in use
def vars():
    print("PLIST:")
    for title in plist:
        print("title")
    print("Songbank:")

#Debugging page, not really useful atm..
@route('/debug')
def debug():
    vars()

# Hello world 
@route('/hello')
def Hello():
    return "Hello world!"

#####################
# INIT DICTS AND LISTS
# of ID:VoteCount pairs
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
    print(votes)
    plist = client.playlistid() # nice list of dicts
    swapped = 1 #set so it runs the first time
    while swapped == 1: #only stop when it runs without swapping
        swapped = 0
        for i in range(len(plist)):
            if i < len(plist)-1 and i != 0:
                s1 = plist[i] 
                s2 = plist[i+1]
                if votes[s1["id"]] < votes[s2["id"]]:
                    print("Swapping %s and %s",s1["id"],s2["id"])
                    client.swap(int(s1["id"]),int(s2["id"]))
                    i+=1 #to avoid infinite swapping
                    swapped = 1
    redirect('/list')


##############
#PLAYLIST PAGE
#Shows the playlist in the current order, w/ vote buttons
@route('/list')
def List():
    plist = client.playlistid() # nice list of dicts
    print(plist)
    print(votes)
    return template('list', plist=plist, votes=votes)

@post('/list')
def Vote():
    voteid = request.POST.get('voteID')
    votes[voteid] += 1
    print(votes)
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
# for debug
#    for i in result:
#        print(i)
    return template('result', result=result)

@post('/search/result')
def Add(): #TODO: make song play, if state != playing
    uri = request.POST.get('URI')
    songid = client.addid(uri)
    votes[songid] = 0
    print("Song ID:", songid, "added")
    redirect('/list')

run(host='localhost', port=9999)
