FROM python:3.7

# install deps
RUN pip install pipenv
WORKDIR /tmp/
COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock
RUN pipenv install --system --deploy

# copy in the app
WORKDIR /
COPY ./justify /justify

# run it
CMD gunicorn --bind 0.0.0.0:80 justify:app
