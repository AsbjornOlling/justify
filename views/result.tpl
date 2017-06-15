<!-- Displays songs unsorted 

#TODO:
Add spotify album art from pyspotify
-->

<ul>
	% for song in result:
		<li>Song title: {{song["title"]}} Artist: {{song["artist"]}}</li>
	% end
	<a href="add">Add another song?</a>
</ul>
