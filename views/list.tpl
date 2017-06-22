<!DOCTYPE html>
<!-- Displays playlist from mpd -->

<html>
	<head>
		<meta charset="utf-8">
		<title>DAKKEDAK</title>
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
		<!-- link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous"-->
		<link rel="stylesheet" href="https://bootswatch.com/cyborg/bootstrap.min.css" crossorigin="anonymous">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

	</head>
	<body>
		<nav class="navbar navbar-inverse">
			<div class="navbar-header">
				<a class="navbar-brand" href="/list">Justify</a>
			</div>
		</nav>
		<div class="container">
			<div class="page-header">
				<h3>Current playlist</h3>
			</div>
			<table class="table table-striped table-hover">
				<thead>
					<tr>
						<th>Song</th>
						<th>Artist</th>
						<th class="hidden-xs">Album</th>
						<th>Time</th>
						<th>Votes</th>
					</tr>
				</thead>
				<tbody>
					<tr class="warning">
						% if plist:
							<td>{{plist[0]["title"]}}</td>
							<td>{{plist[0]["artist"]}}</td>
							<td class="hidden-xs">{{plist[0]["album"]}}</td>
							<td>{{int(int(plist[0]["time"]) / 60)}}:{{str(int(plist[0]["time"]) % 60).zfill(2)}}</td>
							<td><button class="btn btn-default disabled"><span class="fa fa-thumbs-up"></span> {{votes[plist[0]["id"]]}}</button>
						% end
					</tr>
				% for song in plist[1:]:
					<tr>
					  <td>{{song["title"]}}</td>
						<td>{{song["artist"]}}</td>
						<td class="hidden-xs">{{song["album"]}}</td>
						<td>{{int(int(song["time"]) / 60)}}:{{str(int(song["time"]) % 60).zfill(2)}}</td>
						<td>
							<form action="/list" method="post"> 
								<input type="hidden" name="voteID" value="{{song["id"]}}"> 
								% if time.time() - timers[song["id"]] < delay or song["pos"] == "0":
								<button class="btn btn-default disabled" type="button"><span class="fa fa-thumbs-up"></span> {{votes[song["id"]]}}</button>
								% else:
								<button class="btn btn-default" type="submit"><span class="fa fa-thumbs-up"></span> {{votes[song["id"]]}}</button>
								% end
							</form>
						</td>
					</tr>
				% end
				</tbody>
			</table>
			<form action="/search" method="post">
				<div class="input-group">
					<input class="hidden" name="searchtype" value="simple"/>
					<input class="form-control" placeholder="Add your own songs from spotify" name="inputany" type="text" />
					<span class="input-group-btn">
						<button class="btn btn-default" type="submit">
							<span class="fa fa-search"></span>
						</button>
					</span>
				</div> <!-- /input group -->
			</form>
			<br>
			<br>
			<div align="right">
				<a class="btn btn-default" href="/search">...or use Specific Search</a>
			</div>
		</div> <!-- /container -->
	</body>
</html>
