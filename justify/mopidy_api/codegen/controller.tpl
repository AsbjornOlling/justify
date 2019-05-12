
{% for m in methods %}

def {{ m }}():
	""" {{ methods[m]['description'] }} """
	pass

{% endfor %}
