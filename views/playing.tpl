<!-- Currently playing --> 
<div class="row">

	<!-- Cover art -->
  <div class="col-4">
		% if "coverart" in song.keys():
			% coverart = song.get("coverart")
		% else:
			% coverart = viewer.defaultcoverart
		% end
		<img src="{{ coverart }}"></img>
	</div>

	<!-- Song info -->
  <div class="col-8">
		% title = song.get("title")
		<h4 style="">{{ title }}</h4>

		% artist = song.get("artist")
		<h4 style="">{{ artist }}</h4>

		% album = song.get("album")
		<h4 class="" style="vertical-align: middle;">{{ album }}</h4>

		% duration = str(int(int(song.get("time")) / 60)) + ":" + str(int(song.get("time")) % 60).zfill(2)
		<h4 class="" style="vertical-align: middle;">{{ duration }}</h4>

		% votecount = " " + str(song["votes"])
		<button class="btn btn-outline-secondary disabled">
			<ion-icon class="align-middle" name="thumbs-up"></ion-icon>
			{{ votecount }}
		</button>
	</div>

</div>
