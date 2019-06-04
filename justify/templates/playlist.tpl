{% extends 'base.tpl' %}

{% block content %}
	<div class="container">

		{# Currently playing #}
		<div class="row" style="">
			<div class="col-4" style=""> {# art #}
				<img style="width: 100%;" class="rounded mx-auto d-block" src="{{ imageurl }}"></img>
			</div>
			<div class="col-8" style="height: auto;">
				<h4>{{ current.name }}</h4>
				<h4>{{ current.artist }}</h4>
				<h4 style="vertical-align: middle;">{{ current.album }}</h4>
				<h4 style="vertical-align: middle;">{{ current.time }}</h4>
				<button class="btn btn-outline-secondary disabled">
					{{ current.votes }}
					<span class="mdi mdi-thumbs-up"></span>
				</button>
			</div>
		</div>

		{# Table container #}
		<div class="panel panel-default">
			<table class="table table-striped table-hover">

				{# Table header #}
				<thead>
					<tr>
						<th>Song</th>
						<th>Artist</th>
						<th class="d-none d-sm-table-cell">Album</th>
						<th class="d-none d-sm-table-cell">Time</th>
						<th>Votes</th>
					</tr>
				</thead>

				{# Table contents #}
				<tbody>
					{# Remaining songs #}
					{% for track in playlist %}
						<tr>
							<td style="vertical-align: middle;">{{ track.name }}</td>
							<td style="vertical-align: middle;">{{ track.artist }}</td>
							<td class="d-none d-sm-table-cell" style="vertical-align: middle;">{{ track.album }}</td>
							<td class="d-none d-sm-table-cell" style="vertical-align: middle;">{{ track.time }}</td>

							{# Vote button #}
							<td class="align-middle">
								<form action="/vote/{{ track.uri }}" method="POST">
									<input value="{{ track.votes }}" type="submit" class="btn btn-outline-success {{ "" if track.canvote else "disabled" }}" style="vertical-align: middle;">
										<span class="mdi mdi-thumbs-up"></span>
									</input>
								</form>
							</td>
						</tr>
					{% endfor %}

				</tbody>
			</table>
		</div> {# /table panel #}
	</div> {# /container #}
{% endblock %}
