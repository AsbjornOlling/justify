<html>
	{% block head %}
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">

		<title>Justify</title>

		{# TODO: stop using web resources #}
		<link rel="stylesheet" href="{{ url_for('static', filename='css/cyborg.min.css') }}">
		<link rel="stylesheet" href="https://cdn.materialdesignicons.com/3.6.95/css/materialdesignicons.min.css" crossorigin="anonymous">

		{# css patch: center in tables #}
		<style> .table > tbody > tr > td { vertical-align: middle; } </style>
	</head>
	{% endblock %}

	<body>
		{% block navbar %}
		<nav class="navbar navbar-inverse bg-dark container">

			<div class="navbar-header">
				<a class="navbar-brand" style="font-weight: 700;"  href="/">Justify</a>
			</div>

			{% block searchbar %}
			<form class="form-inline input-group my-auto" style="width: 66%;" action="/search" method="get">
				<input class="form-control" placeholder="Search" name="query" type="text" />

				<div class="input-group-append">
					<button class="btn btn-outline-primary" type="submit">
						<span class="mdi mdi-magnify"></span>
					</button>
				</div>
			</form>
			{% endblock %} {# /inline search #}
		</nav>
		{% endblock %}

		<br> {# dumb spacing is dumb #}
		<br>

	{% block content %}
	{% endblock %}

	</body>
</html>
