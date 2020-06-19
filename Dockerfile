FROM python:3.7-alpine

RUN adduser -D -g '' dewey

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /home/dewey
WORKDIR /home/dewey

RUN apk update && apk add postgresql-dev gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev musl-dev

COPY requirements.txt requirements.txt
RUN pip install -r ./requirements.txt
RUN pip install connexion[swagger-ui]
RUN pip install python-dotenv
RUN pip install gunicorn

COPY webapp webapp
COPY migrations migrations
COPY main.py config.py manage.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP main.py
USER dewey

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
