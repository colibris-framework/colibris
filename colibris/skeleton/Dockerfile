
# Builder stage
FROM colibris/python-base AS builder

ENV PROJECT_NAME __projectname__

COPY . /tmp/${PROJECT_NAME}
WORKDIR /tmp/${PROJECT_NAME}

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
