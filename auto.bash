#!/usr/bin/env bash

cd ~/Desktop/TheMovieBookAPI/themoviebookAPI/userprofiles/

rm *.pyc
rm *.py~

cd ..
cd themoviebookAPI/

rm *.pyc
rm *py~

cd ..

python manage.py makemigrations userprofiles
python manage.py migrate
python manage.py migrate --run-syncdb
python manage.py runserver
