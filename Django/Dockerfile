FROM python:3

ENV PYTHONUNBUFFERED=1
ENV DOCKERIZE_VERSION v0.6.1

RUN apt-get update && apt-get -y install libpq-dev
RUN apt-get install python3-dev gcc -y

RUN mkdir /my_app_dir

WORKDIR /my_app_dir
RUN pip3 install django
RUN pip3 install djangorestframework
ADD requirements.txt ./
RUN pip3 install -r requirements.txt

RUN django-admin startproject backend .

RUN python3 manage.py startapp api

ADD api /my_app_dir/api

WORKDIR /my_app_dir/backend/

ADD settings.py ./settings.py
ADD .env ./.env

ADD urls.py ./urls.py

WORKDIR /my_app_dir/

EXPOSE 8000

RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz



CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


ENTRYPOINT ["dockerize", "-wait", "tcp://db:3306", "-timeout", "10s" ]

