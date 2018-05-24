<!-- Search -->
<h6>Add your own songs from Spotify:</h6>
<form action="/search" method="post">
	<div class="input-group">

		<!-- Search type hidden field -->
		<input class="d-none" name="searchtype" value="simple"/>

		<!-- Search field -->
		<input class="form-control" placeholder="Search" name="query" type="text" />

		<!-- Button -->
		<span class="input-group-append">
			<button class="btn btn-secondary" type="submit">
				<ion-icon name="search"></ion-icon>
			</button>
		</span>

	</div> <!-- /input group -->
</form>

<div align="right">
	<a class="btn btn-default" href="/bettersearch">...or use <b>Better Search</b></a>
</div>
<!-- Search section done -->
