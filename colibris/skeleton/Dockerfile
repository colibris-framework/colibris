FROM python:3.7

RUN apt -y update && apt -y install wait-for-it
RUN apt -y clean && rm -rf /var/lib/apt/lists/*
RUN pip install pipenv

COPY . /tmp/project
WORKDIR /tmp/project

RUN pipenv install --system --deploy
RUN python setup.py sdist
RUN pip install dist/*
RUN rm -rf /tmp/project /root/.cache/*
WORKDIR /

EXPOSE 8888
CMD ["__packagename__", "runserver"]
