FROM python:3.7

RUN apt -y update && apt -y install wait-for-it
RUN apt -y clean && rm -rf /var/lib/apt/lists/*
RUN pip install pipenv

COPY . /app
WORKDIR /app

RUN pipenv install --system --deploy
RUN /root/.cache/*

EXPOSE 8888
CMD ["python", "manage.py", "runserver"]
