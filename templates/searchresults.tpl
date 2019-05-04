{% extends 'base.tpl' %}
			<!-- Header text -->
			<div class="page-header">
				<div class="btn-toolbar float-right">
					<div class="btn-group">
						<a class="btn btn-secondary" href="/">
							<ion-icon name="refresh"></ion-icon>
						</a>
					</div>
				</div>
			</div>

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

						<td>{{ track.artist }}</td>

						<td class="d-none d-sm-table-cell">{{ track.album }}</td>

						<td class="d-none d-sm-table-cell">{{ track.time }}</td>

						<td> <!-- Add button -->
							<form action="/vote/{{ track.uri }}" method="POST">
								<button class="btn btn-secondary" type="submit">
									<span class="mdi mdi-plus"></span>
								</button> 
							</form>
						</td>
					</tr>
				{% endfor %}

			</tbody>
		</table> <!-- table -->
	</div> <!-- /container -->
{% endblock %}
