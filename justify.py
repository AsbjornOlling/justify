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
votes = {"song1":0,"song2":0,"song3":0}
# ordered playlist; is sorted anew on every vote or add
# plist = ["song1","song2"]

###################
# MOPIDY STUFF
client = MPDClient()
client.timeout = 100
client.idletimeout = None
client.connect("localhost", 6600)
client.consume(1)

###########
#PAGE STUFF
#Shows the playlist in the current order, w/ vote buttons
@route('/list')
def List():
    plist = client.playlistid()
    print(plist)
    return template('list', plist=plist)

#sort the playlist, doesnt work now; only makes one pass
# should be deprecated
def bubble():
    buffer = ""
    for i in range(0,len(plist) - 1):
        title1 = plist[i]
        title2 = plist[i + 1]
        if songs[title1] < songs[title2]:
            buffer = title1
            plist[i] = title2
            plist[i + 1] = title1
            print("Swapped something!")
        else:
            print("Swapped nothing!")

#Deprecated
# Add vote to the song bank and (bubble)sort the playlist again
@post('/vote/<title>')
def VoteButton(title="none"):
    songs[title] += 1
    bubble()
    redirect("/list")

# Search page
@route('/search')
def SearchForm():
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

@route('/search/result')
def SearchResults():
# for debug
#    for i in result:
#        print(i)
    return template('result', result=result)

@post('/search/result')
def Add(): #TODO: add to songbank,
    uri = request.POST.get('URI')
    songid = client.addid(uri)
    votes[songid] = 0
    print(songid, "added")

run(host='localhost', port=9999)
