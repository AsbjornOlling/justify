
{% block content %}
	<div class="container">
	
		<!-- Header -->
		<div class="page-header">
			<h3>Search Results</h3>
		</div>

		<!-- Table -->
		<table class="table table-striped">
			<!-- Table Legend -->
			<thead>	
				<tr>
					<th>Song</th>
					<th>Artist</th>
					<th class="d-none d-sm-table-cell">Album</th>
					<th class="d-none d-sm-table-cell">Length</th>
					<th>Add</th>
				</tr>
			</thead>	

			<!-- Table Body -->
			<tbody>

				<!-- If no results -->
				{% if not tracks %}
					<tr>
						<td>Huh, didn't find any tracks matching your search...</td>
						<td/><td/><td/><td/>
					</tr>
					<tr>
						<td>Maybe try <a class="btn btn-sm btn-default" href="/bettersearch"><b>Better Search</b></a> instead?</td>
						<td/><td/><td/><td/>
					</tr>
				{% endif %}

				<!-- Actual results -->
				{% for track in tracks %}
					<tr>
						<td>{{ track.name }}</td>

						<td>{{ track.artists }}</td>

						<td class="d-none d-sm-table-cell">{{ track.album.name }}</td>

						<!-- XXX: % duration = str(int(int(song.get("time")) / 60)) + ":" + str(int(song.get("time")) % 60).zfill(2) -->
						<td class="d-none d-sm-table-cell">{{ length }}</td>

						<!-- Add button -->
						<td>
							<form action="/add" method="POST">
								<input type="hidden" name="songid" value="{{ track.uri }}"> 
								<button class="btn btn-secondary" type="submit">
									<ion-icon name="add"></ion-icon>
								</button> 
							</form>
						</td>
					</tr>
				{% endfor %}

			</tbody>
		</table> <!-- table -->
	</div> <!-- /container -->
{% endblock %}
