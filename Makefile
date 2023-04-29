install:
	poetry install

update:
	poetry update

shell:
	poetry shell

migrations:
	python manage.py makemigrations
	python manage.py migrate

publish:
	poetry publish --dry-run

lint:
	poetry run flake8

test:
	python manage.py test

test-cov:
	poetry run coverage run manage.py test -v 2 && coverage xml

dev:
	poetry run python manage.py runserver 0.0.0.0:8000

PORT ?= 8000
start: 
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application 