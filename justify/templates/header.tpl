<html>
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">

		<!-- TODO: inject header -->
		<title>Justify</title>

		<!-- TODO: stop using web resources -->
		<link rel="stylesheet" href="https://bootswatch.com/4/cyborg/bootstrap.min.css" crossorigin="anonymous">
		<link rel="stylesheet" href="https://cdn.materialdesignicons.com/3.6.95/css/materialdesignicons.min.css" crossorigin="anonymous">

		<!-- css patch: center in tables -->
		<style> .table > tbody > tr > td { vertical-align: middle; } </style>
	</head>
	<body>
		<!-- Top navbar -->
		<nav class="navbar navbar-inverse bg-dark container">

				<!-- Header -->
				<div class="navbar-header">
					<a class="navbar-brand" style="font-weight: 700;"  href="/">Justify</a>
				</div>

				{% block searchbar %}
				<!-- Search -->
				<form class="form-inline input-group my-auto" style="width: 66%;" action="/search" method="get">
					<input class="form-control" placeholder="Search" name="query" type="text" />

					<div class="input-group-append">
						<button class="btn btn-outline-primary" type="submit">
							<span class="mdi mdi-magnify"></span>
						</button>
					</div>
				</form> <!-- /inline search -->
				{% endblock %}

		</nav> <!-- /navbar -->

		<br> <!-- dumb spacing is dumb -->
		<br>
