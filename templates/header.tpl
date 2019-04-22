<html>
	<head>
		<meta charset="utf-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">

		<title>GREAT TITLE</title>

		<!-- CSS -->
		<!-- link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous" -->
		<link rel="stylesheet" href="https://bootswatch.com/cyborg/bootstrap.min.css" crossorigin="anonymous">
		<!-- link rel="stylesheet" href="https://bootswatch.com/4/darkly/bootstrap.min.css" crossorigin="anonymous" -->
		<!--link rel="stylesheet" href="/static/css/cyborg.css" crossorigin="anonymous"-->
		<!-- link rel="stylesheet" href="static/css/{{ "viewer.theme" }}.css" crossorigin="anonymous" -->

		<!--  IonIcons -->
		<script src="https://unpkg.com/ionicons@4.1.2/dist/ionicons.js"></script>
		<!-- Fontawesome Icons >
		<script src="https://use.fontawesome.com/e16f25d1a5.js"></script-->

		<!-- Montserrat! -->
		<link href="https://fonts.googleapis.com/css?family=Montserrat" rel="stylesheet">

	</head>

	<!-- Background image -->
	<!-- body style="background-image: url(/static/bg.png); background-size: cover; background-repeat: no-repeat; background-position:; "-->

	<body>

		<!-- Top navbar -->
		<nav class="navbar navbar-inverse bg-light container">

				<!-- Header -->
				<div class="navbar-header">
					<a class="navbar-brand" style="font-family: 'Montserrat', sans-serif; font-weight: 700;"  href="/">{{ "viewer.headertext" }}</a>
				</div>

				<!-- Search -->
				<form class="form-inline input-group my-auto" style="width: 66%;" action="/search" method="post">
					<!-- Search type hidden field -->
					<input class="d-none" name="searchtype" value="simple"/> 

					<!-- Search field -->
					<input class="form-control" placeholder="Search" name="query" type="text" />

					<!-- Button -->
					<div class="input-group-append">
						<button class="btn btn-outline-success" type="submit">
							<ion-icon name="search"></ion-icon>
						</button>
					</div>
				</form>

			</div>
		</nav>

		<br>

		<br>

