<!-- Displays results of search
Shows only tracks - no artists or albums

#TODO:
Add spotify album art from pyspotify or spotipy
-->

<ul>
	% for song in result:
    % if song["file"][:14] == "spotify:track:":
			<li><b>Track:</b> {{song["title"]}} 
			<br>
			<b>Artist:</b> {{song["artist"]}}</li>
			<form action="/search/result" method="POST">
				<input type="hidden" name="URI" value="{{song["file"]}}"> 
				<input type="submit" name="Add" value="Add"> 
			</form>
		% end
	% end
</ul>
