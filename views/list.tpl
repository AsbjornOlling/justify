<!-- Displays playlist from mpd

#TODO:
d-->

<ul>
	% for song in plist:
		<li>TRACK: {{song["title"]}}<br>
			ARTIST: {{song["artist"]}}<br>
			VOTES: {{votes[song["id"]]}}
	  	<form action="/list" method="post"> 
				<input type="hidden" name="voteID" value="{{song["id"]}}"> 
				<input type="submit" name="Vote" value="Vote"> 
			</form>
    </li>
	% end
</ul>
<a href="search">Add another song?</a>
