## 
## A festify / partify clone, for youtube instead of spotify.
##

from __future__ import unicode_literals
from bottle import route, run, post, request, template, redirect
import youtube_dl

# DEBUGGING STUFF
# print variables and list, not in use
def vars():
    print("PLIST:")
    for title in plist:
        print("title")
    print("Songbank:")

#Debugging page
@route('/debug')
def debug():
    bubble()

# Hello world 
@route('/hello')
def Hello():
    return "Hello world!"
    vars()

# INIT DICTS AND LISTS
# of Title:VoteCount pairs
songs = {"song1":0,"song2":0,"song3":0}
# ordered playlist; is sorted anew on every vote or add
plist = ["song1","song2"]

#PLAYLIST PAGE STUFF
#Shows the playlist in the current order, w/ vote buttons
@route('/list')
def showList():
    return template('list', songs=songs, plist=plist)

#sort the playlist
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

# Add vote to the song bank and (bubble)sort the playlist again
@post('/vote/<title>')
def VoteButton(title="none"):
    songs[title] += 1
    bubble()
    redirect("/list")

##
# YT DL STUFF
# set aside for now
##

# YDL configuration
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
}

#Youtube-url form
@route('/add')
def GetUrl():
    return template('add')

#Download the song, when submit button hit
@post('/add')
def DownloadUrl():
    yt_url = request.forms.get('yt_url')
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])
        meta = ydl.extract_info(yt_url, download=False) 
    title = (meta['title'])
    songs[title] = 0 # adds title to session, w/ no votes
    plist.append("title") # adds the title to the end of the ordered playlist 
    # then return to votes page
    redirect("/list")


run(host='localhost', port=9999)
