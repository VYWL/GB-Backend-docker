#!/bin/bash

sudo docker build --tag ggulbob-django .

#docker run -d --name ggulbob-django-container -p 8000:8000 ggulbob-django
#docker exec -i -t ggulbob-django-container /bin/bash

#docker-compose up -d
