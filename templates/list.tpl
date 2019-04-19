% # html head + navbar
% include("header.tpl", viewer=viewer

		<div class="container">
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
			<div class="panel panel-default">
				<table class="table table-striped table-hover">
					<thead>
						<tr>
							<th>Song</th>
							<th>Artist</th>
							<th class="hidden-xs">Album</th>
							<th class="hidden-xs">Time</th>
							<th>Votes</th>
						</tr>
					</thead>
					<tbody>
						% if plist:
							% if votes.get(plist[0]["id"]) == None:
								% Register(plist[0]["id"])
						  % end
						<tr class="warning">
								<td>{{plist[0]["title"]}}</td>
								<td>{{plist[0]["artist"]}}</td>
								<td class="hidden-xs">{{plist[0]["album"]}}</td>
								<td class="hidden-xs">{{int(int(plist[0]["time"]) / 60)}}:{{str(int(plist[0]["time"]) % 60).zfill(2)}}</td>
								<td><button class="btn btn-default disabled"><span class="fa fa-thumbs-up"></span> {{votes[plist[0]["id"]]}}</button></td>
						</tr>
						% end
						% for song in plist[1:]:
							% if votes.get(song["id"]) == None:
								% Register(song["id"])
							% end
						<tr>
							<td>{{song["title"]}}</td>
							<td>{{song["artist"]}}</td>
							<td class="hidden-xs">{{song["album"]}}</td>
							<td class="hidden-xs">{{int(int(song["time"]) / 60)}}:{{str(int(song["time"]) % 60).zfill(2)}}</td>
							<td>
								<form action="/list" method="post"> 
									<input type="hidden" name="voteID" value="{{song["id"]}}"> 
									% if time.time() - timers[song["id"]] < delay or song["pos"] == "0":
										<button class="btn btn-default disabled" type="button"><i class="fa fa-thumbs-up"></i> {{votes[song["id"]]}}</button>
									% else:
									<button class="btn btn-default" type="submit"><i class="fa fa-thumbs-up"></i>{{votes[song["id"]]}}</button>
									% end
								</form>
							</td>
						</tr>
					% end
					</tbody>
				</table>
			</div>
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
		</div> <!-- /container -->
	</body>
</html>
