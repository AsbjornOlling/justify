<!DOCTYPE html>
<!-- Displays results of search
Shows only single tracks from spotify
#TODO:
Add spotify album art from pyspotify or spotipy
-->
<html>
	<head>
		<meta charset="utf-8">
		<title>DAKKEDAK</title>
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
	</head>
	<body>
		<div class="container">
			<table class="table table-striped">
				<thead>	
					<tr>
						<th>Song</th>
						<th>Artist</th>
						<th>Length</th>
						<th>Add</th>
					</tr>
				</thead>	
				<tbody>
					% for song in result:
						% if song["file"][:14] == "spotify:track:":
							<tr>
								<td>{{song["title"]}}</td>
								<td>{{song["artist"]}}</td>
								<td>{{int(song["time"]) / 60}}:{{str(int(song["time"]) % 60).zfill(2)}}</td>
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
