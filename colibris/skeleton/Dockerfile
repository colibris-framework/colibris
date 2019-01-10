FROM python:3.7

RUN apt -y update && apt -y install wait-for-it
RUN apt -y clean && rm -rf /var/lib/apt/lists/*
RUN pip install pipenv

COPY . /tmp/project
WORKDIR /tmp/project

RUN pipenv install --system --deploy
RUN rm -rf /root/.cache/*
RUN python setup.py install
#RUN rm -rf /tmp/project
#WORKDIR /

EXPOSE 8888
CMD ["python", "manage.py", "runserver"]
