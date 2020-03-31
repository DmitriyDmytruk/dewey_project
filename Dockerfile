FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /home/dewey_project
WORKDIR /home/dewey_project

RUN apk update && apk add postgresql-dev gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev musl-dev

COPY requirements.txt requirements.txt
RUN python -m venv dewey_project
RUN pip install -r ./requirements.txt
RUN pip install gunicorn

COPY webapp webapp
COPY migrations migrations
COPY main.py config.py manage.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP main.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
