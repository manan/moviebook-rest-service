#!/usr/bin/env bash

python manage.py makemigrations userprofiles
python manage.py makemigrations posts
python manage.py makemigrations movies
python manage.py migrate
python manage.py migrate --run-syncdb
