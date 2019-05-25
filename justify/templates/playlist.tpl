{% extends 'base.tpl' %}

{% block content %}
	<div class="container">

		{# Refresh button #}
		<div class="page-header">
			<div class="btn-toolbar float-right">
				<div class="btn-group">
					<a class="btn btn-secondary" href="/">
						{# TODO: replace ionicon #}
						<ion-icon name="refresh"></ion-icon>
					</a>
				</div>
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
					{# TODO: Currently playing song 
					{% if playlist %}
						% include("playing.tpl", song=playlist[0], viewer=viewer)
					{% endif %} #}

					{# Remaining songs #}
					{% for track in playlist %}
						<tr>
							<td style="vertical-align: middle;">
								{{ track.name }}
							</td>

							<td style="vertical-align: middle;">
								{{ track.artist }}
							</td>

							<td class="d-none d-sm-table-cell" style="vertical-align: middle;">
								{{ track.album }}
							</td>

							<td class="d-none d-sm-table-cell" style="vertical-align: middle;">
								{{ track.time }}
							</td>

							{# Vote button #}
							<td class="align-middle">
								<form action="/vote/{{ track.uri }}" method="POST">
									{# TODO: new icon #}
									<input value="{{ track.votes }}" type="submit" class="btn btn-outline-success {{ "" if track.canvote else "disabled" }}" style="vertical-align: middle;">
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
