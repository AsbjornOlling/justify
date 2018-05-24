	% # html head + navbar
	% include("header.tpl", viewer=viewer)

		<div class="container">

			<!-- Header text -->
			<div class="page-header">
				<div class="btn-toolbar float-right">
					<div class="btn-group">
						<a class="btn btn-secondary" href="/">
							<ion-icon name="refresh"></ion-icon>
						</a>
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
							<th class="d-none d-sm-table-cell">Album</th>
							<th class="d-none d-sm-table-cell">Time</th>
							<th>Votes</th>
						</tr>
					</thead>


					<!-- Table contents -->
					<tbody>
						<!-- Currently playing song -->

						% # handle empty playlist
						% if playlist:
							<tr class="table-success">

								% title = playlist[0].get("title")
								<td style="vertical-align: middle;">{{ title }}</td>

								% artist = playlist[0].get("artist")
								<td style="vertical-align:middle;">{{ artist }}</td>

								% album = playlist[0].get("album")
								<td class="d-none d-sm-table-cell" style="vertical-align: middle;">{{ album }}</td>

								% duration = str(int(int(playlist[0].get("time")) / 60)) + ":" + str(int(playlist[0].get("time")) % 60).zfill(2)
								<td class="d-none d-sm-table-cell" style="vertical-align: middle;">{{ duration }}</td>

								% votecount = " " + str(playlist[0]["votes"])
								<td style="vertical-align: middle;">
									<button class="btn btn-outline-secondary disabled">
										<ion-icon class="align-middle" name="thumbs-up"></ion-icon>
										{{ votecount }}
									</button>
								</td>
							</tr>
						% end


						<!-- Remaining songs -->
						% for song in playlist[1:]:
							<tr>

								% title = song["title"]
								<td style="vertical-align: middle;">{{ title }}</td>

								% artist = song["artist"]
								<td style="vertical-align: middle;">{{ artist }}</td>

								% album = song["album"]
								<td class="d-none d-sm-table-cell" style="vertical-align: middle;">{{ album }}</td>

								% duration = str(int(int(song["time"]) / 60)) + ":" + str(int(song["time"]) % 60).zfill(2)
								<td class="d-none d-sm-table-cell" style="vertical-align: middle;">{{ duration }}</td>

								<!-- Vote button -->
								<td class="align-middle">
									<form action="/vote" method="post" style="vertical-align: middle;">

										% songid = song["file"]
										<input type="hidden" name="songid" value="{{ songid }}"> 

										% votecount = " " + str(song["votes"])
										% buttonstate = "" if song["buttonstate"] else "disabled"
										<button class="btn btn-outline-success {{ buttonstate }}"  style="vertical-align: middle;" type="submit">
											<ion-icon class="align-middle" name="thumbs-up"></ion-icon>
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
