<!DOCTYPE html>
<!-- Displays playlist from mpd -->

<html>
	<head>
		<meta charset="utf-8">
		<title>Justify</title>
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
		<link rel="stylesheet" href="https://bootswatch.com/cyborg/bootstrap.min.css" crossorigin="anonymous">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
	</head>

	<body>
		<nav class="navbar navbar-inverse">
			<div class="navbar-header">
				<a class="navbar-brand" href="/list">
					<i class="glyphicon glyphicon-chevron-left"></i>
					Justify
				</a>
			</div>
		</nav>
		<div class="container text-center">
		<div class="page-header">
			<h3>Specific Search</h3>
		</div>
			<div class="row">
				<div class="hidden-xs col-md-4 col-lg-4"></div>
				<div class="col-xs-12 col-md-4 col-lg-4">
					<form action="/search" method="post">
						<input class="hidden" name="searchtype" value="specific"/>
						<div class="input-group">
							<span class="input-group-addon"><i class="glyphicon glyphicon-music"></i></span>
							<input class="form-control" placeholder="Track title" name="inputsong" type="text" />
						</div>
						<div class="input-group">
							<span class="input-group-addon"><i class="glyphicon glyphicon-user"></i></span>
							<input class="form-control" placeholder="Artist" name="inputartist" type="text" />
						</div>
						<div class="input-group">
							<span class="input-group-addon"><i class="glyphicon glyphicon-cd"></i></span>
							<input class="form-control" placeholder="Album" name="inputalbum" type="text" />
						</div>
						<br>
						<div align="center">
							<button class="btn btn-default" type="submit"><i class="fa fa-search"></i> Search!</button>
						</div>
					</form>
				</div>
				<div class="hidden-xs col-md-4 col-lg-4"></div>
			</div>
		</div> <!-- container -->
	</body>
</html>
