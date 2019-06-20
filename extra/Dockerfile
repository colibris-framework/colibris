
# Builder stage
FROM python:3.7-slim-stretch

# Make sure we have an up-to-date OS + python installation
RUN apt-get update && apt-get -y upgrade && \
    apt-get -y install build-essential git python-dev wait-for-it

# Install pipenv and lock down the version for the sake of reproducibility
RUN pip install pipenv==2018.11.26

# Cleanup
RUN apt-get clean autoclean && \
    apt-get autoremove --yes && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/
