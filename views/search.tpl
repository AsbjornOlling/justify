<!DOCTYPE html>
<!-- Displays playlist from mpd -->

<html>
	<head>
		<meta charset="utf-8">
		<title>DAKKEDAK</title>
		<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

	</head>
	<body>
		<form action="/search" method="post">
			<input class="hidden" name="searchtype" value="specific"/>
			SONG: <input name="inputsong" type="text" />
			<br><br>
			ARTIST: <input name="inputartist" type="text" />
			<br><br>
			ALBUM: <input name="inputalbum" type="text" />
			<br><br>
			<input value="FIND DIT DAK!" type="submit" />
		</form>
	</body>
</html>
