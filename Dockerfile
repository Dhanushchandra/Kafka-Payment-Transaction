# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /Docker-Flask-Test

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app.py"]
CMD [ "python3", "lookup.py"]
CMD [ "python3", "produce.py"]