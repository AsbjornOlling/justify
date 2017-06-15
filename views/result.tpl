<!-- Displays songs unsorted 

#TODO:
Add spotify album art from pyspotify or spotipy
-->

<ul>
	% for song in result:
    % if song["file"][:14] == "spotify:track:":
			<li><b>Track:</b> {{song["title"]}} 
			<br>
			<b>Artist:</b> {{song["artist"]}}</li>
			<input type="button" value="Add!" onclick="Add(song['file'])"> 
		% end
	% end
</ul>
