<!-- Displays songs unsorted 

#TODO:
d-->

<ul>
	% for title in plist:
		<li>{{title}} Votes: {{songs[title]}}</li>
		<form action="/vote/{{title}}" method="post"> <input type="submit" name="vote" value="vote"> </form>
	% end
	<a href="add">Add another song?</a>
</ul>
