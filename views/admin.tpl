<!DOCTYPE html>
<!-- Displays playlist from mpd -->

<html>
	<head>
		<meta charset="utf-8">
		<title>{{header}}</title>
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
		<link rel="stylesheet" href="https://bootswatch.com/cyborg/bootstrap.min.css" crossorigin="anonymous">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

	</head>
	<body>
		<nav class="navbar navbar-inverse">
			<div class="navbar-header">
				<a class="navbar-brand" href="/list">{{header}}</a>
			</div>
		</nav>
		<div class="page-header">
			<h3>Admin panel</h3>
		</div>
		<table class="table table-striped table-hover">
			<thead>
				<tr>
					<th>Song</th>
					<th>Artist</th>
					<th>Delete</th>
					<th>Votes</th>
				</tr>
			</thead>
			<tbody>
				% if plist:
					% if votes.get(plist[0]["id"]) == None:
						% Register(plist[0]["id"])
					% end
				<tr class="warning">
					<td>{{plist[0]["title"]}}</td>
					<td>{{plist[0]["artist"]}}</td>
					<td>
						<form action="{{admin_uri}}" method="post">
							<input type="hidden" name="actionType" value="delete">
							<input type="hidden" name="deleteID" value="{{plist[0]["id"]}}">
							<button type="submit" class="btn btn-danger"><i class="fa fa-trash-o"></i></button>
						</form>
					</td>
					<td>
						<button class="btn btn-default disabled">
							<span class="fa fa-thumbs-up"></span> {{votes[plist[0]["id"]]}}
						</button>
					</td>
				</tr>
				% end
				% for song in plist[1:]:
					% if votes.get(song["id"]) == None:
						% Register(song["id"])
					% end
				<tr>
					<td>{{song["title"]}}</td>
					<td>{{song["artist"]}}</td>
					<td>
						<form action="{{admin_uri}}" method="post">
							<input type="hidden" name="actionType" value="delete">
							<input type="hidden" name="deleteID" value="{{song["id"]}}">
							<button type="submit" class="btn btn-danger"><i class="fa fa-trash-o"></i></button>
						</form>
					</td> <!-- /delete button -->
					<td>
							<form style="float: left; padding: 0px;" action="{{admin_uri}}" method="post">
								<input type="hidden" name="actionType" value="vote">
								<input type="hidden" name="votedirection" value="down">
								<input type="hidden" name="voteID" value="{{song["id"]}}">
								<button class="btn btn-secondary" type="submit">
									<i class="fa fa-minus"></i>
								</button>
							</form>
							<button style="float: left;" class="btn btn-secondary disabled">
								{{votes[song["id"]]}}
							</button>
							<form style="float: left; padding: 0px;" action="{{admin_uri}}" method="post">
								<input type="hidden" name="actionType" value="vote">
								<input type="hidden" name="votedirection" value="up">
								<input type="hidden" name="voteID" value="{{song["id"]}}">
								<button class="btn btn-secondary" type="submit">
									<i class="fa fa-plus"></i>
								</button>
							</form>
							<form style="float: left; padding: 0px;" action="{{admin_uri}}" method="post">
								<input type="hidden" name="actionType" value="vote">
								<input type="hidden" name="votedirection" value="420">
								<input type="hidden" name="voteID" value="{{song["id"]}}">
								<button class="btn btn-secondary" type="submit">
									<i class="fa fa-leaf"></i>
								</button>
							</form>
					</td> <!-- /votes buttons -->
				</tr>
			% end
			</tbody>
		</table>
	</body>
</html>
