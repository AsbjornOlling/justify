
% include("header.tpl", viewer=viewer)

	<div class="container">
	
		<!-- Header -->
		<div class="page-header">
			<h3>Search Results</h3>
		</div>

		<!-- Table -->
		<table class="table table-striped">

			<!-- Table Header -->
			<thead>	
				<tr>
					<th>Song</th>
					<th>Artist</th>
					<th class="hidden-xs">Album</th>
					<th class="hidden-xs">Length</th>
					<th>Add</th>
				</tr>
			</thead>	

			<!-- Table contents -->
			<tbody>

				<!-- If no results -->
				% if not searchresults:
					<tr>
						<td>Huh, didn't find any tracks matching your search...</td>
						<td/><td/><td/><td/>
					</tr>
					<tr>
						<td>Maybe try <a class="btn btn-sm btn-default" href="/search"><b>Better Search</b></a> instead?</td>
						<td/><td/><td/><td/>
					</tr>
				% end

				<!-- Actual results -->
				% for song in searchresults:
					% # filter out non-track results (artists and albums)
					% if song["file"].split(":")[1] == "track":
						<tr>
							% title = song["title"]
							<td>{{ title }}</td>

							% artist = song["artist"]
							<td>{{ artist }}</td>

							% album = song["album"]
							<td class="hidden-xs">{{ album }}</td>

							% duration = str(int(int(song["time"]) / 60)) + ":" + str(int(song["time"]) % 60).zfill(2)
							<td class="hidden-xs">{{ duration }}</td>

							<!-- Add button -->
							<td>
								<form action="/search/result" method="POST">
									<input type="hidden" name="songID" value="{{song["file"]}}"> 
									<button class="btn btn-default" type="submit">
										<span class="fa fa-plus"></span>
									</button> 
								</form>
							</td>
						</tr>
					% end  # track filtering
				% end    # for loop
			</tbody>
		</table> <!-- table -->

	</div> <!-- /container -->

% include("footer.tpl", viewer=viewer)
