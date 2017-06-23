<!DOCTYPE html>
<!-- Displays results of search
Shows only single tracks from spotify
#TODO:
Add spotify album art from pyspotify or spotipy
-->
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
		<div class="container">
		<div class="page-header">
			<h3>Search Results</h3>
		</div>
			<table class="table table-striped">
				<thead>	
					<tr>
						<th>Song</th>
						<th>Artist</th>
						<th class="hidden-xs">Album</th>
						<th class="hidden-xs">Length</th>
						<th>Add</th>
					</tr>
				</thead>	
				<tbody>
					% if not result:
						<tr>
							<td>Huh, didn't find any tracks matching your search...</td>
							<td/><td/><td/><td/>
						</tr>
						<tr>
							<td>Maybe try <button class="btn btn-sm btn-default" href="/search">specific search</button> instead?</td>
							<td/><td/><td/><td/>
						</tr>
					% end
					% for song in result:
						% if song["file"][:14] == "spotify:track:":
							<tr>
								<td>{{song["title"]}}</td>
								<td>{{song["artist"]}}</td>
								<td class="hidden-xs">{{song["album"]}}</td>
								<td class="hidden-xs">{{int(int(song["time"]) / 60)}}:{{str(int(song["time"]) % 60).zfill(2)}}</td>
								<td>
									<form action="/search/result" method="POST">
										<input type="hidden" name="URI" value="{{song["file"]}}"> 
										<button class="btn btn-default" type="submit"><span class="fa fa-plus"></span></button> 
									</form>
								</td>
							</tr>
						% end
					% end
				</tbody>
			</table>
		</div>
	</body>
<html>
