.PHONY: graph docs lint reinit runserver test

help:
	@echo "Actions disponibles :"
	@echo "  format      Formatte le code en utilisant l'outil black"
	@echo "  lint        Analyse le code avec pylint"
	@echo "  reinit      Supprime les fichiers de migration et recrée la base de données"
	@echo "  runserver   Démarre le serveur de développement Django"
	@echo "  test        Exécute les tests Django"

format:
	python3 -m black .

lint:
	python3 pylint --load-plugins pylint_django --rcfile .pylintrc **/*.py

reinit:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	rm db.sqlite3
	python3 manage.py makemigrations
	python3 manage.py migrate
	python3 manage.py populate
	export DJANGO_SUPERUSER_PASSWORD=admin
	python3 manage.py createsuperuser --noinput --username admin --email ad@min.fr

runserver:
	python3 manage.py runserver

test:
	python3 manage.py test
