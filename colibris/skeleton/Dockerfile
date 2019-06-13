
# Builder stage
FROM python:3.7-slim-stretch AS builder

ENV PROJECT_NAME __projectname__

COPY . /tmp/${PROJECT_NAME}
WORKDIR /tmp/${PROJECT_NAME}

# Make sure we have an up-to-date OS + python installation
RUN apt-get update && apt-get -y upgrade && \
    apt-get -y install build-essential git python-dev wait-for-it

# Install pipenv and lock down the version for the sake of reproducibility
RUN pip install pipenv==2018.11.26

# Install project deps using pipenv
RUN test -f Pipfile.lock || (echo 'Please run "pipenv lock" to generate the Pipfile.lock file'; false)
RUN pipenv install --system --deploy

# Install the project itself
RUN python setup.py sdist && pip install dist/*

# Cleanup
RUN rm -rf /tmp/${PROJECT_NAME} /root/.cache/*
WORKDIR /

# Server image
FROM builder AS server
EXPOSE 8888
CMD /usr/local/bin/${PROJECT_NAME} runserver

# Worker image
# FROM builder AS worker
# CMD /usr/local/bin/${PROJECT_NAME} runworker
