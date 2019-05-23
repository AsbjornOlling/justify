{% extends 'base.tpl' %}

{% block content %}
	<div class="container">
		
		<form action="/newuser" method="POST" class="input-group">
			<label for="username">Welcome! Please tell me your name.</label>

			<!-- username field -->
			<input type="text" id="username" name="username" class="form-control" placeholder="Your Name">

			<!-- submit button -->
			<span class="input-group-append">
				<button class="btn btn-secondary" type="submit">
					GO! <!-- TODO: icon here -->
				</button>
			</span>
		</form>

	</div> <!-- /container -->
{% endblock %}
