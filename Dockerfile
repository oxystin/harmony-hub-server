FROM python:3.7-slim

ENV APP /harmonyserver
WORKDIR $APP

COPY requirements.txt $APP
RUN pip install -r requirements.txt

COPY . $APP

CMD [ "gunicorn", "-c", "gunicorn.conf", "main:app" ]
