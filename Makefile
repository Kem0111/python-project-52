install:
	poetry install

update:
	poetry update

publish:
	poetry publish --dry-run

lint:
	poetry run flake8 page_analyzer

test:
	poetry run pytest

reporter:
	coverage report -m

makemessages-ru:
	django-admin makemessages -l ru

makemessages-en:
	django-admin makemessages -l en

compilemessages:
	django-admin compilemessages

test-cov:
	poetry run pytest --cov-report xml --cov=page_analyzer tests/  

web: 
	gunicorn task_manager.wsgi