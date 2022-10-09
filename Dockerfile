FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /compliment
COPY requirements.txt /compliment/
RUN apt-get update
RUN apt-get -y install libev-dev libnss3
RUN pip install -r requirements.txt
COPY . /compliment/
