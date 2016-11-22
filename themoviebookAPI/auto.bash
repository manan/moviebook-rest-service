cd ~/Desktop/TheMovieBook/themoviebookAPI/userprofiles/

rm *.pyc
rm *.py~
rm -rf migrations

cd ..

rm db.sqlite3

cd themoviebookAPI/

rm *.pyc
rm *py~

cd ..

python manage.py makemigrations userprofiles

python manage.py migrate

