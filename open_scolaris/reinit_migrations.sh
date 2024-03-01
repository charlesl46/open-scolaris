find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
rm db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
export DJANGO_SUPERUSER_PASSWORD=admin
python3 manage.py createsuperuser --noinput --username admin --email ad@min.fr
python3 manage.py populate
