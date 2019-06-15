{% extends 'base.tpl' %}

{# No searchbar #}
{% block searchbar %}
{% endblock %}

{% block content %}
	<div class="container">
		<h1 class="text-center">Welcome to Justify</h1>
		
		<img src="{{ url_for('static', filename='j256.png') }}" alt="logo" class="img-responsive mx-auto d-block" />

		<br>

		<br>

		<h6 class="text-center">You seem new here...</h6>
		<h5 class="text-center">Tell me your name to get started!</h5>

		{# Username field #}
		<form action="{{ url_for('web.new_user') }}" method="POST" class="input-group">
			<input type="text" id="username" name="username" class="form-control" placeholder="Your Name">
			<span class="input-group-append">
				<button class="btn btn-secondary" type="submit">
					<span class="mdi mdi-arrow-right-bold"></span>
				</button>
			</span>
		</form>

		<br>

		<br>

		<h4 class="list-group-item-heading">Add whatever music you want!</h4>
		<p style="font-size: 16px;" class="list-group-item-text">
			Search for any song. Results come from multiple music sources. Odds are you'll find what you're looking for.
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

	</div> {# /container #}
{% endblock %}
