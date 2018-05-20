	% # html head + navbar
	% include("header.tpl", viewer=viewer)

		<div class="container">

			<!-- Header text -->
			<div class="page-header">
				<div class="btn-toolbar pull-right">
					<div class="btn-group">
						<a class="btn btn-default" href="/list"><i class="fa fa-refresh"></i></a>
					</div>
				</div>
				<h3>
					Current playlist
				</h3>
			</div>

			<!-- Table container -->
			<div class="panel panel-default">
				<table class="table table-striped table-hover">

					<!-- Table header -->
					<thead>
						<tr>
							<th>Song</th>
							<th>Artist</th>
							<th class="hidden-xs">Album</th>
							<th class="hidden-xs">Time</th>
							<th>Votes</th>
						</tr>
					</thead>


					<!-- Table contents -->
					<tbody>
						% # get the playlist
						% playlist = viewer.model.playlist

						<!-- Currently playing songs -->
						<tr class="warning">
								<td>{{ playlist[0]["title"] }}</td>
								<td>{{ playlist[0]["artist"] }}</td>
								<td class="hidden-xs">{{ plist[0]["album"]}}</td>
								<td class="hidden-xs">{{ int(int(plist[0]["time"]) / 60)}}:{{str(int(plist[0]["time"]) % 60).zfill(2)}}</td>
								<td><button class="btn btn-default disabled"><span class="fa fa-thumbs-up"></span> {{votes[plist[0]["id"]]}}</button></td>
						</tr>

						<!-- Remaining songs -->
						<tr>
							<td>{{song["title"]}}</td>
							<td>{{song["artist"]}}</td>
							<td class="hidden-xs">{{song["album"]}}</td>
							<td class="hidden-xs">{{int(int(song["time"]) / 60)}}:{{str(int(song["time"]) % 60).zfill(2)}}</td>
							<td>
								<form action="/list" method="post"> 
									<input type="hidden" name="voteID" value="{{song["id"]}}"> 
									% if time.time() - timers[song["id"]] < delay or song["pos"] == "0":
											button class="btn btn-default disabled" type="button"><i class="fa fa-thumbs-up"></i> {{votes[song["id"]]}}</button>
									% else:
									<button class="btn btn-default" type="submit"><i class="fa fa-thumbs-up"></i>{{votes[song["id"]]}}</button>
									% end
								</form>
							</td>
						</tr>

					</tbody>
				</table>
			</div>
			<!-- Table Done -->

			<!-- Search field -->
			<h6>Add your own songs from Spotify:</h6>
			<form action="/search" method="post">
				<div class="input-group">
					<input class="hidden" name="searchtype" value="simple"/>
					<input class="form-control" placeholder="Input either the song title [OR] the artist" name="inputany" type="text" />
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
				<a class="btn btn-default" href="/search">...or use Better Search</a>
			</div>
			<!-- Search section done -->

		</div> <!-- /container -->

	% include("footer.tpl", viewer=viewer)
