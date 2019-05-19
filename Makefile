CODEGEN_DIR=./codegen

run:
	pipenv run \
	flask run

gunicorn-run:
	pipenv run \
	gunicorn --bind 0.0.0.0:8080 justify:app

gen-controller-code:
	pipenv run \
	python $(CODEGEN_DIR)/codegen.py \
	--template $(CODEGEN_DIR)/controller.tpl \
	--outdir justify/mopidy_api/controllers

