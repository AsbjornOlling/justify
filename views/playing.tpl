<!-- Currently playing --> 
		% title = song.get("title")
		<h2 style="vertical-align: middle;">{{ title }}</h2>

		% artist = song.get("artist")
		<h2 style="vertical-align:middle;">{{ artist }}</h2>

		% album = song.get("album")
		<h2 class="d-none d-sm-table-cell" style="vertical-align: middle;">{{ album }}</h2>

		% duration = str(int(int(song.get("time")) / 60)) + ":" + str(int(song.get("time")) % 60).zfill(2)
		<h2 class="d-none d-sm-table-cell" style="vertical-align: middle;">{{ duration }}</h2>

		% votecount = " " + str(song["votes"])
		<button class="btn btn-outline-secondary disabled">
			<ion-icon class="align-middle" name="thumbs-up"></ion-icon>
			{{ votecount }}
		</button>
