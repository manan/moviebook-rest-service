#!/usr/bin/env bash

cd ~/Desktop/MovieBookAPI/MoviebookAPI/userprofiles/

rm *.pyc
rm *.py~

cd ..
cd MoviebookAPI/

rm *.pyc
rm *py~

cd ..

python manage.py makemigrations userprofiles
python manage.py migrate
python manage.py migrate --run-syncdb
python manage.py runserver
