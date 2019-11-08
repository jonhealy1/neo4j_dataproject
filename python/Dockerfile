FROM python:3.7-alpine
# WORKDIR /code
# ENV FLASK_APP load_data_body.py
# ENV FLASK_RUN_HOST 0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# COPY . .
# CMD ["flask", "run"]
ENV PYTHONUNBUFFERED 1
RUN mkdir /python 
WORKDIR /python 
ADD requirements.txt /python
# COPY ./requirements.txt .
RUN pip install -r requirements.txt

ADD . /python/