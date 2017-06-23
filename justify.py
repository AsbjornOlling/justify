#
## Justify.py
# A democratic http front-end for Mopidy
#
# TODO:
# rewrite front page
# make release + 2820.camp branch
# write admin panel
# allow more than just spotify results
# switch away from development server - test w/ multiple people first
# generate results page dynamically - test w/ multiple people first

from __future__ import unicode_literals
from bottle import route, run, post, request, template, redirect, static_file, auth_basic, parse_auth
from paste import httpserver # not in use atm
from mpd import MPDClient
import time
import configparser
import sys
import os.path
from passlib.hash import sha256_crypt

# dictionary of mpd ID : vote counts
votes = {}
# dictionary of mpd ID : vote times, for spoof prevention
timers = {}

# Set paths
relpath = os.path.dirname(sys.argv[0]) # path relative to shell dir
abspath = os.path.abspath(relpath) # absolute path of script
confpath = abspath + "/config.txt" # config file path
stapath = abspath + "/static" #static server path
tplpath = abspath + "/views/" #html templates path
print("Paths set.")

###############
# CONFIGURATION
config = configparser.RawConfigParser()
config.read(confpath)
# http section
host = config.get("http", "host")
port = config.getint("http","port")
# mpd section
mpdhost = config.get("mpd", "host")
mpdport = config.getint("mpd","port")
# other section
delay = config.getint("other","delay")
admin_uri = config.get("other","admin_uri")
print("Configuration loaded.")

# MPD SETTINGS
client = MPDClient()
client.timeout = 100
client.idletimeout = None
client.connect(mpdhost, mpdport)
client.consume(1)
print("MPD connection established.")

# SORTING FUNCTION
# Runs on every vote and add. Sorts the song by bubble sort
def Sort():
    playlist = client.playlistid() # get nice list of dicts
    swapped = True
    while swapped == True:
        swapped = False
        for i in range(1,len(playlist)-1): #iterate thru playlist, skipping first and last tracks
            print("Sorting song nr. %i" % i)
            song = playlist[i]
            song2 = playlist[i+1]
            if votes[song["id"]] < votes[song2["id"]]:
                client.move(int(song["pos"]),int(song["pos"])+1)
                playlist = client.playlistid() # reload playlist after swap
                swapped = True
    print("Completed sorting.")

# REGISTER FUNCTION
# Triggered from list.tpl, adds a song to the dicts if not there. (for songs from other front-ends)
def Register(songid):
    votes[songid] = 0
    timers[songid] = time.time()
    print("Found and registered an unknown song.")

# STATIC FILE SERVER
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=stapath)

# FRONT PAGE
@route('/')
def Root():
    print("Serving front page.")
    return template(tplpath+'front',delay=delay)

#PLAYLIST PAGE
#Shows the playlist in the current order, w/ vote buttons
@route('/list')
def List():
    print("Serving playlist page.")
    plist = client.playlistid() # get nice list of dicts
    return template(tplpath+'list', plist=plist, votes=votes, timers=timers, delay=delay, time=time, Register=Register)

@post('/list')
def Vote():
    voteid = request.POST.get('voteID')
    votes[voteid] += 1
    timers[voteid] = time.time() # reset timer
    print("Received vote.")
    Sort()
    redirect('/list')

# SEARCH PAGE
# for specific search form
@route('/search')
def SearchForm():
    print("Serving specific search page")
    return template(tplpath+'search')

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

# SEARCH RESULTS PAGE
@route('/search/result')
def SearchResults():
    print("Serving search results page")
    return template(tplpath+'result', result=result)

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
    print("Added a song.")
    redirect('/list')

# ADMIN PAGE totally incomplete
def Delete(id="None"):
    if not id == "None":
        client.deleteid(id)

@route(admin_uri)
def AdminPanel():
    return template(tplpath+'admin', plist=plist, votes=votes, timers=timers, delay=delay, time=time, Register=Register)

run(host=host, port=port)
