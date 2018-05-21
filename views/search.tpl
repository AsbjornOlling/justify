<!-- Search -->
<h6>Add your own songs from Spotify:</h6>
<form action="/search" method="post">
	<div class="input-group">

		<!-- Search type hidden field -->
		<input class="hidden" name="searchtype" value="simple"/>

		<!-- Search field -->
		<input class="form-control" placeholder="Input either the song title [OR] the artist" name="query" type="text" />

		<!-- Button -->
		<span class="input-group-btn">
			<button class="btn btn-warning" type="submit">
				<span class="fa fa-search"></span>
			</button>
		</span>

	</div> <!-- /input group -->
</form>

<br>

<br>

<div align="right">
	<a class="btn btn-default" href="/search">...or use <b>Better Search</b></a>
</div>
<!-- Search section done -->
