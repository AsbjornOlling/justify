{% extends 'base.tpl' %}

{% block content %}
	<div class="container">
		
		<img src="{{ url_for('static', filename='j256.png') }}" alt="logo" class="img-responsive mx-auto d-block" />

		<br>

		<br>

		<h5 class="text-center">Tell me your name to get started!</h5>
		<form action="{{ url_for('web.new_user') }}" method="POST" class="input-group">
			<!-- username field -->
			<input type="text" id="username" name="username" class="form-control" placeholder="Your Name">

			<!-- submit button -->
			<span class="input-group-append">
				<button class="btn btn-secondary" type="submit">
					GO! <!-- TODO: icon here -->
				</button>
			</span>
		</form>

		<br>

		<br>

		<h4 class="list-group-item-heading">Add whatever music you want!</h4>
		<p style="font-size: 16px;" class="list-group-item-text">
			Search for any song. Results come from spotify, soundcloud, and youtube. Odds are you'll find what you're looking for.
		</p>

		<br>

		<h4 class="list-group-item-heading">No selfish speaker-hijacks. Ever.</h4>
		<p style="font-size: 16px;" class="list-group-item-text">
			The next song will always be the one in highest demand. 
			It's very simple; You leave a vote on the songs you want to hear, and the playlist sorts itself automagically.
		</p>

		<br>

		<h4 class="list-group-item-heading">Wow, that's fucking cool!</h4>
		<p style="font-size: 16px;" class="list-group-item-text">
			Right? Even better, it's 100% open source software! It was made for Roskilde Festival 2017 by Asbjørn, a member of Camp C.A.M.P.. 
			If you want to know more, go get Asbjørn a beer.
		</p>

	</div> <!-- /container -->
{% endblock %}
