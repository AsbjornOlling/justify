<!-- Displays playlist from mpd

#TODO:
d-->

<ul>
	% for song in plist:
		<li>TRACK: {{song["title"]}}<br>
			ARTIST: {{song["artist"]}}
	  	<form action="/list" method="post"> <input type="submit" name="Vote" value="Vote"> </form>
    </li>
	% end
</ul>
<a href="add">Add another song?</a>
