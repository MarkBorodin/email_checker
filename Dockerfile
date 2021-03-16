FROM python:3.8

WORKDIR /srv
COPY requirements.txt /srv/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-deps
COPY . /srv/
