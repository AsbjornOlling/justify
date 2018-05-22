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
						<!-- Currently playing song -->

						% # handle empty playlist
						% if playlist:
							<tr class="warning">

								% title = playlist[0].get("title")
								<td>{{ title }}</td>

								% artist = playlist[0].get("artist")
								<td>{{ artist }}</td>

								% album = playlist[0].get("album")
								<td class="hidden-xs">{{ album }}</td>

								% duration = str(int(int(playlist[0].get("time")) / 60)) + ":" + str(int(playlist[0].get("time")) % 60).zfill(2)
								<td class="hidden-xs">{{ duration }}</td>

								% votecount = playlist[0]["votes"]
								<td>
									<button class="btn btn-default disabled"><span class="fa fa-thumbs-up"></span>
										{{ votecount }}
									</button>
								</td>
							</tr>
						% end


						<!-- Remaining songs -->
						% for song in playlist[1:]:
							<tr>

								% title = song["title"]
								<td>{{ title }}</td>

								% artist = song["artist"]
								<td>{{ artist }}</td>

								% album = song["album"]
								<td class="hidden-xs">{{ album }}</td>

								% duration = str(int(int(song["time"]) / 60)) + ":" + str(int(song["time"]) % 60).zfill(2)
								<td class="hidden-xs">{{ duration }}</td>

								<!-- Vote button -->
								<td>
									<form action="/vote" method="post"> 

										% songid = song["file"]
										<input type="hidden" name="songid" value="{{ songid }}"> 

										% votecount = song["votes"]
										% buttonstate = "" if song["buttonstate"] else "disabled"
										<button class="btn btn-default {{ buttonstate }}" type="submit">
											<i class="fa fa-thumbs-up"></i>
											{{ votecount }}
										</button>

									</form>
								</td>
							</tr>
						% end

					</tbody>
				</table>
			</div>
			<!-- Table Done -->

			% include("search.tpl", viewer=viewer)


		</div> <!-- /container -->

	% include("footer.tpl", viewer=viewer)
