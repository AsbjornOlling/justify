run:
	pipenv run \
	flask run

gunicorn-run:
	pipenv run \
	gunicorn --bind 0.0.0.0:8080 justify:app
